---
name: rut-kinh-nghiem
description: Rút bài học từ phiên làm việc hiện tại (lần người dùng sửa lại cách làm, lỗi đã gỡ, quy trình lặp lại) và lưu vào bộ nhớ dự án có chấm độ tin cậy, để các phiên sau không lặp lại lỗi cũ. Dùng khi người dùng gõ /rut-kinh-nghiem, nói "lưu bài học", "nhớ cái này cho lần sau", hoặc khi hook nhắc /compact và vừa xong một giai đoạn.
---

# Rút kinh nghiệm phiên làm việc

Bản rút gọn, chạy thủ công của `continuous-learning-v2` trong ECC (github.com/affaan-m/ECC, MIT).
Bản gốc cần tiến trình nền theo dõi mọi lệnh — không sống được trên Windows thường — nên ở đây
Claude tự rà lại phiên khi được gọi, và ghi vào hệ thống bộ nhớ sẵn có (thư mục `memory/` của dự
án, đường dẫn nằm trong system prompt mục "Memory") thay vì kho riêng của ECC.

## Bước 1 — Rà phiên, chỉ nhặt 4 loại tín hiệu

| Loại | Ví dụ | Độ tin cậy khởi điểm |
|---|---|---|
| Người dùng **sửa lại** cách làm của Claude | "không, đừng tạo file mới, sửa file cũ" | 0.7 |
| Lỗi đã **gỡ xong** và nguyên nhân gốc đã rõ | `py` trỏ vào đường dẫn Python đã mất → dùng `C:/Users/Admin/AppData/Local/Python/bin/python.exe` | 0.6 |
| Cách làm người dùng **xác nhận là đúng** (không sửa, còn khen/duyệt) | "đúng rồi, cứ làm vậy" | 0.5 |
| Quy trình **lặp lại** ≥2 lần trong phiên | cùng chuỗi lệnh kiểm tra trước deploy | 0.4 |

Bỏ qua: lỗi gõ phím, việc chỉ làm một lần, sự cố tạm thời của dịch vụ ngoài, và mọi thứ đã có
sẵn trong code / git log / CLAUDE.md / AGENTS.md (đọc được thì không cần nhớ).

## Bước 2 — Đối chiếu bộ nhớ hiện có

Đọc `MEMORY.md` và các file liên quan trước khi ghi:
- Đã có bài học tương tự → **cập nhật file đó**, tăng `confidence` thêm 0.1 (tối đa 0.9), thêm dòng
  bằng chứng mới có ngày tuyệt đối. Không tạo file trùng.
- Bài học mới **mâu thuẫn** với file cũ → hỏi người dùng cái nào đúng, rồi sửa/xoá file sai.
- Chưa có → tạo file mới.

## Bước 3 — Ghi theo đúng định dạng bộ nhớ của dự án

```markdown
---
name: <slug-ngan>
description: <1 dòng, dùng để quyết định khi nào nhớ lại>
metadata:
  type: feedback | project | reference
  confidence: 0.6
---

<bài học, 1 ý duy nhất>

**Why:** <vì sao — sự việc cụ thể, ngày YYYY-MM-DD>
**How to apply:** <khi nào/ở đâu áp dụng>
```

Thêm 1 dòng trỏ tới file vào `MEMORY.md`. Mỗi file chỉ 1 bài học ("nguyên tử" như instinct của ECC).

## Bước 4 — Báo lại người dùng

Liệt kê ngắn gọn: bài học mới / bài học được củng cố (độ tin cậy cũ → mới) / thứ đã bỏ qua và lý do.
Tối đa 5 bài học mỗi lần — ít mà chắc hơn nhiều mà nhiễu. Nếu phiên không có gì đáng nhớ, nói thẳng
là không có, đừng ghi cho có.
