# Lịch Đăng Bài Cụ Thể (từ 2026-08-04)

_Tự soạn 2026-08-04 vì kho nội dung sẵn có trong `content/posts_ready.md` (19 bài) gần như chưa
dùng — chỉ để xác định NGÀY NÀO đăng BÀI NÀO, không tạo nội dung mới. Nhịp đề ra: 2 lần/tuần
(Thứ 3 + Thứ 6) — nếu bận không kịp đúng ngày thì lùi vài ngày cũng được, quan trọng là đăng đều,
không để trống cả tháng như vừa qua._

**Ghi chú 2026-08-11**: nhà mình đã chuyển từ phơi nắng sang sấy bằng lò sấy chuyên dụng cho Tinh
Bột Sắn Dây. Đã rà lại toàn bộ chữ trong kho bài — kiểm tra kỹ từng video thật thì phát hiện video
"hậu trường phơi" KHÔNG hề quay cảnh ngoài trời nào (chỉ tên gọi cũ gây hiểu lầm), nên 2 mục Thứ 6
bên dưới **vẫn đăng được bình thường**, chỉ cần đổi đúng bản chữ mới trong `content/posts_ready.md`
(đã sửa sẵn). Ngoài ra có thêm video mới `quy-trinh-say-san-day.mp4` quay đúng cảnh lò sấy thật
(bảng điều khiển, khay sấy nhiều tầng) — dùng thay hoặc dùng thêm tuỳ ý.

**Cách dùng**: đến ngày, mở `content/posts_ready.md` ở dòng ghi tương ứng, copy-paste đăng tay.
Sau khi đăng, quay lại tick `[x]` ở dòng dưới đây VÀ đánh dấu `[Đã đăng]` vào đầu tiêu đề bài đó
trong `posts_ready.md` (để không đăng trùng lần sau).

**Quy tắc dùng chung ảnh/video cho nhiều kênh (chốt 2026-09-04)**:
- **Video**: pipeline `make_process_video.py` xuất sẵn 1080×1920 (dọc, chuẩn 9:16) — dùng **nguyên 1
  file** cho Facebook, Zalo, Instagram Reels, TikTok, YouTube Shorts, không cần dựng riêng. LinkedIn
  cũng phát được video dọc bình thường (không chuẩn gu ngang/vuông của họ, nhưng không đáng dựng
  riêng chỉ vì 1 kênh) — vẫn dùng chung. Giữ nguyên cấu hình 1080×1920 khi dựng video mới về sau.
- **Ảnh**: kho ảnh hiện có tỷ lệ không đồng nhất (có ảnh ngang ~900×506, có ảnh dọc ~720×1280/540×960)
  — **không dùng chung được như video**, chọn theo kênh:
  - Ảnh dọc/vuông → Instagram feed, ảnh bìa video (nơi bị crop nếu dùng ảnh ngang).
  - Ảnh ngang → Facebook, Zalo, website (không bị crop, ảnh ngang hiển thị đẹp hơn ở đây).

## Checklist đăng theo kênh (chốt 2026-09-04)

_Bảng duy nhất theo dõi đã đăng kênh nào — tick ✅ trực tiếp vào đây, không cần sửa thêm ở
`posts_ready.md` nữa (chỉ sửa `posts_ready.md` khi thêm bài mới). LinkedIn/YouTube không bắt buộc
đúng ngày, tick khi nào đăng xong._

| Ngày | Chủ đề | FB | Zalo | Instagram | LinkedIn | YouTube |
|---|---|---|---|---|---|---|
| 08/09 | Hành trình đầy đủ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ (chờ có kênh) |
| 11/09 | Bên trong lò sấy | ⬜ | ⬜ | ⬜ | — | ⬜ (chờ có kênh) |
| 15/09 | Nhìn lại vườn cam mùa trước | ⬜ | ⬜ | ⬜ | — | — |
| 18/09 | Mở rộng vùng trồng sắn dây | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ (chờ có kênh) |
| 22/09 | Củ sắn dây tươi (video, dựng xong 04/09) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ (chờ có kênh) |
| 25/09 | Một góc khác của vườn (ảnh, mới 04/09) | ⬜ | ⬜ | ⬜ | — | — |
| 29/09 | Một buổi sáng trên nương (video, dựng xong 06/09) | ⬜ | ⬜ | ⬜ | — | — |
| 02/10 | Cam Đường Canh: hoa đến quả non (video hâm nóng, dựng xong 06/09) | ⬜ | ⬜ | ⬜ | — | — |
| Bất kỳ lúc nào | Company intro tiếng Anh (video, dựng xong 06/09) | — | — | — | ⬜ | — |

