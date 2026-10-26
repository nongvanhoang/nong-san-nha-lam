# Báo Google: web đã chuyển từ nongsannhalam.com sang thehungorganic.com

_Cập nhật 2026-10-26, ngay sau khi chuyển tên miền. Làm sớm để Google chuyển thứ hạng cũ sang tên miền mới,
không phải "tìm lại từ đầu". Khoảng 15 phút. Phải đăng nhập Gmail nhà mình nên Claude không làm thay được._

Đăng nhập **đúng Gmail đã dùng cho Search Console của nongsannhalam.com** (Gmail đó đang giữ mã xác minh).

## Bước 1: Thêm tên miền mới (khoảng 2 phút)

1. Vào **search.google.com/search-console**.
2. Bấm vào tên web ở góc trái trên, chọn **"+ Thêm tài sản"** (Add property).
3. Chọn ô bên phải **"Tiền tố URL"** (URL prefix), gõ đúng:
   `https://thehungorganic.com/`
   rồi bấm **Tiếp tục**.
4. Google thường **tự xác minh luôn**, vì web mới vẫn giữ nguyên mã xác minh cũ trong trang chủ.
   Nếu Google hỏi cách xác minh, chọn **"Thẻ HTML"** và bấm **Xác minh**. Không cần dán gì thêm, mã đã có sẵn trên web.
   Nếu báo lỗi, chụp màn hình gửi Claude.

## Bước 2: Nộp sơ đồ trang (khoảng 1 phút)

Vẫn ở tài sản **thehungorganic.com**: cột trái bấm **"Sơ đồ trang web"** (Sitemaps), ô nhập gõ `sitemap.xml`, bấm **Gửi**.

## Bước 3: Báo chuyển địa chỉ (khoảng 3 phút)

1. Bấm tên web ở góc trái trên, chọn tài sản cũ **nongsannhalam.com**.
2. Cột trái, dưới cùng bấm **Cài đặt** (Settings), rồi **"Thay đổi địa chỉ"** (Change of address).
3. Chọn trang web mới **thehungorganic.com**, bấm **Xác thực và cập nhật** (Validate & update).
4. Google sẽ tự kiểm tra việc chuyển hướng 301 (đã cài trên Cloudflare). Thấy dấu tích xanh thì bấm **Xác nhận chuyển**.
   Nếu báo lỗi, chụp màn hình gửi Claude.

## Sau khi xong

- Giữ nguyên quy tắc chuyển hướng trên Cloudflare và **gia hạn nongsannhalam.com ít nhất 1 năm nữa**.
  Google cần khoảng 180 ngày để chuyển hẳn sang tên miền mới.
- Trong vài tuần đầu, lượt hiển thị có thể chững lại một chút rồi chuyển dần sang tên miền mới. Điều này bình thường.
- Khoảng 2 tuần sau, vào tài sản mới, mục **"Hiệu suất"** (Performance), xem khách tìm từ khoá gì để viết thêm nội dung.
