# Hướng dẫn dùng Canva để làm ảnh/video đẹp hơn

_Thêm 2026-08-14. Claude không đăng nhập được vào Canva của bạn nên không tự làm thay được — đây là
hướng dẫn để bạn tự làm trong Canva (canva.com, có bản miễn phí đủ dùng), làm theo đúng số liệu/màu
sắc dưới đây thì không cần tự nghĩ gì thêm._

⚠️ **Quy tắc quan trọng**: Canva chỉ dùng để **trình bày đẹp hơn** ảnh/video thật đã có (thêm khung,
chữ, bố cục, ghép nhiều ảnh) — **KHÔNG dùng công cụ "AI tạo ảnh" của Canva để vẽ sản phẩm/hình ảnh
giả**. Đúng theo nguyên tắc của nhà mình: chỉ ảnh/video thật, không dàn dựng.

## Bộ nhận diện (copy đúng để đồng bộ với website)

- **Logo**: `docs/assets/logo-transparent.svg` (nền trong suốt, hợp mọi nền màu) hoặc
  `docs/assets/icon-512.png` nếu Canva không nhận file .svg
- **Màu chính**:
  - Đen ngà (chữ/nền tối): `#14100c`
  - Kem/ngà (nền sáng): `#f3ead9`
  - Vàng gold (điểm nhấn): `#c9a227`
  - Vàng gold nhạt: `#e6c878`
  - Xanh lá (phụ): `#6a8256`
- **Font chữ**: Canva có sẵn font `Cambria` — dùng cho tiêu đề để đồng bộ với logo/website (font
  này hiển thị đúng dấu tiếng Việt, các font khác có thể lỗi dấu ắ/ằ/ẳ/ẵ/ặ)

## Mẫu 1 — Ảnh vuông đăng nhóm Facebook sỉ nguyên liệu

- Trong Canva: tìm mẫu có sẵn **"Instagram Post"** hoặc **"Facebook Post"** (kích thước 1080×1080)
- Tải lên 1 trong các ảnh thật: `docs/assets/tinh-bot-san-day-real-01.jpg` hoặc
  `docs/assets/san-day-banhkhonut-real.jpg`
- Đặt logo `docs/assets/logo-transparent.svg` ở góc dưới
- Chữ tiêu đề (copy nguyên): **"TINH BỘT SẮN DÂY THỦ CÔNG — GIÁ SỈ CHO QUÁN CHÈ/TRÀ SỮA/TIỆM BÁNH"**
- Chữ phụ: **"Lạng Sơn · Tự lọc tay · Sấy bằng lò sấy riêng · Không hoá chất"**
- Góc dưới: SĐT/Zalo **0979 502 000**

## Mẫu 2 — Video ngắn ghép cảnh (dùng cho Reels/TikTok/Story Facebook)

- Trong Canva: tìm mẫu **"Instagram Reel"** hoặc **"TikTok Video"** (kích thước dọc 1080×1920)
- Ghép 3-4 đoạn video thật đã có theo đúng thứ tự quy trình (kéo thả vào timeline Canva):
  1. Cảnh thu hoạch — chọn 1 clip trong `Hình Ảnh, Video/Sắn Dây/` nhóm `cutuoi` hoặc dùng sẵn
     `docs/assets/san-day-thu-hoach.mp4`
  2. Cảnh nghiền lọc tay — `docs/assets/san-day-nghienloc-loc-tay.jpg` (ảnh) hoặc video trong nhóm
     `nghienloc`
  3. Cảnh sấy trong lò — `content/video/output/quy-trinh-say-san-day.mp4` (đã có sẵn, có thể cắt
     ngắn lại)
  4. Cảnh sản phẩm thành phẩm — `docs/assets/tinh-bot-san-day-real-01.jpg`
- Nhạc nền: dùng nhạc có sẵn miễn phí bản quyền trong thư viện Canva (mục "Audio"), chọn loại nhẹ
  nhàng/mộc mạc — tránh nhạc có lời hoặc nhạc bản quyền ngoài Canva để không bị gỡ video.
- Chữ overlay từng cảnh (copy nguyên, đừng thêm công dụng chưa xác thực):
  1. "Thu hoạch sắn dây tại Lạng Sơn"
  2. "Lọc tay — không hoá chất, không tẩy trắng"
  3. "Sấy bằng lò sấy riêng — không phơi nắng"
  4. "Tinh Bột Sắn Dây Nhà Làm — 0979 502 000"

## Mẫu 3 — Ảnh bìa Google Business Profile

- Kích thước gợi ý trong Canva: tìm mẫu **"Facebook Cover"** rồi tự chỉnh về 1024×576 (đúng tỉ lệ
  Google Business Profile khuyến nghị)
- Dùng ảnh `docs/assets/san-day-thu-hoach-poster.jpg` (cảnh rễ sắn dây thật rất to, ấn tượng) làm
  nền, đặt logo + tên "Nông Sản Nhà Làm" đè lên góc

## Mẫu 4 — Ảnh cho cửa hàng đặc sản Lạng Sơn (dùng khi mang mẫu đến 211/115 Trần Đăng Ninh)

- Mẫu **"Poster"** khổ A5, in màu tại tiệm photo gần nhà, kẹp cùng túi mẫu sản phẩm khi mang đến
  chào hàng trực tiếp — chuyên nghiệp hơn nói suông
- Nội dung: ảnh sản phẩm + logo + giá tham khảo lấy từ `data/products.json` + SĐT/Zalo

## Sau khi làm xong

Lưu file thiết kế lại trong Canva (không cần tải về máy nếu không cần) để lần sau chỉnh sửa nhanh,
chỉ cần đổi ảnh/giá khi cần — không phải làm lại từ đầu.
