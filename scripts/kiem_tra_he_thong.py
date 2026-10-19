#!/usr/bin/env python3
"""Kiểm tra sức khoẻ toàn bộ hệ thống tự động của dự án — gộp SOP.md mục 11 (kiểm tra hàng
tháng) thành 1 lệnh duy nhất thay vì phải tự nhớ kiểm tra từng phần.

Chạy: python scripts/kiem_tra_he_thong.py
"""
import json
import os
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

from nsn_core import (
    B2B_CSV,
    BASE_DIR,
    CUSTOMERS_CSV,
    DATA_DIR,
    EXPENSES_CSV,
    ORDERS_CSV,
    POSTED_LOG_CSV,
    PRODUCTION_CSV,
    PRODUCTS_JSON,
    TARGETS_JSON,
    find_upcoming_deadlines,
    load_rows,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SOCIAL_QUEUE_JSON = DATA_DIR / "social_queue.json"
SOCIAL_QUEUE_STATE_JSON = DATA_DIR / "social_queue_state.json"
SCHEDULED_TASKS = ["NongSanNhaLam_SocialReminder", "NongSanNhaLam_WeeklyDigest"]

# File dự án tự ghi ra có thể chứa dữ liệu khách hàng/kinh doanh thật (tên, SĐT, địa chỉ, doanh
# thu/chi phí) - PHẢI nằm trong .gitignore, không được lọt lên repo public. Chỉ gồm các file do
# nsn_core.py quản lý (phạm vi code chịu trách nhiệm trực tiếp), không phải audit toàn bộ .gitignore.
SENSITIVE_PATHS = [ORDERS_CSV, PRODUCTION_CSV, POSTED_LOG_CSV, EXPENSES_CSV, CUSTOMERS_CSV, B2B_CSV, TARGETS_JSON]
BACKUP_CHECK_FILES = [ORDERS_CSV, PRODUCTION_CSV, EXPENSES_CSV, CUSTOMERS_CSV, PRODUCTS_JSON, B2B_CSV]

_counts = {"ok": 0, "warn": 0, "err": 0}


def status(label, ok, detail=""):
    if ok is True:
        tag, key = "✅", "ok"
    elif ok is None:
        tag, key = "⚠️", "warn"
    else:
        tag, key = "❌", "err"
    _counts[key] += 1
    print(f"{tag} {label}" + (f" — {detail}" if detail else ""))


def check_scheduled_tasks():
    print("\n-- Lịch tự động (Windows Task Scheduler) --")
    for name in SCHEDULED_TASKS:
        try:
            result = subprocess.run(
                ["schtasks", "/query", "/tn", name, "/fo", "LIST"],
                capture_output=True, text=True, timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            status(name, False, f"không chạy được schtasks ({exc})")
            continue
        if result.returncode != 0:
            status(name, False, "KHÔNG TÌM THẤY — task đã bị xoá hoặc chưa tạo, xem CLAUDE.md để tạo lại")
            continue
        output = result.stdout
        if "Disabled" in output or "Đã tắt" in output:
            status(name, None, f"đang bị TẮT — bật lại bằng 'schtasks /change /tn {name} /enable'")
        else:
            status(name, True, "đang chạy")


def check_social_queue():
    print("\n-- Hàng đợi đăng bài --")
    if not SOCIAL_QUEUE_JSON.exists() or not SOCIAL_QUEUE_STATE_JSON.exists():
        status("Hàng đợi đăng bài", False, "thiếu file social_queue.json/social_queue_state.json")
        return
    try:
        with SOCIAL_QUEUE_JSON.open(encoding="utf-8") as f:
            queue = json.load(f)["items"]
        with SOCIAL_QUEUE_STATE_JSON.open(encoding="utf-8") as f:
            state = json.load(f)
    except (json.JSONDecodeError, KeyError) as exc:
        status("Hàng đợi đăng bài", False, f"file lỗi định dạng: {exc}")
        return

    remaining = len(queue) - state["next_index"]
    if remaining <= 0:
        status("Hàng đợi đăng bài", False, "ĐÃ HẾT — báo Claude soạn thêm mục mới vào data/social_queue.json")
        return
    days_left = remaining * 3
    run_out_date = date.today() + timedelta(days=days_left)
    detail = f"còn {remaining} mục (~{days_left} ngày, hết khoảng {run_out_date.isoformat()})"
    if days_left <= 7:
        status("Hàng đợi đăng bài", None, detail + " — sắp hết, nên soạn thêm")
    else:
        status("Hàng đợi đăng bài", True, detail)


def check_data_files():
    print("\n-- File dữ liệu (đọc thử, phát hiện lỗi định dạng sớm) --")
    csv_files = {
        "orders.csv": ORDERS_CSV,
        "production_log.csv": PRODUCTION_CSV,
        "expenses.csv": EXPENSES_CSV,
        "DANH_SACH_KHACH_HANG_B2B.csv": B2B_CSV,
    }
    for name, path in csv_files.items():
        if not path.exists():
            status(name, None, "chưa có file (bình thường nếu chưa ghi dòng nào)")
            continue
        try:
            rows = load_rows(path)
            status(name, True, f"{len(rows)} dòng, đọc OK")
        except Exception as exc:  # noqa: BLE001 - muốn bắt mọi lỗi đọc file để báo rõ, không crash cả script
            status(name, False, f"LỖI đọc file: {exc}")

    json_files = {"products.json": PRODUCTS_JSON, "muc_tieu.json": TARGETS_JSON}
    for name, path in json_files.items():
        if not path.exists():
            status(name, False, "thiếu file")
            continue
        try:
            with path.open(encoding="utf-8") as f:
                json.load(f)
            status(name, True, "đọc OK")
        except json.JSONDecodeError as exc:
            status(name, False, f"LỖI định dạng JSON: {exc}")


def check_git_safety():
    """Xác nhận mọi file có thể chứa dữ liệu khách hàng/kinh doanh thật đều nằm trong
    .gitignore — phòng sự cố lặp lại kiểu DANH_SACH_KHACH_HANG_B2B.csv từng lỡ public
    (phát hiện 2026-09-06) hoặc data/customers.csv suýt lặp lại (phát hiện 2026-10-02)."""
    print("\n-- An toàn git (file nhạy cảm có nằm trong .gitignore không) --")
    for path in SENSITIVE_PATHS:
        if not path.exists():
            continue  # chưa có file thì chưa có gì để lộ, bỏ qua
        try:
            result = subprocess.run(
                ["git", "check-ignore", "-q", str(path)],
                cwd=BASE_DIR, capture_output=True, timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            status(path.name, None, f"không kiểm tra được git ({exc})")
            continue
        rel = path.relative_to(BASE_DIR)
        if result.returncode == 0:
            status(str(rel), True, "đã gitignore")
        elif result.returncode == 1:
            status(str(rel), False, "CHƯA gitignore — có nguy cơ lộ dữ liệu thật nếu git add, thêm ngay vào .gitignore")
        else:
            status(str(rel), None, "không kiểm tra được (có thể không ở trong git repo)")


def check_backup():
    print("\n-- Backup OneDrive --")
    onedrive = os.environ.get("OneDrive") or os.environ.get("ONEDRIVE")
    if not onedrive:
        status("Backup OneDrive", None, "máy này không có biến môi trường OneDrive — dữ liệu chỉ có 1 bản duy nhất, không có backup tự động")
        return
    backup_latest = Path(onedrive) / "NongSanNhaLam-Backup" / "latest"
    if not backup_latest.exists():
        status("Backup OneDrive", None, f"chưa có thư mục {backup_latest} — chưa từng ghi đơn/chi phí nào để kích hoạt backup")
        return
    missing = [p.name for p in BACKUP_CHECK_FILES if p.exists() and not (backup_latest / p.name).exists()]
    if missing:
        status("Backup OneDrive", False, f"CÓ FILE THẬT nhưng CHƯA có bản backup: {', '.join(missing)}")
    else:
        status("Backup OneDrive", True, f"đủ bản sao cho mọi file dữ liệu đang có ({backup_latest})")


def check_targets():
    print("\n-- Mục tiêu tăng trưởng --")
    if not TARGETS_JSON.exists():
        status("Mục tiêu tháng", None, "chưa có file data/muc_tieu.json")
        return
    with TARGETS_JSON.open(encoding="utf-8") as f:
        targets = json.load(f)
    if not targets.get("doanh_thu_thang_vnd") and not targets.get("loi_nhuan_thang_vnd"):
        status("Mục tiêu tháng", None, "chưa đặt số nào — xem HE_THONG_VAN_HANH_1_NGUOI.md mục 3 nếu muốn đặt")
    else:
        status("Mục tiêu tháng", True, "đã đặt ít nhất 1 mục tiêu")


def check_deadlines():
    print("\n-- Hạn chót đang theo dõi (từ VIEC_CAN_LAM.md) --")
    deadlines = find_upcoming_deadlines()
    if not deadlines:
        status("Hạn chót", True, "không có hạn chót nào đang treo")
        return
    for d in deadlines:
        if d["days_left"] < 0:
            status(d["title"], False, f"ĐÃ TRỄ {-d['days_left']} ngày")
        elif d["days_left"] <= 7:
            status(d["title"], None, f"còn {d['days_left']} ngày — sắp tới hạn")
        else:
            status(d["title"], True, f"còn {d['days_left']} ngày")


def main():
    print("=== KIỂM TRA SỨC KHOẺ HỆ THỐNG — Thế Hưng Organic ===")
    print(f"(chạy lúc {datetime.now().strftime('%Y-%m-%d %H:%M')})")

    check_scheduled_tasks()
    check_social_queue()
    check_data_files()
    check_git_safety()
    check_backup()
    check_targets()
    check_deadlines()

    print(f"\n=== TỔNG KẾT: {_counts['ok']} OK, {_counts['warn']} cần chú ý, {_counts['err']} LỖI ===")
    if _counts["err"]:
        print("Có lỗi thật cần xử lý trước — xem các dòng ❌ ở trên.")
    elif _counts["warn"]:
        print("Không có lỗi nặng, nhưng có vài điểm nên xử lý sớm (dòng ⚠️).")
    else:
        print("Mọi thứ đang chạy ổn.")


if __name__ == "__main__":
    main()