**Ghi chú 2026-08-17**: rà lại lịch, thấy đã trễ 4 mốc liên tiếp (04/08, 07/08, 11/08, 14/08) —
đồng thời phát hiện `posts_ready.md` đã có thêm nội dung mới hơn (video đào củ 15-16/08) mà lịch
này chưa cập nhật, số dòng tham chiếu trong các mục cũ cũng đã lệch vì nội dung mới chèn lên đầu
file. Quyết định: **bỏ qua mốc 04/08** (2 bài thu hoạch — đã có clip mới hơn 15-16/08 thay thế,
đăng bài cũ giờ sẽ thấy lạc hậu so với nội dung mới hơn cùng chủ đề). Mốc 07/08, 11/08, 14/08 vẫn
còn dùng được (công thức/cách dùng không lỗi thời, cam thì chỉ hơi trễ vài ngày không đáng kể) —
đăng bù dần trong tuần, không cần đúng thứ tự ngày gốc.

## Tuần 1

- [ ] **Thứ 3, 04/08/2026** — Đợt 1 (đăng đồng thời cả 3, đúng kế hoạch gốc trong
  `TRIEN_KHAI_DONG_THOI_SOCIAL.md`):
  - Facebook: "Quy mô thu hoạch thật, không phải làm cho có" (dòng ~100 trong posts_ready.md)
  - Zalo: "Báo khách quen có ảnh/video thật mới" (dòng ~136)
  - TikTok/Reels: video thu hoạch dựng sẵn `san-day-video-thuhoach-dung-01.mp4` (dòng ~85)
- [ ] **Thứ 6, 07/08/2026** — Đợt 2 (**đã trễ + 2 mục dưới cần sửa trước khi đăng, xem ghi chú
  2026-08-11**):
  - Facebook: "3 cách dùng tinh bột sắn dây giải nhiệt ngày hè" (dòng ~61) — vẫn đăng được.
  - Facebook/Zalo: "Từ video thật đến túi tinh bột, không giấu gì cả" (dòng ~153) — đã sửa 1 chữ
    "phơi" thành "sấy" trong `posts_ready.md`, đăng bình thường.
  - TikTok/Reels: video hậu trường `san-day-video-haitruong-dung-01.mp4` (dòng ~119) — vẫn dùng
    được (không quay cảnh ngoài trời), dùng chữ chốt mới đã sửa trong `posts_ready.md`.
  - Shopee/TikTok Shop: mô tả sản phẩm (dòng ~311, đã sửa lại đúng quy trình lò sấy 2026-08-11) —
    **chỉ đăng nếu gian hàng đã đăng ký xong**; nếu chưa xong thì bỏ qua mục này, đợi tuần nào đăng
    ký xong thì dùng.

## Tuần 2

- [ ] **Thứ 3, 11/08/2026** — Cam Đường Canh, hâm nóng nhẹ (được phép đăng sớm theo
  `TRIEN_KHAI_DONG_THOI_SOCIAL.md` Đợt 3, không cần đợi tháng 9-10):
  - Facebook/Zalo: "Cập nhật vườn cam, quả non đã đậu trên cành" (dòng ~40)
- [ ] **Thứ 6, 14/08/2026** — nội dung mới nhất chưa dùng:
  - Facebook: "Công thức chè sắn dây hạt sen giải nhiệt" (dòng ~9, soạn 03/08)

## Tuần 3

- [ ] **Thứ 3, 18/08/2026**:
  - Zalo: "Công thức chè sắn dây hạt sen giải nhiệt" (dòng ~29, bản Zalo của bài Thứ 6 tuần trước —
    đăng lệch kênh/lệch ngày để không trùng lúc)
- [ ] **Thứ 6, 21/08/2026**: kho bài mới soạn riêng cho mùa hè coi như dùng hết ở đây. Nếu chưa có
  đơn hàng thật nào để khoe (mục "Ghi sổ đơn hàng" vẫn đang trống), có thể dùng lại bài nền tảng cũ
  "Giới thiệu Tinh Bột Sắn Dây" (dòng ~252) làm bài lấp chỗ — hoặc nhắn tôi soạn thêm góc độ mới
  (feedback khách nếu đã có, hoặc mượn 1-2 ảnh/video thật chưa dùng trong
  `Hình Ảnh, Video/Sắn Dây/`).

## Tuần 4

_Soạn 2026-08-12 — kho 24 bài cũ đến đây gần như hết cho Tinh Bột Sắn Dây, nên 2 mục dưới là nội
dung MỚI, khai thác góc chưa từng lên bài: công đoạn "nghiền lọc" (có ảnh/video thật, chưa dùng
bao giờ) và video lò sấy đã dựng xong nhưng mới chỉ nằm trên website, chưa đăng mạng xã hội riêng._

