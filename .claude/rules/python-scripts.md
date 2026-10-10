---
paths:
  - "**/*.py"
---
# Quy tắc khi viết/sửa script Python trong dự án này

Rút gọn từ bộ `rules/python` của ECC (github.com/affaan-m/ECC, MIT), bỏ phần không hợp (ép black/mypy,
đổi print sang logging) và thêm các bài học thật của máy này.

- **Chạy Python bằng** `C:/Users/Admin/AppData/Local/Python/bin/python.exe` (hoặc `.venv/Scripts/python.exe`
  nếu dự án có). Lệnh `py` đang trỏ vào một đường dẫn đã mất trên ổ E:, `python`/`python3` là shim
  Microsoft Store — cả hai đều hỏng.
- **Khoá bí mật** (API key, OAuth token, client_secret) đọc từ biến môi trường hoặc file đã nằm trong
  `.gitignore`. Trước khi tạo file token/secret mới, kiểm tra `git check-ignore -v <file>` trước.
- **Tiếng Việt / Windows**: mở file luôn kèm `encoding="utf-8"`; script in ra tiếng Việt thì gọi
  `sys.stdout.reconfigure(encoding="utf-8")` — không thì cp1252 làm lỗi hoặc mất chữ.
- **Script sửa hàng loạt file HTML** (generate_*, inject_*, update_*): chạy thử trên 1 file trước,
  sau khi chạy luôn xem `git diff --stat` và soát các đoạn thêm tay (GTM, AdSense) có bị ghi đè không.
- **Diff tối thiểu**: sửa đúng chỗ cần sửa, không format lại cả file, không đổi tên hàng loạt khi không được yêu cầu.
- **Chỉ dùng thư viện chuẩn** trừ khi dự án đã có sẵn thư viện đó; muốn thêm thư viện mới thì hỏi trước.
