#!/usr/bin/env python3
"""In báo cáo doanh thu và sản lượng trong N ngày gần nhất (mặc định 7 ngày)."""
import argparse
import sys

from nsn_core import (
    compute_report,
    compute_repeat_customers,
    compute_month_to_date,
    find_upcoming_deadlines,
    find_customers_to_followup,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Báo cáo doanh thu/sản lượng theo khoảng ngày")
    parser.add_argument("--days", type=int, default=7, help="Số ngày gần nhất để tính, mặc định 7")
    parser.add_argument("--khach-quen", action="store_true", help="Chỉ in danh sách khách mua từ 2 lần trở lên (toàn thời gian), bỏ qua báo cáo theo ngày")
    parser.add_argument("--min-don", type=int, default=2, help="Số đơn tối thiểu để tính là khách quen, mặc định 2 (dùng cùng --khach-quen)")
    parser.add_argument("--thang-nay", action="store_true", help="Chỉ in doanh thu/chi phí/lãi lỗ từ đầu tháng dương lịch đến hôm nay, đối chiếu mục tiêu trong data/muc_tieu.json")
    parser.add_argument("--nhac-viec", action="store_true", help="Chỉ in hạn chót sắp tới + cảnh báo tồn kho + khách quen lâu chưa quay lại (phần không phải tài chính của tab Tổng quan) - dùng cho bản tin tuần tự động")
    args = parser.parse_args()

    if args.nhac_viec:
        deadlines = find_upcoming_deadlines()
        print("=== HẠN CHÓT ĐANG THEO DÕI (từ VIEC_CAN_LAM.md) ===\n")
        if not deadlines:
            print("  (không có hạn chót nào đang theo dõi)")
        else:
            for d in deadlines:
                tag = f"TRỄ {-d['days_left']} NGÀY" if d["days_left"] < 0 else f"còn {d['days_left']} ngày"
                print(f"  [{tag}] {d['title']} (hạn {d['deadline']})")

        print("\n=== CẢNH BÁO TỒN KHO (toàn thời gian) ===\n")
        inventory = compute_report(1)["inventory"]
        warnings = [i for i in inventory if i["warning"]]
        if not warnings:
            print("  (không có cảnh báo nào)")
        else:
            for i in warnings:
                print(f"  ⚠️ {i['product']}: {i['warning']} (còn {i['remaining']:g})")

        print("\n=== KHÁCH QUEN LÂU CHƯA QUAY LẠI (từ 21 ngày) ===\n")
        followups = find_customers_to_followup()
        if not followups:
            print("  (không có khách nào đang chờ nhắn lại, hoặc chưa đủ dữ liệu đơn hàng)")
        else:
            for c in followups:
                print(f"  {c['customer']}: {c['days_since_last_order']} ngày chưa mua lại "
                      f"({c['order_count']} đơn trước, mua {', '.join(c['products'])})")
            print("\n  Mẫu nhắn lại: content/templates/nhan_tin_truc_tiep.md (Mẫu 2)")
        return

    if args.thang_nay:
        m = compute_month_to_date()
        print(f"=== THÁNG {m['month']} (từ {m['since']} đến hôm nay) ===\n")
        print(f"  Doanh thu: {m['revenue']:,.0f} VNĐ")
        print(f"  Chi phí:   {m['expenses']:,.0f} VNĐ")
        print(f"  Lãi/lỗ:    {m['profit']:,.0f} VNĐ")
        if m["target_revenue"]:
            pct = m["revenue"] / m["target_revenue"] * 100
            print(f"\n  Mục tiêu doanh thu tháng: {m['target_revenue']:,.0f} VNĐ — đã đạt {pct:.0f}%")
        if m["target_profit"]:
            pct = m["profit"] / m["target_profit"] * 100
            print(f"  Mục tiêu lợi nhuận tháng: {m['target_profit']:,.0f} VNĐ — đã đạt {pct:.0f}%")
        if not m["target_revenue"] and not m["target_profit"]:
            print("\n  (Chưa đặt mục tiêu tháng — xem data/muc_tieu.json)")
        return

    if args.khach_quen:
        khach_quen = compute_repeat_customers(args.min_don)
        print(f"=== KHÁCH QUEN (từ {args.min_don} đơn trở lên, toàn thời gian) ===\n")
        if not khach_quen:
            print("  (chưa có khách nào đủ điều kiện — hoặc chưa có đơn hàng nào được ghi sổ)")
        else:
            for c in khach_quen:
                print(f"  {c['customer']}: {c['order_count']} đơn, {c['total_revenue']:,.0f} VNĐ, "
                      f"mua {', '.join(c['products'])}, lần gần nhất {c['last_date']}")
        return

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

    print("\n-- Chi phí --")
    if not report["expenses_by_category"]:
        print("  (chưa ghi chi phí nào trong khoảng thời gian này)")
    else:
        for item in report["expenses_by_category"]:
            print(f"  {item['label']}: {item['amount']:,.0f} VNĐ")
        print(f"  TỔNG CHI PHÍ: {report['total_expenses']:,.0f} VNĐ")

    print(f"\n-- Lãi/lỗ trong kỳ: {report['profit']:,.0f} VNĐ --")

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
