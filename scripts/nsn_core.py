"""Logic dùng chung cho ghi sổ đơn hàng/sản xuất, báo cáo và sửa giá sản phẩm.

Dùng chung bởi cả script dòng lệnh (add_order.py, add_batch.py, weekly_report.py)
và app web local (webapp.py) để tránh hai nơi tính toán khác nhau.
"""
import csv
import json
import os
import re
import shutil
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ORDERS_CSV = DATA_DIR / "orders.csv"
PRODUCTION_CSV = DATA_DIR / "production_log.csv"
EXPENSES_CSV = DATA_DIR / "expenses.csv"
TARGETS_JSON = DATA_DIR / "muc_tieu.json"
PRODUCTS_JSON = DATA_DIR / "products.json"
B2B_CSV = BASE_DIR / "DANH_SACH_KHACH_HANG_B2B.csv"
CUSTOMERS_CSV = DATA_DIR / "customers.csv"
LICH_DANG_BAI_MD = BASE_DIR / "LICH_DANG_BAI.md"
VIEC_CAN_LAM_MD = BASE_DIR / "VIEC_CAN_LAM.md"
POSTS_READY_MD = BASE_DIR / "content" / "posts_ready.md"
POSTED_LOG_CSV = DATA_DIR / "posted_log.csv"
POSTED_LOG_FIELDS = ["date", "chu_de", "channel", "time"]

B2B_FIELDS = [
    "Nhom", "Uu_tien", "Ten", "Chuyen_ve_Ly_do_phu_hop", "Khu_vuc", "SDT",
    "Email", "Website", "Facebook", "Nguon", "Trang_thai", "Ghi_chu",
]

ORDER_FIELDS = ["date", "customer", "product", "qty", "unit", "unit_price_vnd", "channel", "status", "phone", "address", "note"]
BATCH_FIELDS = ["date", "product", "batch_id", "quantity", "unit", "note"]
EXPENSE_FIELDS = ["date", "category", "amount_vnd", "note"]
CUSTOMER_FIELDS = ["name", "phone", "address", "note", "updated_at"]
CHANNELS = ["facebook", "zalo", "shopee", "lazada", "tiktok", "offline"]
STATUSES = ["moi", "da_giao", "da_huy"]
STATUS_LABELS = {"moi": "Mới", "da_giao": "Đã giao", "da_huy": "Đã huỷ"}
EXPENSE_CATEGORIES = [
    "nguyen_lieu", "bao_bi_nhan", "van_chuyen", "quang_cao",
    "in_an", "dung_cu_may_moc", "giay_to_phap_ly", "khac",
]
EXPENSE_CATEGORY_LABELS = {
    "nguyen_lieu": "Nguyên liệu",
    "bao_bi_nhan": "Bao bì/nhãn",
    "van_chuyen": "Vận chuyển",
    "quang_cao": "Quảng cáo",
    "in_an": "In ấn",
    "dung_cu_may_moc": "Dụng cụ/máy móc",
    "giay_to_phap_ly": "Giấy tờ/pháp lý",
    "khac": "Khác",
}


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
        for src in (ORDERS_CSV, PRODUCTION_CSV, PRODUCTS_JSON, B2B_CSV, EXPENSES_CSV, CUSTOMERS_CSV):
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


def add_order(*, date_str=None, customer, product, qty, unit="kg", unit_price, channel, status="moi", phone="", address="", note=""):
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
        "phone": phone or "",
        "address": address or "",
        "note": note or "",
    }
    append_row(ORDERS_CSV, ORDER_FIELDS, row)
    if phone or address:
        upsert_customer(name=customer, phone=phone, address=address)
    backup_data()
    return row


def upsert_customer(*, name, phone="", address="", note=""):
    """Lưu/cập nhật số điện thoại + địa chỉ giao hàng gần nhất cho 1 khách — để lần
    ghi đơn sau không phải hỏi lại địa chỉ khách quen (SOP.md mục 1). Khớp theo tên
    chính xác; khớp tay nếu khách đổi tên gọi khác lần sau (hiếm, không tự động)."""
    if not name:
        return None
    rows = load_rows(CUSTOMERS_CSV)
    target = None
    for r in rows:
        if r.get("name", "").strip().lower() == name.strip().lower():
            target = r
            break
    if target is None:
        target = {"name": name, "phone": "", "address": "", "note": ""}
        rows.append(target)
    if phone:
        target["phone"] = phone
    if address:
        target["address"] = address
    if note:
        target["note"] = note
    target["updated_at"] = date.today().isoformat()

    tmp_path = CUSTOMERS_CSV.with_suffix(".csv.tmp")
    with tmp_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CUSTOMER_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(tmp_path, CUSTOMERS_CSV)
    return target


