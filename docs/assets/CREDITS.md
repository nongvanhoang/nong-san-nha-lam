# Nguồn ảnh / video

Từ 2026-07-26, website dùng ảnh thật chụp tại vườn/xưởng nhà mình, không còn dùng ảnh minh hoạ
stock nữa:

- `tinh-bot-san-day-real-01.jpg` — bánh tinh bột sắn dây thành phẩm
- `tinh-bot-san-day-real-02.jpg` — vườn sắn dây nhà mình (vùng núi Lạng Sơn)
- `cam-duong-canh-real-qua.jpg` — cam đường canh bổ đôi, chụp tại vườn
- `cam-duong-canh-real-vuon.jpg` — toàn cảnh vườn cam nhà mình buổi sáng sớm

Từ 2026-08-11, thêm video thật vào cả 2 trang (VI/EN):

- `san-day-thu-hoach.mp4` — video thu hoạch củ sắn dây, nén lại từ file gốc
  `Hình Ảnh, Video/Sắn Dây/san-day-video-thuhoach-dung-01.mp4` (9.4MB → nén còn ~3.2MB bằng ffmpeg,
  scale 540px, CRF 27, không âm thanh) để tải nhanh trên web. Không có tiếng nói/nhạc trong clip gốc.
- `san-day-thu-hoach-poster.jpg` — ảnh đại diện (poster) trích từ giây thứ 2 của video trên.
- `san-day-quy-trinh-say.mp4` — video quy trình sấy (nặn bột ướt → xếp khay → lò sấy nhiều tầng →
  bảng điều khiển → gạt nước → bột rạn vân trắng lúc khô → thành phẩm vỡ giòn), dựng bằng
  `content/video/make_process_video.py` từ 11 clip thật có sẵn trong kho ảnh/video (đã có sẵn từ
  đợt nhập media 2026-07-25, không cần quay mới) — xem cấu hình đầy đủ ở
  `content/video/configs/quy-trinh-say-san-day.json`. **Cập nhật 2026-09-04**: dựng lại đầy đủ hơn
  bản gốc (5 clip/24s → 11 clip/47s), có thêm giọng đọc AI (Edge-TTS, miễn phí) + phụ đề tiếng Anh
  chèn cứng. Nén còn ~5MB (audio + thời lượng gấp đôi nên nặng hơn bản cũ 1.5MB, vẫn `preload="none"`
  nên không tải khi mới vào trang).
- `san-day-quy-trinh-say-poster.jpg` — ảnh đại diện trích từ video trên (cập nhật 2026-09-04, cùng
  lúc với video).

Từ 2026-09-04, thêm video "hành trình đầy đủ" vào cả 2 trang VI/EN (mục "Nhà mình làm thế nào" /
"How we make it") — trang giờ có 2 video xếp theo thứ tự tổng quan → chi tiết:

- `san-day-hanh-trinh-day-du.mp4` — video đầy đủ cả 3 công đoạn (đào củ → nghiền lọc → sấy), dựng
  từ 14 clip thật + giọng đọc AI (Edge-TTS) + phụ đề tiếng Anh, xem cấu hình ở
  `content/video/configs/san-day-hanh-trinh-day-du.json`. Nén cho web (540x960, CRF 27) còn ~7.7MB,
  `preload="none"` nên không tải khi mới vào trang.
- `san-day-hanh-trinh-day-du-poster.jpg` — ảnh đại diện trích từ video trên (cảnh máy xúc đào gốc).

**2026-09-05**: thêm video thứ 3 "Củ tươi to cỡ nào" vào trang `san-day.html`/`en/san-day.html` —
`san-day-cu-tuoi.mp4` (5 clip thật, có giọng đọc AI + phụ đề Anh, cảnh ôm củ to hơn người khi so
với đồng hồ đeo tay), nén cho web (540x960, CRF 27) còn ~4MB. Poster
`san-day-cu-tuoi-poster.jpg` trích lại từ bản video mới nhất (bản cũ lúc soạn caption đã lỗi thời
do video được dựng lại theo nhịp độ mới cùng ngày, xem `content/video/configs/README.md`).

Cùng ngày, thêm video đầu tiên cho trang Cam Đường Canh (cả 2 bản VI/EN, mục "Nhìn lại vườn cam
nhà mình" / "A look back at our orchard") — trước đó trang này chưa có video nào:

- `cam-vuon-mua-truoc.mp4` — 5 clip thật từ mùa thu hoạch trước (~11/2025-1/2026, xác nhận với
  người dùng 2026-09-03), chữ đè tiếng Việt, KHÔNG có giọng đọc/phụ đề Anh (Cam Đường Canh chưa
  chào xuất khẩu, xem `CLAUDE.md`) — trang EN vẫn nhúng file này kèm ghi chú rõ "on-screen text is
  in Vietnamese", không giả vờ là nội dung song ngữ. Nén cho web (540x960, CRF 27, không âm thanh
  vì bản gốc cũng không có) còn ~2.1MB.
- `cam-vuon-mua-truoc-poster.jpg` — ảnh đại diện trích từ video trên.

**Tối ưu giao diện/tốc độ (2026-09-04)** — rà code thật (không đo Lighthouse vì không có công cụ
trình duyệt trong phiên này), sửa 4 điểm cụ thể trên cả 4 trang có video:
- Thêm class CSS dùng chung `.video-frame` trong `site.css`, thay 8 chỗ đang lặp inline style
  y hệt nhau (do vừa thêm nhiều video cùng lúc) — dễ sửa sau này (đổi 1 chỗ áp dụng cả trang).
- `.video-frame video` khai báo sẵn `aspect-ratio:9/16` — tránh trang bị giật (layout shift) lúc
  ảnh poster tải xong, các video trước đó không khai báo kích thước.
- `loading="lazy"` cho ảnh `cam-duong-canh-real-qua.jpg` (2 trang VI/EN) — ảnh nội dung thật duy
  nhất nằm dưới màn hình đầu; các ảnh hero khác dùng CSS `background-image` nên không áp dụng được
  thuộc tính này.
- Nén lại 5 ảnh nặng nhất site (`hero-cam-poster.jpg`, `cam-duong-canh-real-qua.jpg`,
  `home-hero.jpg`, `san-day-vuon-toancanh-real.jpg`, `hero-san-day-poster.jpg`) bằng ffmpeg
  `-q:v 6`, giảm tổng ~550KB, đã kiểm tra bằng mắt không thấy khác biệt chất lượng.

Video khâu phơi/sấy cũ (`san-day-video-haitruong-dung-01.mp4`, chưa dùng trên web, chỉ có trong kho
mạng xã hội) đã kiểm tra lại 2026-08-11: KHÔNG quay cảnh phơi nắng ngoài trời như tên gọi, vẫn dùng
được — xem ghi chú trong `content/posts_ready.md`.

Ảnh/video gốc (độ phân giải cao hơn) lưu trong `Hình Ảnh, Video/` ở thư mục gốc dự án (không đưa vào
repo git vì dung lượng lớn — xem README.md). Khi muốn đổi ảnh/video khác, chọn từ thư mục đó rồi nhờ
Claude resize/nén lại trước khi đưa vào đây.
