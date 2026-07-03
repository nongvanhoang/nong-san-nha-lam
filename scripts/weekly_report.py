#!/usr/bin/env python3
"""In báo cáo doanh thu và sản lượng trong N ngày gần nhất (mặc định 7 ngày)."""
import argparse
import csv
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
ORDERS_CSV = DATA_DIR / "orders.csv"
PRODUCTION_CSV = DATA_DIR / "production_log.csv"


def parse_date(value: str):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def load_rows(path: Path):
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser(description="Báo cáo doanh thu/sản lượng theo khoảng ngày")
    parser.add_argument("--days", type=int, default=7, help="Số ngày gần nhất để tính, mặc định 7")
    args = parser.parse_args()

    since = date.today() - timedelta(days=args.days)

    orders = [r for r in load_rows(ORDERS_CSV) if (d := parse_date(r["date"])) and d >= since]
    batches = [r for r in load_rows(PRODUCTION_CSV) if (d := parse_date(r["date"])) and d >= since]

    print(f"=== BÁO CÁO {args.days} NGÀY GẦN NHẤT (từ {since.isoformat()}) ===\n")

    print("-- Doanh thu theo sản phẩm --")
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

    if not active_orders:
        print("  (chưa có đơn hàng nào trong khoảng thời gian này)")
    else:
        for product, revenue in sorted(revenue_by_product.items(), key=lambda x: -x[1]):
            print(f"  {product}: {qty_by_product[product]:g} đơn vị, {revenue:,.0f} VNĐ")
        print(f"  TỔNG DOANH THU: {total_revenue:,.0f} VNĐ ({len(active_orders)} đơn)")

        print("\n-- Doanh thu theo kênh --")
        for channel, revenue in sorted(revenue_by_channel.items(), key=lambda x: -x[1]):
            print(f"  {channel}: {revenue:,.0f} VNĐ")

    print("\n-- Sản lượng sản xuất/thu hoạch --")
    qty_produced = defaultdict(float)
    for r in batches:
        qty_produced[r["product"]] += float(r["quantity"])

    if not qty_produced:
        print("  (chưa có mẻ sản xuất/thu hoạch nào trong khoảng thời gian này)")
    else:
        for product, qty in sorted(qty_produced.items(), key=lambda x: -x[1]):
            print(f"  {product}: {qty:g} đơn vị")


if __name__ == "__main__":
    main()
