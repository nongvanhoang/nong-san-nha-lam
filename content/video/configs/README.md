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
