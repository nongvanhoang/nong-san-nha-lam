# Nông Sản Nhà Làm

Dự án hỗ trợ kinh doanh nông sản gia đình: Tinh Bột Sắn Dây (bán quanh năm) và
Cam Đường Canh (theo mùa, ~tháng 11 âm lịch - tháng 1). Mở Claude Code trong thư mục
này để nhờ giúp việc — Claude đã có sẵn ngữ cảnh sản phẩm/giá/tông giọng trong `CLAUDE.md`.

## Website đang chạy

- Tiếng Việt: https://nongsannhalam.com/
- English (cho khách/đối tác xuất khẩu): https://nongsannhalam.com/en/

(cập nhật tự động mỗi khi push lên `main`)

## App quản lý (ghi đơn/mẻ sản xuất/báo cáo/giá) — không cần mở Claude Code

Bấm đúp file **`MO_APP_QUAN_LY.bat`** ở gốc thư mục dự án — app tự mở trên trình duyệt tại
`http://127.0.0.1:8943/`. Có 4 mục: Ghi đơn hàng, Ghi mẻ sản xuất, Báo cáo, Giá sản phẩm. Dùng được
cả trên điện thoại nếu cùng mạng wifi nhà (địa chỉ LAN được in ra trong cửa sổ khi khởi động app).
Giữ cửa sổ đen (Command Prompt) đang mở khi dùng app — đóng cửa sổ đó là app tắt. Dữ liệu ghi vào
đúng `data/orders.csv`/`data/production_log.csv`/`data/products.json` như trước giờ, không có gì
thay đổi ở chỗ lưu trữ.

Nếu không muốn mở app, vẫn có thể nhờ Claude Code làm qua chat như trước:

- "Viết giúp caption Facebook giới thiệu mẻ tinh bột sắn dây mới"
- "Ghi giúp đơn hàng: chị Lan mua 2kg tinh bột sắn dây, 150k/kg, đặt qua Zalo"
- "Ghi giúp mẻ sản xuất hôm nay: 10kg tinh bột sắn dây"
- "Tính giúp doanh thu tuần này"
- "Cập nhật giá tinh bột sắn dây túi 1kg thành 160k"

Claude sẽ tự chạy script hoặc sửa file phù hợp.

## Cấu trúc thư mục

- `.claude/agents/sales-content-writer.md` — subagent soạn nội dung đồng bộ cho cả 3 kênh
  (Facebook, Zalo, Shopee/TikTok Shop) từ một yêu cầu duy nhất. Gõ ví dụ "nhờ sales-content-writer
  viết bài giới thiệu mẻ sắn dây mới" hoặc cứ yêu cầu bình thường, Claude sẽ tự gọi khi phù hợp.
  Chỉ soạn nội dung — không tự đăng bài lên bất kỳ kênh nào.
- `CLAUDE.md` — ngữ cảnh dự án cho Claude (sản phẩm, giá, tông giọng, quy tắc)
- `data/products.json` — bảng giá và thông tin sản phẩm (sửa khi có giá thật)
- `data/orders.csv` — sổ đơn hàng
- `data/production_log.csv` — sổ sản xuất/thu hoạch