def find_customer(name: str):
    """Tra cứu SĐT/địa chỉ gần nhất đã lưu cho 1 khách theo tên (khớp chính xác,
    không phân biệt hoa/thường) — dùng để tự điền sẵn khi ghi đơn cho khách quen."""
    if not name:
        return None
    for r in load_rows(CUSTOMERS_CSV):
        if r.get("name", "").strip().lower() == name.strip().lower():
            return r
    return None


def add_expense(*, date_str=None, category, amount, note=""):
    if category not in EXPENSE_CATEGORIES:
        raise ValueError(f"Hạng mục không hợp lệ: {category} (chọn trong {EXPENSE_CATEGORIES})")
    if amount is None or amount == "":
        raise ValueError("Thiếu số tiền")
    amount = float(amount)
    if amount <= 0:
        raise ValueError("Số tiền phải lớn hơn 0")
    row = {
        "date": date_str or date.today().isoformat(),
        "category": category,
        "amount_vnd": amount,
        "note": note or "",
    }
    append_row(EXPENSES_CSV, EXPENSE_FIELDS, row)
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
    expenses = [r for r in load_rows(EXPENSES_CSV) if (d := parse_date(r["date"])) and d >= since]

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

    expenses_by_category = defaultdict(float)
    total_expenses = 0.0
    for r in expenses:
        amount = float(r["amount_vnd"])
        expenses_by_category[r["category"]] += amount
        total_expenses += amount

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
        "total_expenses": total_expenses,
        "expenses_by_category": [
            {"category": c, "label": EXPENSE_CATEGORY_LABELS.get(c, c), "amount": a}
            for c, a in sorted(expenses_by_category.items(), key=lambda x: -x[1])
        ],
        "profit": total_revenue - total_expenses,
    }


def compute_month_to_date():
    """Doanh thu/chi phí/lãi lỗ từ đầu tháng dương lịch hiện tại đến hôm nay,
    đối chiếu với mục tiêu tháng trong data/muc_tieu.json (nếu có) — dùng để biết
    đang đi đúng hướng mục tiêu tăng trưởng hay không, không chỉ nhìn 7 ngày gần nhất."""
    today = date.today()
    since = today.replace(day=1)
    days = (today - since).days + 1
    report = compute_report(days)

    targets = {}
    if TARGETS_JSON.exists():
        with TARGETS_JSON.open("r", encoding="utf-8") as f:
            targets = json.load(f)

    return {
        "month": today.strftime("%Y-%m"),
        "since": since.isoformat(),
        "revenue": report["total_revenue"],
        "expenses": report["total_expenses"],
        "profit": report["profit"],
        "target_revenue": targets.get("doanh_thu_thang_vnd"),
        "target_profit": targets.get("loi_nhuan_thang_vnd"),
    }


def compute_repeat_customers(min_orders: int = 2):
    """Gom đơn hàng theo tên khách (đã bỏ đơn huỷ), trả về danh sách khách có
    từ min_orders đơn trở lên, sắp xếp theo số đơn giảm dần — dùng để nhắn lại
    khách quen khi có mẻ mới/ưu đãi, thay vì chỉ chạy theo lead B2B lạ."""
    orders = [r for r in load_rows(ORDERS_CSV) if r.get("status") != "da_huy"]
    by_customer = defaultdict(lambda: {"order_count": 0, "total_revenue": 0.0, "products": set(), "last_date": None})
    for r in orders:
        c = by_customer[r["customer"]]
        c["order_count"] += 1
        c["total_revenue"] += float(r["qty"]) * float(r["unit_price_vnd"])
        c["products"].add(r["product"])
        d = parse_date(r["date"])
        if d and (c["last_date"] is None or d > c["last_date"]):
            c["last_date"] = d

    result = [
        {
            "customer": name,
            "order_count": v["order_count"],
            "total_revenue": v["total_revenue"],
            "products": sorted(v["products"]),
            "last_date": v["last_date"].isoformat() if v["last_date"] else None,
        }
        for name, v in by_customer.items()
        if v["order_count"] >= min_orders
    ]
    result.sort(key=lambda x: (-x["order_count"], -x["total_revenue"]))
    return result


