@echo off
REM Bam dup lan file nay de mo app quan ly Nong San Nha Lam.
REM Neu sau nay cai lai Python o duong dan khac, sua dong PYTHON_EXE ben duoi.

set PYTHON_EXE=C:\Users\Admin\AppData\Local\Python\bin\python.exe
cd /d "%~dp0"

if not exist "%PYTHON_EXE%" (
  echo Khong tim thay Python o: %PYTHON_EXE%
  echo Mo CLAUDE.md de xem huong dan, hoac nho Claude Code kiem tra lai.
  pause
  exit /b 1
)

"%PYTHON_EXE%" scripts\webapp.py
pause
