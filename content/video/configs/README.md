# Cấu trúc file config cho `make_process_video.py`

Mỗi video 1 file JSON riêng trong thư mục này (đặt tên theo slug, vd `san-day-thu-hoach.json`).

```json
{
  "slug": "san-day-thu-hoach",
  "clips": [
    {"file": "Sắn Dây/san-day-cutuoi-botrenco-09.mp4", "start": 0, "duration": 2.5},
    {"file": "Sắn Dây/san-day-nghienloc-XX.mp4", "start": 1, "duration": 3}
  ],
  "captions": [
    {"text": "Sắn dây nhà mình - thu hoạch tận vườn", "clip_index": 0, "start": 0, "duration": 2.5},
    {"text": "Nghiền lọc thủ công, không hoá chất", "clip_index": 1, "start": 0, "duration": 3}
  ],
  "end_card_text": "Đặt hàng: Zalo 0979 502 000"
}
```

- `clips[].file` — đường dẫn TƯƠNG ĐỐI tính từ `Hình Ảnh, Video/` (thư mục gốc chứa toàn bộ clip
  thật). Không tự bịa tên file — luôn kiểm tra file thật tồn tại trước (dùng Glob/Bash `ls`).
- `clips[].start`/`duration` — giây, cắt từ clip gốc (không nhất thiết dùng cả clip).
- `captions[].clip_index` — clip thứ mấy (đếm từ 0 theo mảng `clips`) mà chữ này sẽ hiện lên khi
  video chạy tới đoạn của clip đó. `start`/`duration` tính theo thời gian RIÊNG của clip đó, script
  tự quy đổi sang thời gian tuyệt đối trên video đã ghép.
- `end_card_text` — dòng chữ cuối video (có thể nhiều dòng, cách nhau `\n`), luôn dùng số điện
  thoại/Zalo thật lấy từ `CLAUDE.md`/`data/products.json`, không tự bịa.

Chạy: `python make_process_video.py --config configs/<slug>.json`
Output: `output/<slug>.mp4` + `output/<slug>_caption.txt` (agent tự điền caption sau khi tạo xong).

## Ghi chú 2026-08-11 — quy trình sấy đã đổi

Từ 2026-08-11, Tinh Bột Sắn Dây sấy bằng **lò sấy chuyên dụng**, không còn phơi nắng tự nhiên. Đã
sửa chữ caption trong `quy-trinh-san-day.json` cho đúng, nhưng **clip gốc ở bước 3
(`san-day-phoisay-botkhoduoinangvang-07.mp4`) vẫn quay cảnh bột phơi dưới nắng thật** — chỉ sửa chữ
không đủ, vì hình vẫn cho thấy quy trình cũ. `content/video_final/san-day-phoibot-final.mp4` (video
đã dựng từ config này) coi như lỗi thời, đừng dùng cho tới khi có clip mới quay cảnh lò sấy để thay
vào bước 3 rồi chạy lại script.
