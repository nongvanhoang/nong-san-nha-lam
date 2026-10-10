#!/usr/bin/env python3
"""Chép đơn/khách chờ từ trang "Sổ Đơn Nhà Làm" (artifact claude.ai) về sổ CSV trên máy.

Claude chạy quy trình này khi người dùng nhắn "đồng bộ đơn":
  1. ArtifactData list collection `orders` và `waitlist` với out_dir=<thư mục tạm>
  2. python scripts/sync_so_don.py <thư mục tạm>
  3. Đánh dấu synced=true cho các id script in ra (ArtifactData batch update)

- Nông Sản Nhà Làm -> data/orders.csv qua nsn_core.add_order (quy ra kg như luật của sổ).
- Tiệm Cháo Măm Măm -> C:/Users/Admin/TiemChaoMamMam/data/orders.csv (cột id = id trên trang).
- Khách chờ -> data/danh_sach_cho.csv, GHI LẠI TOÀN BỘ từ trang (trang là nguồn gốc của danh sách này).
Đơn đã có trong sổ (trùng id) thì bỏ qua, nên chạy lại nhiều lần không bị nhân đôi.
"""
import csv
import json
import os
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nsn_core import ORDERS_CSV, add_order  # noqa: E402

NSN_ROOT = Path(__file__).resolve().parent.parent
WAITLIST_CSV = NSN_ROOT / "data" / "danh_sach_cho.csv"
WAIT_FIELDS = ["id", "ngay_dang_ky", "ten", "lien_he", "quan_tam", "nguon", "da_bao", "ghi_chu"]
TC_ORDERS_CSV = Path("C:/Users/Admin/TiemChaoMamMam/data/orders.csv")
TC_FIELDS = ["id", "date", "time", "customer_name", "phone", "address", "item", "size",
             "qty", "unit_price_vnd", "delivery_fee_vnd", "total_vnd", "channel", "note"]
TAG = "[sodon:{}]"


def load_docs(folder: Path, collection: str) -> list:
    d = folder / collection
    if not d.exists():
        return []
    docs = []
    for f in sorted(d.glob("*.json")):
        body = json.loads(f.read_text(encoding="utf-8"))
        body = body.get("data", body) if isinstance(body.get("data"), dict) else body
        body["_id"] = f.stem
        docs.append(body)
    return docs


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def sync_nsn(doc: dict) -> bool:
    if TAG.format(doc["_id"]) in read_text(ORDERS_CSV):
        return False
    count = float(doc.get("count") or 1)
    price = float(doc.get("price") or 0)
    kg = doc.get("kg_per_pkg")
    if kg:
        qty, unit, unit_price = count * float(kg), "kg", price / float(kg)
    else:
        qty, unit, unit_price = count, "goi", price
    extras = [f"{int(count) if count.is_integer() else count} x {doc.get('pkg') or 'gói'}"]
    if doc.get("phone"):
        extras.append(f"SĐT {doc['phone']}")
    if doc.get("note"):
        extras.append(doc["note"])
    extras.append(TAG.format(doc["_id"]))
    add_order(date_str=doc.get("date"), customer=doc["customer"], product=doc["product"], qty=qty,
              unit=unit, unit_price=round(unit_price), channel=doc["channel"],
              status=doc.get("status") or "moi", note=" · ".join(extras))
    return True


def sync_tc(doc: dict) -> bool:
    existing = read_text(TC_ORDERS_CSV)
    if f"\n{doc['_id']}," in existing:
        return False
    row = {
        "id": doc["_id"], "date": doc.get("date"), "time": doc.get("time"),
        "customer_name": doc.get("customer"), "phone": doc.get("phone") or "",
        "address": doc.get("address") or ("tại quán" if doc.get("channel") == "walk-in" else ""),
        "item": doc.get("product"), "size": doc.get("size"), "qty": doc.get("count"),
        "unit_price_vnd": doc.get("price"), "delivery_fee_vnd": doc.get("delivery_fee") or 0,
        "total_vnd": doc.get("total"), "channel": doc.get("channel"), "note": doc.get("note") or "",
    }
    is_new = not TC_ORDERS_CSV.exists() or not existing.strip()
    with TC_ORDERS_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=TC_FIELDS)
        if is_new:
            w.writeheader()
        w.writerow(row)
    return True


def write_waitlist(docs: list) -> None:
    docs = sorted(docs, key=lambda d: d.get("createdAt") or 0)
    fd, tmp = tempfile.mkstemp(dir=WAITLIST_CSV.parent, suffix=".tmp")
    with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=WAIT_FIELDS)
        w.writeheader()
        for d in docs:
            w.writerow({k: (d["_id"] if k == "id" else d.get(k, "")) for k in WAIT_FIELDS})
    os.replace(tmp, WAITLIST_CSV)  # ghi an toàn: không bao giờ để sổ bị cắt dở


def main():
    if len(sys.argv) != 2:
        sys.exit("Cách dùng: sync_so_don.py <thư mục out_dir của ArtifactData>")
    folder = Path(sys.argv[1])
    orders = load_docs(folder, "orders")
    waits = load_docs(folder, "waitlist")
    done, skipped, errors = [], [], []
    for doc in orders:
        if doc.get("synced"):
            continue
        try:
            added = sync_nsn(doc) if doc.get("project") == "nsn" else sync_tc(doc)
            (done if added else skipped).append(doc["_id"])
        except Exception as e:  # 1 đơn lỗi không được chặn các đơn khác
            errors.append(f"{doc['_id']}: {e}")
    if waits:
        write_waitlist(waits)
    print(json.dumps({"orders_synced": done + skipped, "orders_new": len(done), "orders_already_in_book": len(skipped),
                      "waitlist_ids": [w["_id"] for w in waits if not w.get("synced")],
                      "waitlist_total": len(waits), "errors": errors}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
