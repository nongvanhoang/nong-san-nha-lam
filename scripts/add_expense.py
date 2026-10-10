#!/usr/bin/env python3
"""Ghi một khoản chi phí mới vào data/expenses.csv."""
import argparse
import sys
from datetime import date

from nsn_core import EXPENSE_CATEGORIES, EXPENSE_CATEGORY_LABELS, add_expense

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Ghi khoản chi phí mới")
    parser.add_argument("--date", default=date.today().isoformat(), help="Ngày chi (YYYY-MM-DD), mặc định hôm nay")
    parser.add_argument("--category", required=True, choices=EXPENSE_CATEGORIES, help="Hạng mục chi phí")
    parser.add_argument("--amount", required=True, type=float, help="Số tiền (VNĐ)")
    parser.add_argument("--note", default="", help="Ghi chú thêm (VD: tên xưởng in, số lượng)")
    args = parser.parse_args()

    row = add_expense(
        date_str=args.date,
        category=args.category,
        amount=args.amount,
        note=args.note,
    )

    label = EXPENSE_CATEGORY_LABELS.get(row["category"], row["category"])
    print(f"Đã ghi chi phí: {label} - {row['amount_vnd']:,.0f} VNĐ ({row['date']})" + (f" - {row['note']}" if row['note'] else ""))


if __name__ == "__main__":
    main()
