@echo off
REM Chay next_social_post.py, ghi ket qua ra file, roi mo Notepad de chac chan nguoi dung thay -
REM Task Scheduler chay ngam, khong tu hien thong bao gi neu khong lam vay.
cd /d "%~dp0.."
"C:\Users\Admin\AppData\Local\Python\bin\python.exe" scripts\next_social_post.py > "BAI_DANG_HOM_NAY.txt" 2>&1
start "" notepad.exe "BAI_DANG_HOM_NAY.txt"
