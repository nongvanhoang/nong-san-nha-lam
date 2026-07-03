#!/usr/bin/env python3
"""Ghi một đơn hàng mới vào data/orders.csv."""
import argparse
import csv
import sys
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ORDERS_CSV = Path(__file__).resolve().parent.parent / "data" / "orders.csv"
FIELDS = ["date", "customer", "product", "qty", "unit", "unit_price_vnd", "channel", "status", "note"]


def main():
    parser = argparse.ArgumentParser(description="Ghi đơn hàng mới")
    parser.add_argument("--date", default=date.today().isoformat(), help="Ngày đặt hàng (YYYY-MM-DD), mặc định hôm nay")
    parser.add_argument("--customer", required=True, help="Tên khách hàng")
    parser.add_argument("--product", required=True, help="Tên sản phẩm, VD: 'Tinh Bột Sắn Dây'")
    parser.add_argument("--qty", required=True, type=float, help="Số lượng")
    parser.add_argument("--unit", default="kg", help="Đơn vị, mặc định 'kg'")
    parser.add_argument("--unit-price", required=True, type=float, dest="unit_price", help="Đơn giá (VNĐ)")
    parser.add_argument("--channel", required=True, choices=["facebook", "zalo", "shopee", "lazada", "tiktok", "offline"], help="Kênh bán hàng")
    parser.add_argument("--status", default="moi", choices=["moi", "da_giao", "da_huy"], help="Trạng thái đơn, mặc định 'moi'")
    parser.add_argument("--note", default="", help="Ghi chú thêm")
    args = parser.parse_args()

    row = {
        "date": args.date,
        "customer": args.customer,
        "product": args.product,
        "qty": args.qty,
        "unit": args.unit,
        "unit_price_vnd": args.unit_price,
        "channel": args.channel,
        "status": args.status,
        "note": args.note,
    }

    is_new_file = not ORDERS_CSV.exists()
    with ORDERS_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if is_new_file:
            writer.writeheader()
        writer.writerow(row)

    total = args.qty * args.unit_price
    print(f"Đã ghi đơn: {args.customer} - {args.product} x{args.qty}{args.unit} = {total:,.0f} VNĐ ({args.channel})")


if __name__ == "__main__":
    main()