**Sao lưu tự động**: mỗi lần ghi đơn/mẻ/sửa giá (qua app web hoặc qua Claude), 3 file trong `data/`
tự động được copy sang `OneDrive\NongSanNhaLam-Backup\` (1 bản mới nhất + 1 bản lưu theo từng ngày).
Máy hỏng hay xoá nhầm vẫn còn bản trên OneDrive. Không cần làm gì thêm, tự chạy ngầm.
- `content/templates/` — mẫu caption theo từng kênh (Facebook, Zalo, Shopee/TikTok)
- `content/posts_ready.md` — nơi lưu các caption đã soạn, chờ đăng tay
- `content/ai_media_prompts.md` — prompt ảnh/video AI (dán vào Midjourney/DALL-E/Sora... vì Claude
  Code không tự tạo ảnh/video), dùng tạm trong lúc chưa có ảnh/video thật
- `content/ocop_mo_ta_san_pham.md` — bản nháp mô tả sản phẩm Cam Đường Canh cho hồ sơ OCOP (2026-08-04),
  còn vài chỗ `[CẦN CẬP NHẬT]` (diện tích, sản lượng) chờ số liệu thật
- `LICH_DANG_BAI.md` — lịch đăng bài cụ thể theo ngày (2026-08-04), gán ngày thật cho các bài có sẵn
  trong `content/posts_ready.md` vì phát hiện gần 1 tháng chưa đăng bài nào trong kho
- `scripts/` — script Python nhẹ, chạy bằng `python scripts/<ten_file>.py --help`. `nsn_core.py` là
  logic dùng chung (ghi đơn, ghi mẻ, tính báo cáo, sửa giá) cho cả script dòng lệnh và app web.
  `webapp.py` + `webapp_static/` là app quản lý chạy local (xem mục phía trên).
- `MO_APP_QUAN_LY.bat` — bấm đúp để mở app quản lý trên trình duyệt.
- `docs/` — website tĩnh: `index.html` (tiếng Việt), `en/index.html` (tiếng Anh, cho khách/đối tác
  xuất khẩu), dùng chung `styles.css`

## Ảnh trên website hiện tại

`docs/assets/` dùng 4 ảnh thật chụp tại vườn/xưởng nhà mình (từ 2026-07-26), chọn và nén lại từ
kho ảnh/video gốc trong `Hình Ảnh, Video/` — xem `docs/assets/CREDITS.md`. Kho gốc (269 file, ~1.2GB,
ảnh + video) KHÔNG đưa vào git vì quá nặng cho GitHub Pages; muốn đổi ảnh khác trên web thì chọn
file trong kho đó rồi nhờ Claude resize/nén lại trước khi đưa vào `docs/assets/`.

## Việc còn cần bạn làm

1. ~~Thay ảnh minh hoạ bằng ảnh/video thật~~ — ✅ đã xong (2026-07-26, xem mục trên). Còn nhiều
   ảnh/video thật chưa dùng trong `Hình Ảnh, Video/`, có thể nhờ Claude chọn thêm cho caption
   hoặc đổi ảnh web sau này.
2. **Link Facebook** — hiện đang tạm ẩn (comment) trong `docs/index.html` và để
   `"CẦN CẬP NHẬT"` trong `data/products.json`. Khi có link, nhờ Claude bật lại giúp.
3. **Email và WhatsApp cho khách quốc tế** — hiện để "CẦN CẬP NHẬT"/"coming soon" trong
   `data/products.json` và cả 2 trang web. Zalo không dùng được ở nước ngoài nên phần này
   khá quan trọng để thực sự nhận được liên hệ xuất khẩu. Khi có, nhờ Claude điền vào.
4. Giá, số Zalo (0979 502 000), khu vực giao hàng (toàn quốc) đã cập nhật đầy đủ.
5. Đã có sẵn 5 caption mẫu dùng số liệu thật trong `content/posts_ready.md`, sẵn sàng copy đăng.
6. Trang tiếng Anh nói rõ cơ sở CHƯA có chứng nhận ATTP/HACCP/xuất khẩu chính thức — nếu sau này
   có, nhờ Claude cập nhật cả 2 trang để tăng uy tín với khách quốc tế.
7. **Shopee/TikTok Shop (Tinh Bột Sắn Dây)** — đã quyết định mở (xem `KE_HOACH_BAN_HANG.md`), trang
   tiếng Việt hiện để "sắp ra mắt". Bạn tự đăng ký gian hàng; khi có link thật, nhờ Claude thay vào
   `docs/index.html` (mục sản phẩm + mục Đặt hàng).

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
