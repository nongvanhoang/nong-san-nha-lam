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
- `san-day-quy-trinh-say.mp4` — video quy trình sấy (bảng điều khiển nhiệt độ, khay sấy nhiều tầng),
  dựng bằng `content/video/make_process_video.py` từ 5 clip thật có sẵn trong kho ảnh/video
  (đã có sẵn từ đợt nhập media 2026-07-25, không cần quay mới) — xem cấu hình đầy đủ ở
  `content/video/configs/quy-trinh-say-san-day.json`. Nén còn ~1.5MB để tải nhanh trên web.
- `san-day-quy-trinh-say-poster.jpg` — ảnh đại diện trích từ video trên.

Video khâu phơi/sấy cũ (`san-day-video-haitruong-dung-01.mp4`, chưa dùng trên web, chỉ có trong kho
mạng xã hội) đã kiểm tra lại 2026-08-11: KHÔNG quay cảnh phơi nắng ngoài trời như tên gọi, vẫn dùng
được — xem ghi chú trong `content/posts_ready.md`.

Ảnh/video gốc (độ phân giải cao hơn) lưu trong `Hình Ảnh, Video/` ở thư mục gốc dự án (không đưa vào
repo git vì dung lượng lớn — xem README.md). Khi muốn đổi ảnh/video khác, chọn từ thư mục đó rồi nhờ
Claude resize/nén lại trước khi đưa vào đây.
