@echo off
REM Chay bao cao doanh thu/ton kho (7 ngay) + khach quen + han chot/canh bao/khach can nhan lai,
REM gop vao 1 file, roi mo Notepad - Task Scheduler chay ngam, khong tu hien thong bao gi neu
REM khong lam vay. Them muc nhac-viec 2026-10-01 de ban tin tuan (push) co cung tin hieu voi
REM tab "Tong quan" trong app (pull), khong can nho mo app moi thay han chot/khach can nhan.
cd /d "%~dp0.."
set PY="C:\Users\Admin\AppData\Local\Python\bin\python.exe"
> "BAO_CAO_TUAN.txt" (
    %PY% scripts\weekly_report.py --nhac-viec
    echo.
    echo ================================
    echo.
    %PY% scripts\weekly_report.py --days 7
    echo.
    echo ================================
    echo.
    %PY% scripts\weekly_report.py --khach-quen
)
start "" notepad.exe "BAO_CAO_TUAN.txt"
