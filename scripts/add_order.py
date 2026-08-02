#!/usr/bin/env python3
"""Ghi một đơn hàng mới vào data/orders.csv."""
import argparse
import sys
from datetime import date

from nsn_core import CHANNELS, STATUSES, add_order

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Ghi đơn hàng mới")
    parser.add_argument("--date", default=date.today().isoformat(), help="Ngày đặt hàng (YYYY-MM-DD), mặc định hôm nay")
    parser.add_argument("--customer", required=True, help="Tên khách hàng")
    parser.add_argument("--product", required=True, help="Tên sản phẩm, VD: 'Tinh Bột Sắn Dây'")
    parser.add_argument("--qty", required=True, type=float, help="Số lượng")
    parser.add_argument("--unit", default="kg", help="Đơn vị, mặc định 'kg'")
    parser.add_argument("--unit-price", required=True, type=float, dest="unit_price", help="Đơn giá (VNĐ)")
    parser.add_argument("--channel", required=True, choices=CHANNELS, help="Kênh bán hàng")
    parser.add_argument("--status", default="moi", choices=STATUSES, help="Trạng thái đơn, mặc định 'moi'")
    parser.add_argument("--note", default="", help="Ghi chú thêm")
    args = parser.parse_args()

    row = add_order(
        date_str=args.date,
        customer=args.customer,
        product=args.product,
        qty=args.qty,
        unit=args.unit,
        unit_price=args.unit_price,
        channel=args.channel,
        status=args.status,
        note=args.note,
    )

    total = row["qty"] * row["unit_price_vnd"]
    print(f"Đã ghi đơn: {row['customer']} - {row['product']} x{row['qty']}{row['unit']} = {total:,.0f} VNĐ ({row['channel']})")


if __name__ == "__main__":
    main()
