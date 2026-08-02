#!/usr/bin/env python3
"""Ghi một mẻ sản xuất/thu hoạch mới vào data/production_log.csv."""
import argparse
import sys
from datetime import date

from nsn_core import add_batch

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Ghi mẻ sản xuất/thu hoạch mới")
    parser.add_argument("--date", default=date.today().isoformat(), help="Ngày sản xuất/thu hoạch (YYYY-MM-DD)")
    parser.add_argument("--product", required=True, help="Tên sản phẩm, VD: 'Tinh Bột Sắn Dây'")
    parser.add_argument("--quantity", required=True, type=float, help="Sản lượng")
    parser.add_argument("--unit", default="kg", help="Đơn vị, mặc định 'kg'")
    parser.add_argument("--batch-id", dest="batch_id", default=None, help="Mã mẻ, để trống sẽ tự sinh")
    parser.add_argument("--note", default="", help="Ghi chú thêm")
    args = parser.parse_args()

    row = add_batch(
        date_str=args.date,
        product=args.product,
        quantity=args.quantity,
        unit=args.unit,
        batch_id=args.batch_id,
        note=args.note,
    )

    print(f"Đã ghi mẻ {row['batch_id']}: {row['product']} - {row['quantity']}{row['unit']} ngày {row['date']}")


if __name__ == "__main__":
    main()
