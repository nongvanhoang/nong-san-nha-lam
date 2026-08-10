# Hướng Dẫn Gắn Google Search Console Cho Web Mới (nongsannhalam.com)

_Thêm 2026-08-11, ngay sau khi đổi sang domain riêng (10/08) — cần khai báo lại với Google càng
sớm càng tốt để không mất công Google phải "tìm lại" web, và để nhà mình xem được có bao nhiêu
người tìm thấy web qua Google._

## Việc bạn tự làm (cần đăng nhập Gmail của nhà mình, tôi không đăng nhập thay được)

1. Vào trang **search.google.com/search-console**, đăng nhập bằng Gmail của nhà mình.
2. Bấm **"Thêm property"** (Add property) → chọn loại **"URL prefix"** (không chọn loại "Domain")
   → nhập đúng: `https://nongsannhalam.com/`
3. Google sẽ hỏi cách xác minh quyền sở hữu — chọn 1 trong 2 cách dễ nhất dưới đây, rồi **dừng lại,
   gửi cho tôi** thứ Google đưa ra (đừng bấm "Xác minh" vội, vì web chưa có mã đó):
   - **Cách A — Thẻ HTML (khuyên dùng)**: Google đưa 1 dòng mã dạng
     `<meta name="google-site-verification" content="xxxxxxxx" />` — copy nguyên dòng đó gửi cho tôi.
   - **Cách B — Tệp HTML**: Google cho tải về 1 file tên dạng `google1234567890.html` — gửi file đó
     (hoặc mở ra copy nguyên nội dung bên trong) cho tôi.
4. Sau khi tôi báo đã đưa mã lên web thật (xem mục dưới), quay lại Search Console bấm **"Xác minh"**.
5. Xác minh xong, vào mục **"Sơ đồ trang web"** (Sitemaps) ở cột trái, ô nhập gõ đúng: `sitemap.xml`
   rồi bấm **Gửi** (Google tự ghép thành `https://nongsannhalam.com/sitemap.xml`).

## Việc tôi làm (khi bạn gửi mã ở Bước 3)

- Dán mã xác minh vào đúng vị trí trong web (`docs/index.html` nếu là thẻ HTML, hoặc thêm file vào
  `docs/` nếu là tệp HTML), đẩy lên GitHub — web thật cập nhật sau vài phút, lúc đó nhắn lại để bạn
  bấm "Xác minh" ở Bước 4.

## Sau khi xong

Vài ngày sau có thể vào lại Search Console xem mục "Hiệu suất" (Performance) để biết có bao nhiêu
lượt tìm thấy web qua Google, từ khoá nào khách hay gõ — hữu ích để biết nên viết thêm nội dung gì.