- [ ] **Thứ 3, 25/08/2026**:
  - Facebook: "Công đoạn ít ai thấy: nghiền củ, lọc lấy từng giọt tinh bột" (trong posts_ready.md) —
    kèm 2 ảnh thật mới trích: `docs/assets/san-day-nghienloc-loc-tay.jpg` (tay lọc bột) và
    `docs/assets/san-day-nghienloc-may-nghien.jpg` (máy nghiền ép bã).
  - Zalo: bản ngắn cùng chủ đề (cùng mục ngay dưới bài Facebook)
- [ ] **Thứ 6, 28/08/2026** (2 lựa chọn, có thể đăng 1 hoặc cả 2 cách nhau vài ngày):
  - TikTok/Reels: đăng riêng `docs/assets/san-day-quy-trinh-say.mp4` kèm caption mới soạn (mục
    "Caption riêng cho video quy trình sấy lò" trong posts_ready.md) — video đã có sẵn, chỉ cần
    đăng, không cần dựng gì thêm.
  - **Mới dựng 12/08**: `content/video/output/quy-trinh-nghien-loc-san-day.mp4` (~17s) — video quy
    trình nghiền lọc, dựng thật từ 5 clip trong `Hình Ảnh, Video/Sắn Dây/san-day-nghienloc-*` (rửa
    củ → máy nghiền → lọc tay → bể lắng), chuyển cảnh mượt (crossfade), kèm caption trong
    posts_ready.md. Nếu đăng cả 2 video trong tuần, cách nhau vài ngày để không trùng lúc.
  - **Cập nhật 12/08**: bản trên website (`docs/assets/san-day-quy-trinh-say.mp4`) đã đồng bộ với
    bản chuyển cảnh mượt mới — nén lại đúng theo quy cách cũ (540x960, ~650kbps) nên nhẹ hơn bản cũ
    một chút (1.1MB so với 1.5MB) dù chất lượng hình không đổi.

## Tuần 5

_Soạn 2026-08-15 — 2 góc độ MỚI, khai thác ảnh/video thật chưa từng dùng: cảnh vườn (giàn dây leo,
chưa từng lên bài) và thêm góc thu hoạch máy xúc (khác bài "quy mô thu hoạch" ở Tuần 1, lần này
nhấn vào kích thước gốc củ). Cả 2 đã dựng xong khung thiết kế Canva theo đúng bộ nhận diện — ảnh
thật và logo đã chèn sẵn, chỉ cần mở link và tải xuống đăng._

- [ ] **Thứ 3, 01/09/2026**:
  - Facebook: "Giàn sắn dây trước khi đào củ" (trong posts_ready.md) — ảnh + logo đã chèn sẵn,
    khung Canva sẵn sàng tải xuống đăng: https://www.canva.com/d/2tzcazwJLseEloQ
  - Zalo: bản ngắn cùng chủ đề (cùng mục ngay dưới bài Facebook)
- [ ] **Thứ 6, 04/09/2026** (2 lựa chọn, có thể đăng 1 hoặc cả 2 cách nhau vài ngày):
  - Facebook: "Gốc củ to cỡ nào mới cần máy xúc đào" (trong posts_ready.md) — ảnh + logo đã chèn
    sẵn, khung Canva sẵn sàng tải xuống đăng: https://www.canva.com/d/EOx3J3jr_5Sfg0w
  - Zalo: bản ngắn cùng chủ đề (cùng mục ngay dưới bài Facebook)
  - **Mới dựng 16/08**: TikTok/Reels — `content/video/output/quy-trinh-dao-cu-may-xuc.mp4` (~15s,
    5 clip thật: đào đất → người phụ đào → bẩy gốc → cận cảnh gốc củ → kéo dây lên), caption trong
    posts_ready.md. Nếu đăng cả ảnh tĩnh lẫn video trong tuần, cách nhau vài ngày để không trùng lúc.

## Tuần 6

_Soạn 2026-09-04 — kho bài cũ đã hết đúng như dự kiến, nhưng cùng ngày này vừa dựng xong 2 video
Sắn Dây dựng lại đầy đủ hơn nhiều (giọng đọc AI + phụ đề Anh + nhiều cảnh thật chưa từng dùng), gỡ
đúng điểm nghẽn đã ghi ở đây trước đó. Caption đầy đủ ở `content/posts_ready.md`._

