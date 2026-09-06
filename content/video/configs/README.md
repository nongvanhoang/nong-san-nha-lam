# Cấu trúc file config cho `make_process_video.py`

Mỗi video 1 file JSON riêng trong thư mục này (đặt tên theo slug, vd `san-day-thu-hoach.json`).

**Quy tắc nhịp độ (chốt 2026-09-04, sau phản hồi thật "chuyển cảnh nhanh, chưa kịp hiểu")**: mỗi
cảnh (`clips[].duration`) tối thiểu **4-4.5 giây**, không dùng 2.5-3s như trước — người xem cần đủ
thời gian vừa nhìn hình vừa đọc chữ. Để giữ tổng thời lượng video hợp lý (15-25s), **ưu tiên DÙNG ÍT
CẢNH HƠN thay vì rút ngắn từng cảnh** — 4-5 cảnh/video là vừa, đừng cố nhồi 7-8 cảnh vào 20s. Cách
này còn tiết kiệm nguyên liệu thật (mỗi video "tiêu" ít clip hơn), để dành clip cho video sau thay
vì dùng dồn hết 1 lần.

```json
{
  "slug": "san-day-thu-hoach",
  "clips": [
    {"file": "Sắn Dây/san-day-cutuoi-botrenco-09.mp4", "start": 0, "duration": 2.5},
    {"file": "Sắn Dây/san-day-nghienloc-XX.mp4", "start": 1, "duration": 3}
  ],
  "captions": [
    {"text": "Sắn dây nhà mình - thu hoạch tận vườn", "text_en": "Kudzu root - harvested right in our garden", "clip_index": 0, "start": 0, "duration": 2.5},
    {"text": "Nghiền lọc thủ công, không hoá chất", "text_en": "Hand-ground and filtered, no chemicals", "clip_index": 1, "start": 0, "duration": 3}
  ],
  "narration": {
    "text": "Sắn dây nhà mình được thu hoạch tận vườn, rồi nghiền lọc thủ công, không dùng hoá chất.",
    "voice": "vi-VN-HoaiMyNeural"
  },
  "end_card_text": "Đặt hàng: Zalo 0979 502 000",
  "end_card_text_en": "Order via Zalo: +84 979 502 000"
}
```

- `clips[].file` — đường dẫn TƯƠNG ĐỐI tính từ `Hình Ảnh, Video/` (thư mục gốc chứa toàn bộ clip
  thật). Không tự bịa tên file — luôn kiểm tra file thật tồn tại trước (dùng Glob/Bash `ls`).
- `clips[].start`/`duration` — giây, cắt từ clip gốc (không nhất thiết dùng cả clip).
- `captions[].clip_index` — clip thứ mấy (đếm từ 0 theo mảng `clips`) mà chữ này sẽ hiện lên khi
  video chạy tới đoạn của clip đó. `start`/`duration` tính theo thời gian RIÊNG của clip đó, script
  tự quy đổi sang thời gian tuyệt đối trên video đã ghép.
- `captions[].text_en` — **tuỳ chọn**. Bản dịch tiếng Anh, hiện thành phụ đề nhỏ hơn/in nghiêng ngay
  phía trên dòng chữ tiếng Việt cùng lúc. Bỏ trống nếu bài chỉ đăng nội địa (Facebook/Zalo/Shopee),
  chỉ cần điền khi video hướng tới LinkedIn/Instagram/TikTok/YouTube quốc tế.
- `narration` — **tuỳ chọn**. Có thì video có thêm giọng đọc AI tiếng Việt (Edge-TTS, miễn phí,
  không cần API key — không vi phạm quy tắc "không gọi API AI trả phí" trong `CLAUDE.md`). Chỉ thêm
  LỜI ĐỌC, không đổi/dựng thêm hình ảnh nào — clip vẫn 100% thật. `text` nên là câu văn nói tự nhiên
  (khác caption chữ, vốn ngắn/gọn kiểu tiêu đề) — viết như đang kể lại quy trình bằng lời, giọng
  "nhà mình" đúng tông thương hiệu. `voice` tuỳ chọn, mặc định `vi-VN-HoaiMyNeural` (nữ, thân thiện);
  đổi sang `vi-VN-NamMinhNeural` (nam) nếu muốn đổi giọng. Nếu lời đọc dài hơn video gốc, script tự
  kéo dài thẻ kết thúc để không cắt cụt lời đọc (báo ra màn hình khi việc này xảy ra).