_DEADLINE_SECTION_RE = re.compile(r"^## ⏰.*?\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
_DEADLINE_BULLET_SPLIT_RE = re.compile(r"\n(?=- \[[ x]\] \*\*)")
_DEADLINE_TITLE_RE = re.compile(r"^- \[([ x])\] \*\*(.+?)\*\*")
_DATE_DMY_RE = re.compile(r"(\d{2})/(\d{2})/(\d{4})")


def find_upcoming_deadlines():
    """Tìm các việc có hạn chót cụ thể (ngày/tháng/năm) trong mục '## ⏰ ...' đầu
    VIEC_CAN_LAM.md — chỉ đọc mục này (không quét cả file) để tránh nhặt nhầm ngày
    tháng xuất hiện trong ghi chú việc khác không phải hạn chót thật."""
    if not VIEC_CAN_LAM_MD.exists():
        return []
    text = VIEC_CAN_LAM_MD.read_text(encoding="utf-8")
    m = _DEADLINE_SECTION_RE.search(text)
    if not m:
        return []
    section = m.group(1)

    today = date.today()
    results = []
    for bullet in _DEADLINE_BULLET_SPLIT_RE.split(section):
        title_m = _DEADLINE_TITLE_RE.match(bullet.strip())
        if not title_m:
            continue
        dates = _DATE_DMY_RE.findall(bullet)
        if not dates:
            continue
        d, mo, y = dates[0]  # ngày gần nhất nhắc tới trong bullet, thường là hạn chính
        try:
            deadline = date(int(y), int(mo), int(d))
        except ValueError:
            continue
        results.append({
            "title": title_m.group(2).strip(),
            "done": title_m.group(1) == "x",
            "deadline": deadline.isoformat(),
            "days_left": (deadline - today).days,
        })
    results.sort(key=lambda x: x["days_left"])
    return results


def find_customers_to_followup(min_orders=1, days_since_threshold=21):
    """Khách đã mua ít nhất min_orders đơn nhưng đã quá days_since_threshold ngày
    chưa quay lại mua tiếp — gợi ý nhắn lại chủ động thay vì chỉ ngồi chờ khách tự
    nhắn (đúng chu kỳ mua lại tự nhiên ghi trong content/templates/nhan_tin_truc_tiep.md)."""
    today = date.today()
    result = []
    for c in compute_repeat_customers(min_orders):
        last = parse_date(c["last_date"]) if c["last_date"] else None
        if last is None:
            continue
        days_since = (today - last).days
        if days_since >= days_since_threshold:
            result.append({**c, "days_since_last_order": days_since})
    result.sort(key=lambda x: -x["days_since_last_order"])
    return result


# Cùng thứ tự ưu tiên Giai đoạn 0->4 trong KE_HOACH_KHAI_THAC_B2B.md, lặp lại có chủ đích từ
# app.js (NHOM_PRIORITY) - phía backend chỉ cần cho "Hôm nay nên gọi ai" ở tab Tổng quan, không
# đụng vào bảng B2B đầy đủ ở tab "Bán hàng hôm nay" (vẫn do JS tự sắp như cũ) để tránh rủi ro
# sửa nhầm thứ đang chạy ổn.
_NHOM_PRIORITY = {"N": 0, "B": 1, "F": 1, "H": 2, "J": 2, "K": 2, "L": 3, "M": 3, "A": 4}


def _nhom_tier(nhom_full: str) -> int:
    letter = (nhom_full or "").strip()[:1]
    return _NHOM_PRIORITY.get(letter, 9)


def get_today_call_list(n: int = 10):
    """Danh sách N lead B2B trong nước nên gọi/nhắn hôm nay — lọc 'chưa liên hệ', sắp theo đúng
    thứ tự ưu tiên Giai đoạn 0->4. Không cần con trỏ/trạng thái riêng như hàng đợi đăng bài: mỗi
    khi 1 lead đổi Trang_thai (báo kết quả cuộc gọi), lead đó tự rơi khỏi danh sách này, nên gọi
    lại hàm này luôn ra đúng danh sách tiếp theo chưa gọi."""
    leads = [
        r for r in load_b2b_leads()
        if not r.get("Trang_thai", "").strip() or r.get("Trang_thai", "").strip() == "Chưa liên hệ"
    ]
    def uu_tien(r):
        try:
            return int(r.get("Uu_tien") or 9)
        except ValueError:
            return 9

    leads.sort(key=lambda r: (_nhom_tier(r.get("Nhom", "")), uu_tien(r)))
    return leads[:n]


def compute_today_overview():
    """Gộp mọi thứ cần biết 'hôm nay phải làm gì' vào 1 chỗ — bài cần đăng, hạn chót
    gần nhất, cảnh báo tồn kho, số tài chính tháng này, khách quen lâu chưa quay lại
    — thay vì phải mở riêng từng tab/file mới ghép lại được bức tranh đầy đủ."""
    report = compute_report(1)
    return {
        "today_post": get_todays_post(),
        "deadlines": find_upcoming_deadlines()[:5],
        "inventory_warnings": [i for i in report["inventory"] if i["warning"]],
        "month": compute_month_to_date(),
        "followups": find_customers_to_followup()[:10],
        "today_calls": get_today_call_list(10),
    }


MEDIA_ROOTS = [
    BASE_DIR / "Hình Ảnh, Video",
    BASE_DIR / "docs" / "assets",
    BASE_DIR / "content" / "video" / "output",
]
MEDIA_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MEDIA_VIDEO_EXTS = {".mp4", ".mov", ".webm"}


def _media_category(rel_path: str) -> str:
    lower = rel_path.lower()
    if "sắn dây" in lower or "san-day" in lower or "san_day" in lower:
        return "san-day"
    if "cam" in lower:
        return "cam"
    return "khac"


def _posts_ready_blocks_for_media():
    if not POSTS_READY_MD.exists():
        return []
    text = POSTS_READY_MD.read_text(encoding="utf-8")
    parts = re.split(r"\n(?=## )", text)
    blocks = []
    for part in parts:
        if not part.startswith("## "):
            continue
        heading = part.splitlines()[0][3:].strip()
        blocks.append((heading, part))
    return blocks


def scan_media_library():
    """Quét toàn bộ ảnh/video trong 3 nguồn (gốc, web, video đã dựng), đối chiếu tên file
    với content/posts_ready.md để biết đã dùng trong bài nào chưa — giải quyết đúng việc phải
    dò tay xem 1 file đã lên bài chưa, tốn thời gian nhất khi chuẩn bị nội dung."""
    blocks = _posts_ready_blocks_for_media()
    items = []
    for root in MEDIA_ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            ext = p.suffix.lower()
            if ext in MEDIA_IMAGE_EXTS:
                kind = "image"
            elif ext in MEDIA_VIDEO_EXTS:
                kind = "video"
            else:
                continue
            rel_path = p.relative_to(BASE_DIR).as_posix()
            used_in = [heading for heading, block in blocks if p.name in block]
            stat = p.stat()
            items.append({
                "rel_path": rel_path,
                "name": p.name,
                "kind": kind,
                "category": _media_category(rel_path),
                "size": stat.st_size,
                "mtime": stat.st_mtime,
                "used_in": used_in,
            })
    items.sort(key=lambda x: -x["mtime"])
    return items


def load_products():
    with PRODUCTS_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_products(data: dict):
    tmp_path = PRODUCTS_JSON.with_suffix(".json.tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp_path, PRODUCTS_JSON)


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


def load_b2b_leads():
    """Đọc danh sách khách B2B — giữ nguyên encoding UTF-8 with BOM của file gốc.
    Một vài dòng cũ từng bị ghi thiếu dấu ngoặc kép quanh field có dấu phẩy, khiến
    csv.DictReader tách dư cột (dồn vào key None) — gộp phần dư đó trở lại Ghi_chu
    thay vì để mất, và không bao giờ để dict có key None lọt ra ngoài (key None sẽ
    làm DictWriter báo lỗi khi ghi lại)."""
    if not B2B_CSV.exists():
        return []
    with B2B_CSV.open("r", newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        extra = r.pop(None, None)
        if extra:
            extra_text = ",".join(extra) if isinstance(extra, list) else str(extra)
            r["Ghi_chu"] = f"{r.get('Ghi_chu', '').strip()}, {extra_text}".strip(", ")
    return rows


def save_b2b_leads(rows: list):
    """Ghi đè toàn bộ danh sách - giữ đúng encoding (UTF-8 with BOM) và line ending
    (CRLF) của file gốc để không phá cấu trúc file khi Git/Excel mở lại.

    Ghi ra file TẠM trước, chỉ os.replace() vào file thật sau khi ghi xong hoàn
    toàn không lỗi — tránh lặp lại sự cố 2026-09-08 (1 dòng dữ liệu cũ lỗi định
    dạng khiến DictWriter ném lỗi giữa chừng, làm mất gần hết 500 dòng vì ghi đè
    trực tiếp lên file thật)."""
    tmp_path = B2B_CSV.with_suffix(".csv.tmp")
    with tmp_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=B2B_FIELDS, lineterminator="\r\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(tmp_path, B2B_CSV)
    backup_data()


def update_b2b_lead(ten: str, *, trang_thai: str = None, ghi_chu_them: str = ""):
    """Cập nhật Trạng_thái/Ghi_chú cho 1 lead theo tên (khớp chính xác cột Ten).
    Ghi_chu_them được NỐI vào ghi chú cũ bằng ' | ', không xoá ghi chú cũ."""
    rows = load_b2b_leads()
    target = None
    for r in rows:
        if r.get("Ten", "").strip() == ten.strip():
            target = r
            break
    if target is None:
        raise ValueError(f"Không tìm thấy lead có tên: {ten}")

    if trang_thai is not None:
        target["Trang_thai"] = trang_thai
    if ghi_chu_them:
        existing = target.get("Ghi_chu", "").strip()
        stamp = date.today().isoformat()
        addition = f"{ghi_chu_them} ({stamp})"
        target["Ghi_chu"] = f"{existing} | {addition}" if existing else addition

    save_b2b_leads(rows)
    return target


_HEADING_RE = re.compile(r"^##\s+(Facebook|Zalo|Instagram|LinkedIn|YouTube[^—]*)\s+—\s+(.+?)(?:\s*\(.*\))?\s*$")


def get_todays_post():
    """Tìm bài đăng đã lên lịch cho HÔM NAY trong LICH_DANG_BAI.md (bảng checklist
    'Ngày | Chủ đề | ...'), rồi lấy nội dung từng kênh tương ứng trong
    posts_ready.md (khớp theo chuỗi Chủ đề nằm trong tiêu đề '## Kênh — Chủ đề...').
    Chỉ đọc, không ghi gì — đánh dấu đã đăng vẫn làm thủ công qua chat với Claude."""
    today_dm = date.today().strftime("%d/%m")

    chu_de = None
    if LICH_DANG_BAI_MD.exists():
        text = LICH_DANG_BAI_MD.read_text(encoding="utf-8")
        for line in text.splitlines():
            m = re.match(r"\|\s*(\d{2}/\d{2})\s*\|\s*(.+?)\s*\|", line)
            if m and m.group(1) == today_dm:
                chu_de = m.group(2).strip()
                # bỏ ghi chú kiểu "(video, dựng xong 06/09)" trong ô Chủ đề để so khớp posts_ready.md gọn hơn
                chu_de = re.sub(r"\s*\(.*?\)\s*$", "", chu_de).strip()
                break

    if not chu_de:
        return {"chu_de": None, "channels": {}}

    channels = {}
    if POSTS_READY_MD.exists():
        text = POSTS_READY_MD.read_text(encoding="utf-8")
        blocks = text.split("\n---\n")
        for block in blocks:
            lines = block.strip().splitlines()
            if not lines:
                continue
            m = _HEADING_RE.match(lines[0].strip())
            if not m:
                continue
            channel, block_chu_de = m.group(1).strip(), m.group(2).strip()
            if chu_de.lower() in block_chu_de.lower() or block_chu_de.lower() in chu_de.lower():
                body = "\n".join(lines[1:]).strip()
                channels[channel] = body

    posted = get_posted_today(chu_de) if chu_de else []
    return {"chu_de": chu_de, "channels": channels, "posted": posted}


def mark_posted(chu_de: str, channel: str):
    """Ghi nhận đã đăng 1 kênh cho 1 chủ đề vào nhật ký riêng (data/posted_log.csv)
    — KHÔNG động vào LICH_DANG_BAI.md (cấu trúc markdown đó đổi format theo từng
    tuần, tự parse/ghi lại rủi ro làm hỏng file mà không phải phần thưởng lớn).
    LICH_DANG_BAI.md vẫn cần tick tay như trước, đây chỉ giúp app tự nhớ trong
    ngày cái nào đã bấm "Đã đăng" rồi, khỏi bấm nhầm 2 lần."""
    row = {
        "date": date.today().isoformat(),
        "chu_de": chu_de,
        "channel": channel,
        "time": datetime.now().strftime("%H:%M:%S"),
    }
    append_row(POSTED_LOG_CSV, POSTED_LOG_FIELDS, row)
    return row


def get_posted_today(chu_de: str):
    """Trả về danh sách tên kênh đã đăng HÔM NAY cho đúng chủ đề này."""
    rows = load_rows(POSTED_LOG_CSV)
    today = date.today().isoformat()
    return [r["channel"] for r in rows if r["date"] == today and r["chu_de"] == chu_de]
