# Ảnh cho các kênh và sàn: dùng file nào ở đâu (cập nhật 25-10-2026)

Tất cả ảnh dùng chung một phong cách: ảnh thật của vườn và nương làm nền tối, chữ có chân, điểm nhấn vàng, logo tròn.
Để làm lại toàn bộ ảnh, chạy:
`C:/Users/Admin/AppData/Local/Python/bin/python.exe content/kenh_assets/banner/make_banners.py`

Giá trên ảnh được lấy tự động từ `data/products.json`, số đánh giá lấy từ `data/testimonials.json`. Khi đổi giá, chỉ cần chạy lại lệnh trên.

| Kênh | Chỗ tải lên | File |
|---|---|---|
| Mọi kênh | Ảnh đại diện | `logo-tron/logo-tron-day-du-1080.png` (Facebook, Zalo, YouTube) hoặc `logo-tron-vien-1080.png` (Shopee, TikTok, Instagram) |
| Facebook | Ảnh bìa | `banner/bia-facebook-1640x624.png` |
| Zalo | Ảnh bìa | `banner/bia-zalo-1280x720.png` (chữ nằm giữa vì Zalo cắt ảnh khác nhau trên mỗi máy) |
| YouTube | Ảnh bìa kênh | `banner/bia-youtube-2560x1440.png` |
| Shopee | Ảnh bìa shop | `banner/banner-shopee-1200x600.png` |
| Shopee | Banner vòng xoay (trang trí shop) | `banner/shopee-vong-xoay-1-2000x1000.png`, `-2-2000x1000.png` |
| TikTok Shop | Banner gian hàng | Chưa xác minh được khổ chuẩn. Thử dùng ảnh Shopee 1200×600 hoặc 2000×1000, rồi kiểm tra lại trong Seller Center |
| Facebook / Instagram | Bài đăng | `banner/qc-vuong-san-day-1080.png` (vuông), `banner/bai-doc-san-day-1080x1350.png` (dọc 4:5) |
| Facebook / Instagram / Zalo / TikTok | Story, Reels | `banner/story-cam-dat-truoc-1080x1920.png`, `banner/story-qua-tet-1080x1920.png` |
| Website | Ảnh hiện khi chia sẻ link | `banner/og-share-1200x630.png`, đã chép thành `docs/assets/home/og-share.jpg` |

Lưu ý:
- Ảnh có giá Quà Tết đang ghi "Nhắn báo giá" vì chưa chốt giá. Khi có giá, sửa chữ trong `make_banners.py`.
- **Ảnh cam đặt trước chỉ đăng khi đã nhận đặt trước thật.** Khi đã hết mùa thì không đăng.
- Thư mục `cu-khong-dung/` chứa ảnh kiểu cũ, không dùng nữa.