- `end_card_text` — dòng chữ cuối video (có thể nhiều dòng, cách nhau `\n`), luôn dùng số điện
  thoại/Zalo thật lấy từ `CLAUDE.md`/`data/products.json`, không tự bịa.
- `end_card_text_en` — **tuỳ chọn**, bản tiếng Anh của thẻ kết thúc (chữ nhỏ hơn, nằm dưới bản
  tiếng Việt). Chỉ cần khi video có phụ đề tiếng Anh ở trên.

Chạy: `python make_process_video.py --config configs/<slug>.json`
Output: `output/<slug>.mp4` + `output/<slug>_caption.txt` (agent tự điền caption sau khi tạo xong).
Cần cài `edge-tts` một lần nếu dùng `narration`: `pip install edge-tts` (đã cài sẵn trên máy này
từ 2026-09-03).

## Chọn định dạng nào cho LinkedIn/Instagram/TikTok/YouTube?

Video vẫn xuất ra 1 bản dọc 1080x1920 (9:16) duy nhất — dùng được thẳng cho TikTok, Instagram Reels,
YouTube Shorts, và LinkedIn (nền này hiển thị video dọc bình thường trong feed). Chưa cần dựng thêm
bản ngang riêng vì nội dung là clip quy trình ngắn (15-30s), đúng định dạng "short-form" của cả 4
nền tảng. Nếu sau này cần video dài hơn dạng YouTube thường (16:9), báo lại để thêm biến thể ngang.

## Nhạc nền (thêm 2026-09-06)

- `music` — **tuỳ chọn**. `{"file": "content/video/music/ten-file.mp3", "volume": 0.16}` — đường dẫn
  TƯƠNG ĐỐI tính từ gốc dự án (`NongSanNhaLam/`, khác với `clips[].file` tính từ `Hình Ảnh, Video/`).
  `volume` tuỳ chọn (mặc định `0.16`, đủ nhỏ để không lấn giọng đọc AI). Script tự cắt nhạc vừa đúng
  độ dài video (kể cả thẻ kết thúc), fade in 1s / fade out 1.5s ở cuối. Nếu video có cả `narration`
  lẫn `music`, 2 lớp âm thanh được trộn bằng `amix` (giọng đọc giữ nguyên volume gốc, không bị chia
  đôi). Nếu chỉ có `music` (không `narration`), video vẫn im lặng phần lời, chỉ có nhạc nền.

4 bài nhạc miễn phí bản quyền (Pixabay Content License — dùng thương mại được, không cần ghi credit)
đã tải về, lưu ở `content/video/music/`. **Đã tích hợp vào cả 6 video dưới đây (2026-09-06)** —
dựng lại xong, bản trên website (`docs/assets/`) và bản email đính kèm (xuất khẩu) cũng đã đồng bộ:

| File | Dùng cho video |
|---|---|
| `morning-garden-acoustic-chill.mp3` (folk_acoustic, 3:53) | `san-day-buoi-sang-tren-nuong` |
| `nostalgic-acoustic-music.mp3` (andriig, 2:10) | `cam-duongcanh-ham-nong` |
| `warm-acoustic-music.mp3` (andriig, 2:20) | `san-day-hanh-trinh-day-du`, `san-day-cu-tuoi`, `quy-trinh-say-san-day` |
| `instrumental-acoustic-guitar-music.mp3` (STAROSTIN, 3:45) | `san-day-gioi-thieu-xuat-khau` (tiếng Anh) |

## Ghi chú 2026-08-11 — quy trình sấy đã đổi

Từ 2026-08-11, Tinh Bột Sắn Dây sấy bằng **lò sấy chuyên dụng**, không còn phơi nắng tự nhiên. Đã
sửa chữ caption trong `quy-trinh-san-day.json` cho đúng, nhưng **clip gốc ở bước 3
(`san-day-phoisay-botkhoduoinangvang-07.mp4`) vẫn quay cảnh bột phơi dưới nắng thật** — chỉ sửa chữ
không đủ, vì hình vẫn cho thấy quy trình cũ. `content/video_final/san-day-phoibot-final.mp4` (video
đã dựng từ config này) coi như lỗi thời, đừng dùng cho tới khi có clip mới quay cảnh lò sấy để thay
vào bước 3 rồi chạy lại script.