**Từ mốc này trở đi (04/09): đăng đồng thời trên TẤT CẢ kênh đang có mỗi lần đến lịch**, thay vì
chia chủ đề khác nhau theo từng tuần như trước — 1 nội dung, nhiều bản theo từng kênh, đăng cùng
ngày. Instagram chính thức vào nhịp 2 lần/tuần từ đây (tài khoản đã có sẵn). **YouTube Shorts đã
soạn sẵn nội dung nhưng CHƯA có kênh** — cần tự tạo kênh YouTube trước (Claude không tự tạo tài
khoản được), xong thì đăng theo nội dung đã có trong posts_ready.md, không cần đúng ngày.

**Cập nhật 2026-09-05**: sau phản hồi thật "chuyển cảnh nhanh, chưa kịp hiểu", đã chỉnh lại nhịp độ
toàn bộ script dựng video (xem `content/video/configs/README.md`) — cảnh dài hơn (4-5s thay vì
2.5-3s), ít cảnh hơn/video. 2 video Tuần 6 dưới đây đã dựng lại theo nhịp mới, thời lượng/số cảnh
đổi khác so với lúc soạn lịch (04/09): "Hành trình đầy đủ" còn **34s/7 cảnh** (trước ghi 54s/14
cảnh), "Bên trong lò sấy" còn **31s/6 cảnh** (trước ghi 47s/11 cảnh) — nội dung/câu chuyện vẫn y
nguyên, chỉ đổi nhịp xem cho dễ theo dõi hơn.

- [ ] **Thứ 3, 08/09/2026** — "Hành trình đầy đủ, từ gốc củ đến túi tinh bột" (video
  `san-day-hanh-trinh-day-du.mp4`, 34s, 7 cảnh, có giọng đọc AI + phụ đề Anh):
  - Facebook: bản đầy đủ trong posts_ready.md
  - Zalo: bản ngắn cùng mục
  - Instagram (Reels): bản mới soạn 04/09, có hashtag — cùng mục trong posts_ready.md
  - LinkedIn: bản tiếng Anh, hướng đối tác sỉ/xuất khẩu — không cần đúng ngày, đăng khi thuận tiện
  - YouTube Shorts: tiêu đề + mô tả đã soạn sẵn — **đợi có kênh mới đăng**
- [ ] **Thứ 6, 11/09/2026** — "Bên trong lò sấy, từ bột ướt đến khô giòn" (video
  `quy-trinh-say-san-day.mp4`, bản dựng lại 31s, 6 cảnh):
  - Facebook: bản đầy đủ trong posts_ready.md
  - Zalo: bản ngắn cùng mục
  - Instagram (Reels): bản mới soạn 04/09, có hashtag — cùng mục trong posts_ready.md
  - YouTube Shorts: tiêu đề + mô tả đã soạn sẵn — **đợi có kênh mới đăng**

## Tuần 7

_Đổi sang Cam Đường Canh 1 tuần để không dồn hết vào Sắn Dây liên tiếp — đúng lúc video vườn cam
mùa trước vừa dựng xong (2026-09-03), và đang là giai đoạn "hâm nóng" trước mùa mới (~T11 âm lịch)
theo Giai đoạn 2 của `KE_HOACH_BAN_HANG.md`._

- [ ] **Thứ 3, 15/09/2026**:
  - Facebook + Zalo: "Nhìn lại vườn cam mùa trước" — video
    `content/video/output/cam-vuon-mua-truoc.mp4` (16s), caption đã có sẵn trong posts_ready.md
    (viết ở thì quá khứ, KHÔNG chào bán vì chưa vào mùa — CTA là "để lại inbox nhận tin" chứ không
    phải "đặt hàng ngay").
  - Instagram (Reels): bản mới soạn 05/09, giữ đúng CTA "để lại inbox" — cùng mục trong
    posts_ready.md
- [ ] **Thứ 6, 18/09/2026**:
  - Facebook + Zalo: "Mở rộng vùng trồng sắn dây" — video
    `content/video/output/san-day-mo-rong-vung-trong.mp4` (dựng 2026-09-04 từ 4 clip
    `san-day-vuonmoi-*.mp4`, ruộng mới trồng), caption đã có sẵn trong posts_ready.md — góc độ hoàn
    toàn mới, chưa từng kể.
  - Instagram (Reels): bản mới soạn 05/09 — cùng mục trong posts_ready.md

## Tuần 8

_Soạn 2026-09-05 — 2 nội dung Sắn Dây đã dựng/viết xong (04/09) nhưng chưa có ngày cụ thể: video
"củ tươi" (góc độ chưa từng kể — hình dạng thật của củ trước khi chế biến) và bộ ảnh "vườn lúc còn
xanh". Cả 2 đã có caption đủ 3 kênh (Facebook/Zalo/Instagram) trong `posts_ready.md`._

