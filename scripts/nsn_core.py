"""Logic dùng chung cho ghi sổ đơn hàng/sản xuất, báo cáo và sửa giá sản phẩm.

Dùng chung bởi cả script dòng lệnh (add_order.py, add_batch.py, weekly_report.py)
và app web local (webapp.py) để tránh hai nơi tính toán khác nhau.
"""
import csv
import json
import os
import shutil
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ORDERS_CSV = DATA_DIR / "orders.csv"
PRODUCTION_CSV = DATA_DIR / "production_log.csv"
PRODUCTS_JSON = DATA_DIR / "products.json"

ORDER_FIELDS = ["date", "customer", "product", "qty", "unit", "unit_price_vnd", "channel", "status", "note"]
BATCH_FIELDS = ["date", "product", "batch_id", "quantity", "unit", "note"]
CHANNELS = ["facebook", "zalo", "shopee", "lazada", "tiktok", "offline"]
STATUSES = ["moi", "da_giao", "da_huy"]
STATUS_LABELS = {"moi": "Mới", "da_giao": "Đã giao", "da_huy": "Đã huỷ"}


def backup_data():
    """Sao lưu data/ sang OneDrive (bản mới nhất + 1 bản theo ngày) sau mỗi lần ghi.

    Không có OneDrive hoặc lỗi ghi thì bỏ qua lặng lẽ — không được để hỏng việc ghi sổ chính.
    """
    onedrive = os.environ.get("OneDrive") or os.environ.get("ONEDRIVE")
    if not onedrive:
        return
    try:
        backup_root = Path(onedrive) / "NongSanNhaLam-Backup"
        latest_dir = backup_root / "latest"
        daily_dir = backup_root / "theo-ngay" / date.today().isoformat()
        latest_dir.mkdir(parents=True, exist_ok=True)
        daily_dir.mkdir(parents=True, exist_ok=True)
        for src in (ORDERS_CSV, PRODUCTION_CSV, PRODUCTS_JSON):
            if not src.exists():
                continue
            shutil.copy2(src, latest_dir / src.name)
            daily_target = daily_dir / src.name
            if not daily_target.exists():
                shutil.copy2(src, daily_target)
    except OSError:
        pass


def load_rows(path: Path):
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def append_row(path: Path, fields: list, row: dict):
    is_new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if is_new:
            writer.writeheader()
        writer.writerow(row)


def add_order(*, date_str=None, customer, product, qty, unit="kg", unit_price, channel, status="moi", note=""):
    if not customer:
        raise ValueError("Thiếu tên khách hàng")
    if not product:
        raise ValueError("Thiếu tên sản phẩm")
    if channel not in CHANNELS:
        raise ValueError(f"Kênh không hợp lệ: {channel}")
    if status not in STATUSES:
        raise ValueError(f"Trạng thái không hợp lệ: {status}")
    if qty is None or qty == "":
        raise ValueError("Thiếu số lượng")
    if unit_price is None or unit_price == "":
        raise ValueError("Thiếu đơn giá")
    qty = float(qty)
    unit_price = float(unit_price)
    row = {
        "date": date_str or date.today().isoformat(),
        "customer": customer,
        "product": product,
        "qty": qty,
        "unit": unit or "kg",
        "unit_price_vnd": unit_price,
        "channel": channel,
        "status": status,
        "note": note or "",
    }
    append_row(ORDERS_CSV, ORDER_FIELDS, row)
    backup_data()
    return row


def next_batch_id(product: str) -> str:
    prefix = "".join(w[0] for w in product.upper().split())[:3] or "SP"
    count = 0
    for row in load_rows(PRODUCTION_CSV):
        if row.get("product") == product:
            count += 1
    return f"{prefix}-{count + 1:03d}"


def add_batch(*, date_str=None, product, quantity, unit="kg", batch_id=None, note=""):
    if not product:
        raise ValueError("Thiếu tên sản phẩm")
    if quantity is None or quantity == "":
        raise ValueError("Thiếu sản lượng")
    quantity = float(quantity)
    batch_id = batch_id or next_batch_id(product)
    row = {
        "date": date_str or date.today().isoformat(),
        "product": product,
        "batch_id": batch_id,
        "quantity": quantity,
        "unit": unit or "kg",
        "note": note or "",
    }
    append_row(PRODUCTION_CSV, BATCH_FIELDS, row)
    backup_data()
    return row


def parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def compute_report(days: int = 7):
    since = date.today() - timedelta(days=days)

    orders = [r for r in load_rows(ORDERS_CSV) if (d := parse_date(r["date"])) and d >= since]
    batches = [r for r in load_rows(PRODUCTION_CSV) if (d := parse_date(r["date"])) and d >= since]

    revenue_by_product = defaultdict(float)
    qty_by_product = defaultdict(float)
    revenue_by_channel = defaultdict(float)
    total_revenue = 0.0
    active_orders = [r for r in orders if r["status"] != "da_huy"]
    for r in active_orders:
        line_total = float(r["qty"]) * float(r["unit_price_vnd"])
        revenue_by_product[r["product"]] += line_total
        qty_by_product[r["product"]] += float(r["qty"])
        revenue_by_channel[r["channel"]] += line_total
        total_revenue += line_total

    qty_produced = defaultdict(float)
    for r in batches:
        qty_produced[r["product"]] += float(r["quantity"])

    all_batches = load_rows(PRODUCTION_CSV)
    all_orders = load_rows(ORDERS_CSV)
    produced_total = defaultdict(float)
    for r in all_batches:
        produced_total[r["product"]] += float(r["quantity"])
    sold_total = defaultdict(float)
    for r in all_orders:
        if r["status"] != "da_huy":
            sold_total[r["product"]] += float(r["qty"])

    inventory = []
    for product in sorted(set(produced_total) | set(sold_total)):
        remaining = produced_total[product] - sold_total[product]
        warning = None
        if remaining < 0:
            warning = "ĐÃ NHẬN ĐƠN VƯỢT SỐ SẢN XUẤT — kiểm tra lại tồn kho!"
        elif remaining < 5:
            warning = "SẮP HẾT HÀNG"
        inventory.append({
            "product": product,
            "produced": produced_total[product],
            "sold": sold_total[product],
            "remaining": remaining,
            "warning": warning,
        })

    return {
        "days": days,
        "since": since.isoformat(),
        "order_count": len(active_orders),
        "total_revenue": total_revenue,
        "revenue_by_product": [
            {"product": p, "revenue": r, "qty": qty_by_product[p]}
            for p, r in sorted(revenue_by_product.items(), key=lambda x: -x[1])
        ],
        "revenue_by_channel": [
            {"channel": c, "revenue": r}
            for c, r in sorted(revenue_by_channel.items(), key=lambda x: -x[1])
        ],
        "production": [
            {"product": p, "qty": q}
            for p, q in sorted(qty_produced.items(), key=lambda x: -x[1])
        ],
        "inventory": inventory,
    }


def load_products():
    with PRODUCTS_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_products(data: dict):
    with PRODUCTS_JSON.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def update_variant_price(product_id: str, package: str, new_price: float):
    data = load_products()
    found = False
    for p in data["products"]:
        if p["id"] == product_id:
            for v in p["variants"]:
                if v["package"] == package:
                    v["price_vnd"] = new_price
                    found = True
    if not found:
        raise ValueError("Không tìm thấy sản phẩm/quy cách đó")
    data["updated_at"] = date.today().isoformat()
    save_products(data)
    backup_data()
    return data
