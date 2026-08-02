#!/usr/bin/env python3
"""In báo cáo doanh thu và sản lượng trong N ngày gần nhất (mặc định 7 ngày)."""
import argparse
import sys

from nsn_core import compute_report

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Báo cáo doanh thu/sản lượng theo khoảng ngày")
    parser.add_argument("--days", type=int, default=7, help="Số ngày gần nhất để tính, mặc định 7")
    args = parser.parse_args()

    report = compute_report(args.days)

    print(f"=== BÁO CÁO {report['days']} NGÀY GẦN NHẤT (từ {report['since']}) ===\n")

    print("-- Doanh thu theo sản phẩm --")
    if not report["revenue_by_product"]:
        print("  (chưa có đơn hàng nào trong khoảng thời gian này)")
    else:
        for item in report["revenue_by_product"]:
            print(f"  {item['product']}: {item['qty']:g} đơn vị, {item['revenue']:,.0f} VNĐ")
        print(f"  TỔNG DOANH THU: {report['total_revenue']:,.0f} VNĐ ({report['order_count']} đơn)")

        print("\n-- Doanh thu theo kênh --")
        for item in report["revenue_by_channel"]:
            print(f"  {item['channel']}: {item['revenue']:,.0f} VNĐ")

    print("\n-- Sản lượng sản xuất/thu hoạch --")
    if not report["production"]:
        print("  (chưa có mẻ sản xuất/thu hoạch nào trong khoảng thời gian này)")
    else:
        for item in report["production"]:
            print(f"  {item['product']}: {item['qty']:g} đơn vị")

    print("\n-- Tồn kho ước tính (tổng sản xuất trừ tổng đã bán, TOÀN THỜI GIAN) --")
    if not report["inventory"]:
        print("  (chưa có dữ liệu sản xuất/đơn hàng)")
    else:
        for item in report["inventory"]:
            warning = f"  ⚠️ {item['warning']}" if item["warning"] else ""
            print(f"  {item['product']}: còn {item['remaining']:g} đơn vị (đã làm {item['produced']:g}, đã bán {item['sold']:g}){warning}")
        print("\n  (Lưu ý: số này chỉ đúng nếu luôn ghi số lượng cùng đơn vị, ví dụ luôn quy ra kg)")


if __name__ == "__main__":
    main()