- [ ] **Thứ 3, 22/09/2026** — "Củ sắn dây tươi, trước khi thành tinh bột" (video
  `san-day-cu-tuoi.mp4`, 23s, 5 cảnh, có giọng đọc AI + phụ đề Anh):
  - Facebook + Zalo + Instagram (Reels): bản đầy đủ trong posts_ready.md
  - YouTube Shorts: tiêu đề + mô tả đã soạn sẵn — **đợi có kênh mới đăng**
- [ ] **Thứ 6, 25/09/2026** — "Một góc khác của vườn sắn dây" (4 ảnh thật:
  `san-day-vuon-18.jpg`, `-26.jpg`, `-34.jpg`, `-42.jpg`, chưa từng lên bài):
  - Facebook + Zalo + Instagram (carousel 4 ảnh): bản đầy đủ trong posts_ready.md

## Tuần 9

_Xếp 2026-09-06 — 3 nội dung dựng xong hôm nay (buổi sáng trên nương, company intro tiếng Anh, Cam
hâm nóng) nối tiếp đúng nhịp 2 lần/tuần từ mốc 25/09._

- [ ] **Thứ 3, 29/09/2026** — "Một buổi sáng trên nương sắn dây" (video
  `san-day-buoi-sang-tren-nuong.mp4`, 24s, 5 cảnh chưa từng lên bài):
  - Facebook + Zalo + Instagram (Reels): bản đầy đủ trong posts_ready.md
- [ ] **Thứ 6, 02/10/2026** — "Cam Đường Canh: hoa đến quả non" (video
  `cam-duongcanh-ham-nong.mp4`, 31s, hâm nóng trái mùa — KHÔNG chào bán, chỉ cập nhật tiến độ):
  - Facebook + Zalo + Instagram (Reels): bản đầy đủ trong posts_ready.md
- [ ] **Bất kỳ lúc nào** — "Company intro" tiếng Anh (video `san-day-gioi-thieu-xuat-khau.mp4`, 33s):
  - LinkedIn: bản đầy đủ trong posts_ready.md, không cần đúng ngày. Bản nén nhẹ để đính kèm email
    (`docs/assets/san-day-gioi-thieu-xuat-khau-email.mp4`) CHỈ dùng cho Nhóm E, xem
    `.claude/agents/wholesale-export-outreach.md`.

## Từ tuần 10 trở đi

Không lên lịch cứng trước. Ưu tiên chờ có dữ liệu thật (đơn hàng đầu tiên ghi qua app, feedback
khách) để bài tiếp theo có góc độ mới thay vì viết thêm bài chung chung. Giữ nguyên 2 bài Cam
Đường Canh nhấn VietGAP / chín tự nhiên trên cây (chưa dùng, để dành đúng T9-10/2026 theo Giai
đoạn 2 của `KE_HOACH_BAN_HANG.md` — đừng đăng sớm hơn, tránh lặp ý với bài "quả non đậu trên cành"
ở Tuần 2). Video đóng gói cam (`cam-dong-goi-can-than.mp4`, dựng 2026-09-03) **để dành tới tháng
11** khi mùa thật bắt đầu — không đăng sớm, caption đã viết sẵn ở thì quá khứ nên không sai nếu lỡ
đăng sớm, nhưng nội dung hợp lý nhất là đăng đúng lúc mùa mới bắt đầu.

**Ghi chú 2026-09-06**: video mới `cam-duongcanh-ham-nong.mp4` (hoa → quả non, xem checklist ở
trên) VẪN nên đăng sớm hơn (không cần đợi T9-10), vì đây là góc "tiến độ tiếp theo" sau bài đã đăng
Tuần 2 (11/08, "quả non đã đậu trên cành") chứ không lặp lại — quả trong video mới đã lớn hơn hẳn.
2 bài dành riêng T9-10 (VietGAP / chín tự nhiên trên cây) vẫn giữ nguyên, không đụng tới.

## Bài cũ nên bỏ qua hẳn (không đưa vào lịch — đã có bản mới hơn thay thế)

Giữ nguyên trong file, không cần xoá, nhưng khi đăng theo lịch trên thì bỏ qua:
- "Hậu trường sản xuất Tinh Bột Sắn Dây" (07-05)
- "TikTok — Video hậu trường phơi sắn dây" (07-05, chỉ là kịch bản, đã có video thật thay thế)
- "Công dụng / cách dùng Tinh Bột Sắn Dây" (07-03)
- "Mời khách để lại hẹn báo hàng mùa cam" (07-06, đã có bản 26/07 tốt hơn)
