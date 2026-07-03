# Nông Sản Nhà Làm

Dự án hỗ trợ kinh doanh nông sản gia đình: Tinh Bột Sắn Dây (bán quanh năm) và
Cam Đường Canh (theo mùa, ~tháng 11 âm lịch - tháng 1). Mở Claude Code trong thư mục
này để nhờ giúp việc — Claude đã có sẵn ngữ cảnh sản phẩm/giá/tông giọng trong `CLAUDE.md`.

## Website đang chạy

https://nongvanhoang.github.io/nong-san-nha-lam/ (cập nhật tự động mỗi khi push lên `main`)

## Cách dùng hàng ngày (không cần biết code)

Cứ mở Claude Code trong thư mục `NongSanNhaLam` rồi gõ yêu cầu bằng tiếng Việt bình thường, ví dụ:

- "Viết giúp caption Facebook giới thiệu mẻ tinh bột sắn dây mới"
- "Ghi giúp đơn hàng: chị Lan mua 2kg tinh bột sắn dây, 150k/kg, đặt qua Zalo"
- "Ghi giúp mẻ sản xuất hôm nay: 10kg tinh bột sắn dây"
- "Tính giúp doanh thu tuần này"
- "Cập nhật giá tinh bột sắn dây túi 1kg thành 160k"

Claude sẽ tự chạy script hoặc sửa file phù hợp.

## Cấu trúc thư mục

- `CLAUDE.md` — ngữ cảnh dự án cho Claude (sản phẩm, giá, tông giọng, quy tắc)
- `data/products.json` — bảng giá và thông tin sản phẩm (sửa khi có giá thật)
- `data/orders.csv` — sổ đơn hàng
- `data/production_log.csv` — sổ sản xuất/thu hoạch
- `content/templates/` — mẫu caption theo từng kênh (Facebook, Zalo, Shopee/TikTok)
- `content/posts_ready.md` — nơi lưu các caption đã soạn, chờ đăng tay
- `scripts/` — script Python nhẹ, chạy bằng `python scripts/<ten_file>.py --help`
- `docs/` — trang giới thiệu tĩnh (`index.html` + `styles.css`), mở trực tiếp bằng trình duyệt

## Ảnh trên website hiện tại

`docs/assets/` đang dùng 3 ảnh minh hoạ tải từ Wikimedia Commons (giấy phép rõ ràng, xem
`docs/assets/CREDITS.md`) — KHÔNG phải ảnh sản phẩm/vườn thật của nhà mình. Khi có ảnh/video
thật (chụp mẻ sắn dây, vườn cam nhà mình), đưa vào `docs/assets/`, xoá 3 file `*-stock.jpg`
và nhờ Claude thay vào `index.html` — càng sớm càng tốt vì ảnh thật tăng độ tin cậy với khách
hơn nhiều so với ảnh minh hoạ.

## Việc còn cần bạn làm

1. **Thay ảnh minh hoạ bằng ảnh/video thật** khi có (xem mục trên)
2. **Link Facebook** — hiện đang tạm ẩn (comment) trong `docs/index.html` và để
   `"CẦN CẬP NHẬT"` trong `data/products.json`. Khi có link, nhờ Claude bật lại giúp.
3. Giá, số Zalo (0979 502 000), khu vực giao hàng (toàn quốc) đã cập nhật đầy đủ.
4. Đã có sẵn 5 caption mẫu dùng số liệu thật trong `content/posts_ready.md`, sẵn sàng copy đăng.

## Giới hạn hiện tại (cố tình, để tránh rủi ro/chi phí)

- Không tự động đăng bài lên Facebook/Zalo/Shopee/TikTok Shop — các sàn này chống bot khá gắt,
  tự động hoá dễ bị khoá tài khoản. Nội dung do Claude soạn, bạn tự đăng tay.
- Không dùng API AI trả phí riêng — mọi nội dung do Claude Code tạo ngay trong phiên chat.
- **Không tự tạo/tải video** — Claude Code không có công cụ tạo video hay tải video kho miễn phí
  hàng loạt (các kho như Pexels/Pixabay Videos cần bạn vào web tải tay, hoặc cần API trả phí).
  Cách tốt nhất cho thương hiệu "nhà làm" vẫn là video/ảnh tự quay thật — chân thực hơn stock nhiều.
- Website đã deploy qua GitHub Pages tại repo public
  [github.com/nongvanhoang/nong-san-nha-lam](https://github.com/nongvanhoang/nong-san-nha-lam).
  Link website: xem mục "Website đang chạy" phía trên. Mỗi lần push code mới lên `main`,
  trang tự cập nhật sau vài phút. Lưu ý: giá và số Zalo trên trang này công khai với mọi người.
