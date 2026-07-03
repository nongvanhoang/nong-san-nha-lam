#!/usr/bin/env python3
"""Ghi một mẻ sản xuất/thu hoạch mới vào data/production_log.csv."""
import argparse
import csv
import sys
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

LOG_CSV = Path(__file__).resolve().parent.parent / "data" / "production_log.csv"
FIELDS = ["date", "product", "batch_id", "quantity", "unit", "note"]


def next_batch_id(product: str) -> str:
    prefix = "".join(w[0] for w in product.upper().split())[:3] or "SP"
    count = 0
    if LOG_CSV.exists():
        with LOG_CSV.open("r", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("product") == product:
                    count += 1
    return f"{prefix}-{count + 1:03d}"


def main():
    parser = argparse.ArgumentParser(description="Ghi mẻ sản xuất/thu hoạch mới")
    parser.add_argument("--date", default=date.today().isoformat(), help="Ngày sản xuất/thu hoạch (YYYY-MM-DD)")
    parser.add_argument("--product", required=True, help="Tên sản phẩm, VD: 'Tinh Bột Sắn Dây'")
    parser.add_argument("--quantity", required=True, type=float, help="Sản lượng")
    parser.add_argument("--unit", default="kg", help="Đơn vị, mặc định 'kg'")
    parser.add_argument("--batch-id", dest="batch_id", default=None, help="Mã mẻ, để trống sẽ tự sinh")
    parser.add_argument("--note", default="", help="Ghi chú thêm")
    args = parser.parse_args()

    batch_id = args.batch_id or next_batch_id(args.product)

    row = {
        "date": args.date,
        "product": args.product,
        "batch_id": batch_id,
        "quantity": args.quantity,
        "unit": args.unit,
        "note": args.note,
    }

    is_new_file = not LOG_CSV.exists()
    with LOG_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if is_new_file:
            writer.writeheader()
        writer.writerow(row)

    print(f"Đã ghi mẻ {batch_id}: {args.product} - {args.quantity}{args.unit} ngày {args.date}")


if __name__ == "__main__":
    main()
