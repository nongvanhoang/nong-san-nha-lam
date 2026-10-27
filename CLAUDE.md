# Thế Hưng Organic (THOC) — Bộ nhớ dự án cho Claude

## ⚠️ ĐỔI THƯƠNG HIỆU 2026-10-19 — đọc trước mọi mục bên dưới

- **Thương hiệu mới: THOC — Hợp tác xã Thế Hưng Organic** (EN: The Hung Organic Cooperative). Người dùng
  chọn **đổi hẳn**, KHÔNG giữ "Nông Sản Nhà Làm". Trên web/bài viết dùng "Thế Hưng Organic"; tên pháp lý
  đầy đủ "Hợp tác xã Thế Hưng Organic" ở footer, JSON-LD, nhãn, hồ sơ. Trụ sở: Thôn Liên Lạc, xã Vũ Lăng,
  Lạng Sơn · GĐ Hà Quang Chiến · mã số HTX: CHƯA có. Đây cũng là chủ thể OCOP (thay "công ty cô chú").
- Tài liệu gốc ở `Tài Liệu Công Ty/` (đã gitignore — có danh sách thành viên + vốn góp, KHÔNG đưa lên đâu
  công khai). Logo web: `docs/assets/logo-thoc-mark.png` (+ `logo-thoc.jpg` bản đầy đủ), cắt từ logo gốc.
- **Chứng nhận hữu cơ**: người dùng báo 2026-10-19 là CÓ, nhưng Claude CHƯA thấy giấy (số, đơn vị cấp,
  phạm vi sản phẩm, hạn). Cho tới khi có giấy: không viết số/đơn vị cấp, không thêm dấu "chứng nhận hữu
  cơ" lên web/bài; tên HTX chứa chữ "Organic" thì giữ nguyên. Câu "Tinh Bột Sắn Dây CHƯA có chứng nhận"
  bên dưới sẽ sửa khi có giấy.
- **Nhãn/ảnh kênh đã đổi (2026-10-19)**: `scripts/tao_nhan_ocop.js` giờ nhúng logo THOC (cắt theo viền bầu
  dục) và điền sẵn "Chịu trách nhiệm: Hợp tác xã Thế Hưng Organic" + địa chỉ trụ sở; tạo thêm
  `nhan-thoc-{500g,1kg}` (bản thường, ẩn ô OCOP) — DÙNG THAY `nhan-say-day-500g/1kg.svg` (bản cũ chỉ còn làm
  nguồn nền kraft + QR cho script, không in nữa). Thẻ quà Tết, thiệp, ảnh bìa Shopee/Facebook/YouTube, ảnh
  đại diện trong `content/kenh_assets/` đã đổi. Còn chỗ đỏ: [SỐ TCB], logo OCOP, mã vạch.
- **Ảnh đại diện mạng xã hội (2026-10-25)**: logo gốc bầu dục bị cắt 2 đầu khi kênh cắt tròn → dùng
  `content/kenh_assets/logo-tron/` (3 bản 1080×1080, tạo bằng `scripts/tao_logo_tron.py`), KHÔNG tải logo bầu dục làm avatar.
- **Bao bì mới (2026-10-25)**: bản in sạch ở `content/nhan_bao_bi/bao-bi-moi/` (túi 500g/1kg 2 mặt, bao 5kg/10kg), dựng
  bằng `node scripts/tao_bao_bi.js` (hình cắt từ thiết kế gốc bằng `scripts/tao_bao_bi_anh.py`). Bản gốc của người thiết kế
  (`thiet-ke-2026-10-25/`) sai dấu + có dấu ORGANIC → KHÔNG in bản gốc. Chữ Ắ của font Be Vietnam Pro rất cao: giữ khoảng
  cách giữa 2 dòng tên, nếu không dấu sắc đè lên dòng trên. Túi 5kg/10kg đã lên web dạng "Nhắn báo giá" (chủ shop duyệt).
- **Trang nội dung (2026-10-25)**: 11 trang (ve-chung-toi, giao-hang-doi-tra, qua-tet-2027, mua-si-san-day,
  cam-nang, 5 bài cẩm nang, en/about) dựng bằng `scripts/tao_trang_noi_dung.py` — sửa chữ ở script rồi chạy lại,
  KHÔNG sửa tay HTML các trang này. Ảnh chia sẻ link: `docs/assets/home/og-*.jpg` từ `make_banners.py` (og-*).
  Video nền trang chủ chỉ tải khi mạng nhanh (source data-src). Hồ sơ Google Maps/Merchant: `content/HO_SO_GOOGLE.md`.
- **Câu chuyện sản xuất khi cuộn (2026-10-27)**: mục ảnh ghim + đổi theo từng bước trên 6 trang (VI/EN trang chủ,
  Sắn Dây, Cam) dựng bằng `node scripts/tao_cau_chuyen_cuon.mjs` — sửa chữ/ảnh ở script rồi chạy lại, KHÔNG sửa tay.
  Ảnh 4:5 ở `docs/assets/story/{sd1-6,cam1-6}-{640,1080}.webp` cắt từ bản gốc trong `Hình Ảnh, Video/`; hiệu ứng ở
  `docs/assets/story.js` + cuối `home.css`. 2 video ngắn cách dùng (`dung-pha/nau.mp4`) trên trang Sắn Dây VI/EN.
  Máy chủ shop tắt hiệu ứng Windows → trình duyệt máy này không phóng ảnh/tự chạy video (bình thường, điện thoại vẫn có).
- **Thông số xuất khẩu sắn dây (chủ shop báo 2026-10-27)**: HSD "2/3 năm" (hiểu là 2–3 năm → web ghi 24 tháng),
  công suất ~10–20 tấn bột/tháng (vì vậy KHÔNG còn viết "small-batch/sản xuất nhỏ"), đặt tối thiểu khách nước ngoài
  100kg, phiếu kiểm nghiệm "cung cấp sau" (khi có → điền chỉ số thật vào `EXPORT_SPEC`). Trang `en/wholesale.html`
  + bản in `en/spec-sheet.html` dựng từ `EXPORT_SPEC`/`EXPORT_QA` trong `scripts/tao_trang_noi_dung.py`; sửa xong
  chạy lại script rồi xuất lại PDF `docs/assets/thoc-kudzu-root-starch-spec-sheet.pdf` (Chrome headless, A4, 1 trang).
  Form xin mẫu gửi qua FormSubmit về hello@ (cần kích hoạt 1 lần, chung với dat-truoc).
- **Mã lô + QR truy xuất (2026-10-27)**: `next_batch_id()` trong nsn_core giờ đặt mã `SD-YYMMDD-NN` / `CAM-YYMMDD-NN`.
  `scripts/ma_lo.py` (xuat → docs/lo/lots.json chỉ gồm mã/sản phẩm/ngày/HSD, KHÔNG số lượng; tem <mã> → tờ tem A4 có QR
  `/lo/?ma=`; qr-bao-bi → QR cố định trên bao bì). Trang tra cứu song ngữ `docs/lo/index.html`. QR cũ trên bao bì trỏ
  nongsannhalam.com → đã thay. Cách dùng cho chủ shop: HUONG_DAN_KHAI_THAC.md mục 10.
- **Xuất PDF/ảnh bằng Chrome headless**: khi Chrome của người dùng đang mở, PHẢI thêm
  `--user-data-dir=<thư mục scratchpad riêng>`, và đường dẫn `--print-to-pdf`/`--screenshot` phải là đường dẫn
  ĐẦY ĐỦ (đường dẫn tương đối bị ghi sai chỗ, lệnh vẫn báo thành công) — gặp thật 2026-10-19.
- **Chưa đổi (cần làm tiếp)**: tên miền thehungorganic.com + email hello@ (giữ tạm), tên trang Facebook/
  Zalo/Shopee (người dùng tự đổi + tải ảnh mới trong `content/kenh_assets/`), video đã dựng có tên cũ,
  artifact "Sổ Đơn Nhà Làm", dấu chứng nhận hữu cơ (chờ giấy).
  Nhiều đoạn bên dưới vẫn ghi "Nông Sản Nhà Làm"/"nhà làm" — hiểu là thương hiệu cũ.
- **Đánh giá thật (2026-10-20)**: shop Shopee "Cam Đường Canh TH" mùa 2025–2026 có 106 đánh giá (97×5★, 6×4★,
  1×3★, 2×1★, TB 4,85). 10 lời khen nguyên văn đã lưu `data/testimonials.json` (tên che như Shopee) và hiện ở mục
  "Khách nói gì" (#danh-gia) trên trang chủ + trang Cam (VI/EN, EN là bản dịch). Video gốc `Đánh Giá Khách Hàng/`
  có tên đăng nhập + mã đơn → gitignore, không đăng. Đã loại đánh giá rác (chép mô tả shop, nói về "chiếc set").
  Phàn nàn đều về **cam dập/hư khi vận chuyển xa** — 1 khách nói báo shop mà không được đền: web giờ hứa "đổi mới/
  hoàn tiền nếu hư do vận chuyển", phải làm đúng. Không gắn schema AggregateRating (đánh giá từ bên thứ ba).
  Lưu ý: cam ĐÃ từng bán trên Shopee (khác ghi chú cũ "không đưa cam lên sàn").
- Túi sắn dây 5kg/10kg đã thêm vào `data/products.json`, `price_vnd: null` — CHƯA đăng lên web/sàn đến
  khi người dùng báo giá.

# (Tên cũ: Nông Sản Nhà Làm)

**Hệ thống vận hành doanh nghiệp 1 người**: `HE_THONG_VAN_HANH_1_NGUOI.md` (từ 2026-10-01) — file
ĐẦU TIÊN nên đọc khi không biết bắt đầu từ đâu, gói gọn 4 mảng (nhịp vận hành hàng ngày/tuần/tháng,
quy trình chuẩn `SOP.md`, tài chính thu-chi-lãi-lỗ, mục tiêu tăng trưởng) thành 1 chỗ, trỏ sang file
chi tiết khi cần. `VIEC_CAN_LAM.md` và `HUONG_DAN_KHAI_THAC.md` vẫn giữ nguyên vai trò riêng (việc
đang treo / cách dùng từng công cụ) — file hệ thống chỉ là lớp trên cùng nối chúng lại.

**Checklist hành động tổng hợp**: `VIEC_CAN_LAM.md` (từ 2026-09-26) — gom mọi việc thật đang treo
(tin nhắn cần gửi, cuộc gọi cần gọi, quyết định cần chốt, tài khoản cần tạo) từ nhiều file rải rác
vào 1 chỗ. Cập nhật (tick `[x]`) file này mỗi khi người dùng báo đã xong việc gì, và thêm việc mới
vào đúng nhóm khi phát sinh — đừng để lại thành rải rác như trước.

**Hướng dẫn khai thác công cụ đã xây**: `HUONG_DAN_KHAI_THAC.md` (từ 2026-09-28) — trả lời "đã có
sẵn công cụ gì, dùng thế nào mỗi ngày/mỗi tuần" (khác `VIEC_CAN_LAM.md` là liệt kê việc còn treo).
Cập nhật file này mỗi khi thêm 1 hệ thống/công cụ mới mà người dùng sẽ cần tự dùng lại sau này.

Đây là dự án kinh doanh nông sản gia đình. Khi làm việc trong thư mục này, Claude đóng vai trò
trợ lý riêng cho chủ shop: viết nội dung quảng cáo, ghi sổ đơn hàng, ghi sổ sản xuất, tính báo cáo.
Không có script nào tự động gọi API trả phí — mọi nội dung do Claude tạo trực tiếp trong phiên chat.

## Sản phẩm

1. **Tinh Bột Sắn Dây** — làm thủ công tại nhà, lọc thủ công và sấy bằng lò sấy chuyên dụng (đã đầu
   tư lò sấy, KHÔNG còn phơi nắng tự nhiên nữa — chuyển hẳn từ 2026-08-11), không hoá chất, không
   chất tẩy trắng. Bán quanh năm (đã chế biến, bảo quản được lâu).
2. **Cam Đường Canh** — trồng bởi gia đình, thành viên **Hợp tác xã Thế Hưng Organic — TÊN CŨ là Hợp Tác Xã Cây Ăn Quả
   Nhung Giang** (cùng một HTX, đã đổi tên — người dùng xác nhận 2026-10-20; giấy VietGAP vẫn in tên cũ), tỉnh
   Lạng Sơn, đạt **chứng nhận VietGAP** số 112/CN-TĐC-TT-20-0012 (cấp 23/12/2025, hiệu lực đến
   22/12/2028, do NATEK JSC cấp, phù hợp TCVN 11892-1:2017). Thu hoạch theo mùa (khoảng tháng 11
   âm lịch đến tháng 1 năm sau). Ngoài mùa thu hoạch KHÔNG chào bán sản phẩm này — nếu khách hỏi
   trái mùa, trả lời rằng đang hết mùa, hẹn mùa sau, có thể gợi ý đăng ký nhận tin khi có hàng.

Giá, đơn vị, quy cách đóng gói cụ thể lấy từ `data/products.json`. Nếu trường nào ghi
`"CẦN CẬP NHẬT"`, nghĩa là chưa có số liệu thật — hỏi lại người dùng thay vì tự bịa ra giá/số liệu.

## Định hướng xuất khẩu

Mục tiêu dài hạn là tìm khách sỉ/nhập khẩu nước ngoài, nhưng chỉ cho **Tinh Bột Sắn Dây** (dạng bột
khô, dễ vận chuyển xa). **Cam Đường Canh là trái tươi, hiện KHÔNG chào xuất khẩu** — dù đã có chứng
nhận VietGAP (chứng nhận chất lượng trồng trọt), xuất khẩu trái cây tươi còn cần thêm giấy kiểm
dịch thực vật và thủ tục hải quan riêng mà cơ sở chưa có. VietGAP là điểm cộng uy tín rất tốt để
nói với khách trong nước và làm nền tảng xin thêm giấy tờ sau này, nhưng chưa đủ để xuất khẩu trái
tươi ngay. Nếu khách nước ngoài hỏi mua cam, trả lời rõ ràng là hiện chỉ giao trong nước.

**Chứng nhận thật đã có**: Cam Đường Canh — VietGAP (xem chi tiết ở mục Sản phẩm trên). **Tinh Bột
Sắn Dây — CHƯA có chứng nhận chính thức nào** (không phải VietGAP, không ATTP/HACCP). Không tự thêm/
gợi ý chứng nhận cho Tinh Bột Sắn Dây. Với Tinh Bột Sắn Dây, định vị trung thực là "gia đình sản
xuất nhỏ, thủ công" (small-batch, family-made) — đây là điểm mạnh marketing hợp lệ, không cần
chứng nhận giả.

**Quan trọng về quyền riêng tư**: giấy chứng nhận VietGAP liệt kê tên/địa chỉ/diện tích của 3 thành
viên KHÁC trong hợp tác xã (không phải người nhà). Người dùng đã quyết định KHÔNG đăng file PDF gốc
công khai — chỉ nêu số chứng nhận, tên HTX, ngày hiệu lực bằng chữ trên website. Không tự ý đăng
file PDF gốc hay tên/địa chỉ của 3 thành viên kia lên bất kỳ đâu công khai.

## Tông giọng khi viết nội dung

- Gần gũi, chân thật, xưng "nhà mình" / "shop mình" — không quảng cáo kiểu sáo rỗng, không phóng đại
  công dụng y tế (tuyệt đối không nói tinh bột sắn dây "chữa bệnh" — chỉ nói công dụng dân gian như
  giải nhiệt, mát gan, hay dùng nấu chè/pha nước uống).
- Luôn nhấn mạnh yếu tố "nhà làm / tự nhiên / không hoá chất" và nguồn gốc rõ ràng.
- Ưu tiên câu ngắn, dễ đọc trên điện thoại, có thể kèm 1-2 emoji tự nhiên (🍊, 🌾) nhưng không lạm dụng.
- Luôn có lời kêu gọi hành động cuối bài (nhắn Zalo/Facebook để đặt hàng).

## Việc Claude thường được nhờ làm

- **Chuẩn chất lượng content (từ 2026-09-21)**: mọi bài viết mới đọc `content/templates/chuan_chat_luong_content.md`
  trước — đa dạng hook mở đầu (không mặc định "emoji + TIÊU ĐỀ IN HOA"), bài thuần cập nhật/hậu
  trường chốt bằng câu hỏi mời bình luận thay vì luôn nhắc giá, hashtag Instagram đổi theo đúng chủ
  đề thay vì lặp y hệt bộ tag cũ mọi bài.
- **Viết caption/bài đăng**: dùng góc độ và cấu trúc trong `content/templates/` (facebook.md, zalo.md,
  shopee_tiktok.md). Sau khi viết xong, hỏi người dùng có muốn lưu vào `content/posts_ready.md` không.
  Khi người dùng muốn nội dung cho NHIỀU kênh cùng lúc từ một yêu cầu, dùng subagent
  `.claude/agents/sales-content-writer.md` thay vì soạn thủ công từng kênh.
- **Video cho mọi bài (mặc định từ 2026-08-18)**: mỗi bài viết đều nên có video thật đi kèm để đăng
  đa nền tảng — không cần người dùng nhắc riêng, luôn chủ động tra `Hình Ảnh, Video/` xem có clip
  thật khớp chủ đề không rồi dựng bằng `content/video/make_process_video.py`. Nếu chủ đề không có
  clip thật nào khớp (thường gặp ở bài công thức/cách dùng), nói rõ là chỉ có ảnh, không tự dựng/bịa
  video giả — đây là giới hạn thật của kho tư liệu, không phải lỗi.
- **Giọng đọc AI + phụ đề tiếng Anh (từ 2026-09-03, tuỳ chọn)**: `make_process_video.py` hỗ trợ thêm
  giọng đọc AI tiếng Việt (Edge-TTS, miễn phí — không vi phạm quy tắc "không gọi API trả phí" ở
  dưới) và phụ đề tiếng Anh chèn cứng, dùng khi bài hướng tới LinkedIn/Instagram/TikTok/YouTube quốc
  tế. HÌNH ẢNH vẫn luôn 100% clip thật — chỉ thêm lớp âm thanh/chữ, không dựng cảnh giả. Chi tiết
  cách bật 2 field `narration`/`text_en` xem `content/video/configs/README.md`.
- **Lưu ý môi trường (2026-08-02)**: lệnh `python`/`py` trên máy này không trỏ đúng Python thật (bị Windows Store
  alias/launcher lỗi chặn). Python thật nằm ở `C:\Users\Admin\AppData\Local\Python\bin\python.exe` — dùng đường
  dẫn đầy đủ này khi chạy các script bên dưới, trừ khi người dùng xác nhận đã sửa PATH.
- **Thư viện Media (2026-09-22)**: tab mới trong app quản lý local — quét toàn bộ ảnh/video trong
  `Hình Ảnh, Video/`, `docs/assets/`, `content/video/output/` (361 file tính đến lúc thêm), đối
  chiếu tên file với `content/posts_ready.md` để tự gắn nhãn "Đã dùng" (kèm bài nào) hay "Chưa
  dùng", cho tìm/lọc theo tên/sản phẩm/loại, bấm vào 1 ảnh/video để copy đường dẫn tương đối vào
  clipboard. Giải quyết đúng việc tốn thời gian dò tay xem 1 file đã lên bài chưa/đường dẫn đầy đủ
  là gì. Logic quét ở `scan_media_library()` trong `nsn_core.py`, phục vụ file qua route
  `/media/<đường dẫn>` trong `webapp.py` (có chặn path traversal, hỗ trợ HTTP Range để xem video mượt).
- **App quản lý local (2026-08-02, thêm mục "Bán hàng hôm nay" 2026-09-08, thêm tab "Tổng quan"
  2026-10-01 làm màn hình mặc định)**: tab "Tổng quan" gộp bài cần đăng hôm nay + hạn chót sắp tới
  (đọc từ mục `## ⏰` đầu `VIEC_CAN_LAM.md` qua `find_upcoming_deadlines()`) + cảnh báo tồn kho +
  tài chính tháng này + khách quen lâu chưa quay lại (`find_customers_to_followup()`, ngưỡng mặc
  định 21 ngày) + **"Hôm nay nên gọi/nhắn B2B"** (`get_today_call_list()`, 10 lead "Chưa liên hệ" sắp
  theo đúng thứ tự ưu tiên Giai đoạn 0→4, thêm 2026-10-01 — tự rơi khỏi danh sách khi đổi trạng thái,
  không cần con trỏ/hàng đợi riêng như bài đăng) — tất cả gộp trong `compute_today_overview()`. Ngoài
  việc nhờ Claude chạy
  script qua chat, người dùng có thể tự bấm `MO_APP_QUAN_LY.bat` để mở app web local (`scripts/webapp.py`,
  cổng 8943) — giao diện có 5 mục: ghi đơn hàng, ghi mẻ sản xuất, báo cáo, sửa giá, và **Bán hàng hôm nay**
  (đọc live từ `LICH_DANG_BAI.md`/`content/posts_ready.md` để hiện đúng bài cần đăng hôm nay kèm nút copy,
  với nút "Đã đăng" ghi vào `data/posted_log.csv` để tự nhớ trong ngày, và bảng khách B2B đọc trực tiếp từ
  `DANH_SACH_KHACH_HANG_B2B.csv` (tự xếp theo đúng thứ tự ưu tiên Giai đoạn 0→4 trong
  `KE_HOACH_KHAI_THAC_B2B.md`) với nút gọi/email + cập nhật trạng thái ngay tại chỗ — luôn khớp CSV 100%
  vì đọc live, không như bản hosted "Sổ Gọi Khách" cần đồng bộ tay). Logic
  dùng chung nằm ở `scripts/nsn_core.py`; 3 script CLI cũ (`add_order.py`, `add_batch.py`, `weekly_report.py`)
  giờ chỉ là wrapper mỏng gọi `nsn_core.py` — khi sửa logic ghi sổ/báo cáo, sửa ở `nsn_core.py` để cả CLI và
  app web cùng nhất quán, đừng sửa riêng từng nơi. **Quan trọng khi sửa các hàm ghi CSV/JSON trong
  `nsn_core.py`**: LUÔN ghi ra file tạm rồi `os.replace()` vào file thật (không ghi đè trực tiếp) — sự cố
  thật 2026-09-08: 1 dòng dữ liệu cũ lỗi định dạng (thiếu quote quanh field có dấu phẩy) khiến
  `csv.DictWriter` ném lỗi giữa chừng, ghi đè trực tiếp làm mất gần hết 500 dòng `DANH_SACH_KHACH_HANG_B2B.csv`
  (khôi phục được từ backup trong scratchpad, không mất vĩnh viễn, nhưng phải luôn phòng trước bằng ghi an toàn).
- **Ghi đơn hàng mới**: chạy `python scripts/add_order.py` với các tham số phù hợp (xem `--help`).
  Không tự suy diễn số liệu nếu người dùng chưa cung cấp đủ (khách, sản phẩm, số lượng, đơn giá, kênh).
  QUAN TRỌNG: luôn quy đổi `--qty` ra kg (đơn vị gốc, không phải số thùng/túi) để
  `weekly_report.py` so sánh tồn kho đúng — ví dụ khách mua "2 thùng cam 10kg" thì ghi
  `--qty 20 --unit kg`, không ghi `--qty 2 --unit thùng`.
- **Sổ địa chỉ khách (`data/customers.csv`, thêm 2026-10-01)**: `add_order()` tự lưu SĐT/địa chỉ vào
  đây khi được cung cấp (`upsert_customer()`), và `find_customer()` tra lại cho lần ghi đơn sau — app
  tự gọi khi gõ tên khách vào ô "Ghi đơn hàng" (`GET /api/customers/lookup?name=...`). Khớp theo tên
  chính xác (không phân biệt hoa/thường), không tự động gộp 2 tên gọi khác nhau của cùng 1 khách.
- **Ghi mẻ sản xuất/thu hoạch**: chạy `python scripts/add_batch.py`, cũng luôn quy ra kg.
- **Báo cáo doanh thu/sản lượng/tồn kho**: chạy `python scripts/weekly_report.py` — báo cáo có cả
  phần cảnh báo tồn kho (tổng sản xuất trừ tổng đã bán, toàn thời gian). Nếu thấy cảnh báo
  "SẮP HẾT HÀNG" hoặc "ĐÃ NHẬN ĐƠN VƯỢT SỐ SẢN XUẤT", chủ động báo cho người dùng.
- **Cập nhật giá/sản phẩm**: sửa trực tiếp `data/products.json` khi người dùng cho số liệu mới.
- **Website**: `docs/index.html` (tiếng Việt) và `docs/en/index.html` (tiếng Anh, cho khách quốc
  tế/đối tác xuất khẩu) — thư mục tên `docs/` vì GitHub Pages yêu cầu vậy. Sửa nội dung/giá ở
  CẢ HAI file khi cần đồng bộ với `data/products.json`, đừng chỉ sửa 1 bản rồi quên bản kia.
  Trang tiếng Anh KHÔNG cần mục Shopee/TikTok Shop (đây là kênh bán lẻ nội địa Việt Nam, không phục
  vụ khách quốc tế/đối tác sỉ-xuất khẩu).
- **Ghi chú "sắp ra mắt" (Shopee/TikTok Shop, email, WhatsApp)**: khi có link/số liệu thật, thay
  chữ "đang cập nhật"/"sắp ra mắt" bằng link thật (giống cách Facebook đang để dạng comment chờ link
  thật). Không tự bịa link gian hàng khi chưa có.

## Kênh bán hàng

- **Shopee/TikTok Shop: đã quyết định mở (2026-07-05), chỉ cho Tinh Bột Sắn Dây.** Không đưa Cam
  Đường Canh lên sàn (trái tươi bán theo thùng 5-10kg, khó đáp ứng SLA giao hàng/đổi trả của sàn,
  phí sàn ăn vào biên lợi nhuận mỏng của mặt hàng theo mùa). Chi tiết ở `KE_HOACH_BAN_HANG.md`.
- **B2B/sàn xuất khẩu (Alibaba, sàn giao dịch nông sản...): chưa mở.** Lý do: Tinh Bột Sắn Dây chưa
  có chứng nhận ATTP/HACCP, Cam Đường Canh chưa có giấy kiểm dịch thực vật để xuất khẩu trái tươi.
  Ưu tiên xin ATTP cho Tinh Bột Sắn Dây trước khi tính đến B2B/xuất khẩu.

## Chào hàng Nhóm E cá nhân hoá + nội dung gian hàng Shopee/TikTok Shop (từ 2026-09-28)

- **`content/templates/chao_hang_nhom_e_ca_nhan_hoa.md`**: bản viết sẵn nguyên văn cho từng lead
  trong 32 lead Nhóm E (thay vì phải tự điền `[tên shop]`/`[tên nước]` vào
  `chao_hang_nhom_e_quoc_te.md` mỗi lần) — sắp theo thứ tự rủi ro hải quan tăng dần (Nhật trước, Úc
  cuối), có ghi kênh liên hệ đúng thật (email/điện thoại/Facebook) theo `DANH_SACH_KHACH_HANG_B2B.csv`,
  và ghi chú riêng cho các lead đặc biệt (Đồng Xuân = đầu mối BQL không phải quầy hàng, Miss Linh/
  Tamda = xin làm nhà cung cấp chứ không chào mẫu thường, Úc = chưa gửi mẫu cho đến khi tự tra BICON,
  2 lead Mỹ = dịch vụ vận chuyển chứ không phải khách hàng).
- **`HO_SO_MANG_XA_HOI.md` mục 3** bổ sung "Tên sản phẩm + phân loại hàng khi đăng thật": tiêu đề
  SEO sẵn dùng, bảng phân loại 0.5kg/155k-1kg theo đúng giá `products.json`, gợi ý từ khoá chọn
  ngành hàng, và 4 câu Q&A soạn sẵn cho khung chat của sàn (hạn dùng đánh dấu **[CẦN BẠN XÁC NHẬN]**
  vì chưa có mốc kiểm nghiệm chính thức — không bịa số ngày cụ thể).

## Thẻ treo Quà Tết + Thiệp chúc Tết (từ 2026-10-03)

- `content/nhan_bao_bi/the-qua-tet.svg` — thẻ treo 80mm×120mm cho combo quà Tết (Cam Đường Canh +
  Tinh Bột Sắn Dây), đúng phong cách Mộc & Thật. Có 2 dòng trống "Gói:"/"Giá:" viết tay — dùng chung
  được cho mọi mức giá/gói mà không cần in lại.
- `content/nhan_bao_bi/thiep-chuc-tet.svg` — thiệp chúc Tết 100mm×150mm, mặt trước in sẵn lời chúc
  ngắn + thương hiệu, mặt sau CHỦ ĐỊNH để trống (giấy trơn) để viết tay lời nhắn riêng từng khách.

**⚠️ Lỗi font Georgia đã phát hiện (2026-10-03, đã sửa ở cả 4 file trên)**: font Georgia (cả bản
thường lẫn in nghiêng) trên máy này KHÔNG hiển thị đúng các chữ có dấu "â" + thanh điệu (ấ, ầ, ẩ, ẫ,
ậ) — ví dụ "tấm" thành "tâ´m", "đầu" thành "đâ`u" (dấu tách rời khỏi chữ thay vì đè lên). Đã test xác
nhận Cambria/Times New Roman/Arial đều hiển thị đúng, chỉ Georgia sai. **Quy tắc từ nay**: mọi chữ
nghiêng dùng `font-family="Cambria, Georgia, serif"` (Cambria trước), KHÔNG dùng riêng
`"Georgia, serif"` — đã áp dụng lại cho cả `nhan-say-day-500g.svg`/`-1kg.svg` dù nội dung hiện tại
chưa dính lỗi (phòng khi sửa chữ sau này). Rủi ro này cũng áp dụng khi xưởng in mở file bằng
Illustrator nếu máy họ thiếu đúng glyph này trong Georgia — một lý do nữa nên kiểm tra kỹ bản in thử
đầu tiên trước khi in cả lô.

**Xem trước SVG bằng Chrome headless** (không cần Illustrator): `chrome --headless --screenshot=out.png
--window-size=320,480 --force-device-scale-factor=4 "file:///<đường dẫn tuyệt đối>/file.svg"` rồi mở
file PNG. Dùng được cho mọi file trong `content/nhan_bao_bi/`.

**Xuất PDF đúng khổ thật (đã giải quyết 2026-10-10)**: KHÔNG in thẳng file SVG (ra khổ Letter/A4 +
header/footer rác). Bọc SVG trong 1 file HTML nhỏ có `@page{size:<W>mm <H>mm;margin:0}` và
`<img src="file:///...svg" style="width:<W>mm;height:<H>mm">`, rồi chạy `chrome --headless=new
--allow-file-access-from-files --no-pdf-header-footer --print-to-pdf=out.pdf file:///.../wrap.html`.
Luôn kiểm tra lại `MediaBox` trong PDF (pt ÷ 2.835 = mm) và `/Count 1` (đúng 1 trang). Đã xuất bằng
cách này: thẻ treo (80×120mm), thiệp (100×150mm), và bộ nhãn OCOP bên dưới.

## Nhãn bản OCOP (từ 2026-10-10)

`nhan-say-day-{1kg,500g,250g}-ocop` + `tem-phu-mat-sau` (SVG + PDF) trong `content/nhan_bao_bi/`,
tạo bằng `node scripts/tao_nhan_ocop.js content/nhan_bao_bi` (đọc logo + QR từ nhãn 500g gốc). Chữ
đỏ gạch là chỗ cần điền (tên/địa chỉ công ty cô chú, số tự công bố, logo OCOP chính thức, mã vạch,
QR truy xuất) — chi tiết ở đầu `BAO_BI_DE_XUAT.md`. Chỉ dùng khi đã thật sự có chứng nhận OCOP;
trước đó vẫn in bản cũ `nhan-say-day-500g/1kg`. Không bao giờ tự vẽ logo OCOP hay điền số sao/mã
vạch/số TCB khi chưa có giấy tờ thật.

## Đóng thương hiệu ảnh không cần Canva (từ 2026-09-25)

`content/video/make_branded_photo.py <ảnh gốc> "<chú thích>" <ảnh ra>` — dùng ffmpeg (đã cài, không
cần thư viện Python thêm) để tự thêm logo tròn góc trên phải + dải chú thích trắng-trên-nền-đen ở
dưới, đúng y phong cách chữ đè đã dùng trong video (`make_process_video.py` — cùng font Cambria
Bold, cùng tỉ lệ dải chữ). Dùng khi cần bộ ảnh đồng bộ thương hiệu cho 1 kênh (đã dùng cho 7 ảnh gian
hàng Shopee/TikTok Shop, xem `HO_SO_MANG_XA_HOI.md`) mà không có Canva. Lưu ý: PHẢI giữ
`expansion=none` trên drawtext nếu chú thích có ký tự "%" — nếu không, cả dòng chữ biến mất im lặng
(bug đã gặp và tránh sẵn trong `make_process_video.py`, script này áp dụng lại đúng cách né đó).

## Bản tin tuần tự động (từ 2026-09-25, thêm mục nhắc-việc 2026-10-01)

Windows Task Scheduler (`NongSanNhaLam_WeeklyDigest`, mỗi thứ Hai 9h sáng, chạy local — cùng cơ chế
với mục nhắc đăng bài bên dưới) tự chạy `scripts/weekly_digest.bat` → gộp `weekly_report.py
--nhac-viec` (hạn chót từ `VIEC_CAN_LAM.md` + cảnh báo tồn kho + khách quen lâu chưa quay lại — cùng
tín hiệu với tab "Tổng quan" trong app, nhưng đẩy chủ động (push) thay vì phải tự mở app (pull)) +
`weekly_report.py --days 7` + `weekly_report.py --khach-quen` → ghi ra `BAO_CAO_TUAN.txt` → tự mở
Notepad. Mục đích: báo cáo thật khi đã có đơn hàng, tự nhắc thụ động hàng tuần nếu vẫn chưa ghi đơn
nào (số 0 tự hiện ra thay vì phải nhắc lại trong chat), VÀ không bỏ lỡ hạn chót/khách cần nhắn lại dù
không nhớ mở app. Kiểm tra/xoá: `schtasks /query /tn NongSanNhaLam_WeeklyDigest` /
`schtasks /delete /tn NongSanNhaLam_WeeklyDigest /f`.

## Kiểm tra sức khoẻ hệ thống (từ 2026-10-01, thêm an toàn git + backup 2026-10-02)

`python scripts/kiem_tra_he_thong.py` — 1 lệnh kiểm tra 7 việc: lịch tự động, hàng đợi đăng bài còn
đủ bao lâu, file dữ liệu đọc được không, **mọi file có dữ liệu khách/kinh doanh thật đã nằm trong
`.gitignore` chưa** (tránh lặp lại sự cố lộ dữ liệu khách công khai lên GitHub), **đã có bản backup
OneDrive chưa**, mục tiêu tháng đã đặt chưa, hạn chót nào sắp tới. Chạy hàng tháng (SOP.md mục 11)
hoặc bất cứ khi nào nghi ngờ có gì đó hỏng. 2 kiểm tra an toàn git/backup được thêm sau khi phát hiện
thật `data/customers.csv`/`data/expenses.csv` suýt bị lộ vì quên thêm vào `.gitignore` khi mới xây
(2026-10-02) — đừng xoá 2 mục này dù có vẻ thừa, đây là lớp phòng vệ cho đúng loại lỗi đã từng xảy ra.

## Nhắc đăng bài đều đặn 3 ngày/lần (từ 2026-09-22)

**Chỉ là hệ thống NHẮC, không tự động đăng** — đúng luật cứng "không tự động đăng bài" bên dưới.
Windows Task Scheduler (`NongSanNhaLam_SocialReminder`, chạy local trên máy, KHÔNG phải cloud
routine — cloud routine không đọc được file/Python local) cứ mỗi 3 ngày (9h sáng) tự chạy
`scripts/remind_social_post.bat` → gọi `scripts/next_social_post.py` → lấy đúng bài tiếp theo trong
`data/social_queue.json` (theo con trỏ `data/social_queue_state.json`, tự tăng sau mỗi lần chạy,
không phụ thuộc người dùng đã đăng thật hay chưa) → ghi ra `BAI_DANG_HOM_NAY.txt` → tự mở Notepad.

Hàng đợi hiện có 27 mục (11 mục cũ + 13 mục thêm 2026-10-10 theo `CHIEN_DICH_TET_2027.md`: sắn dây
quanh năm, "hẹn báo hàng mùa cam" 31/10 + 12/11, Bài A hộp quà Tết 15/11 + 24/11 — **phải điền giá
trước khi đăng**, Bài B quà Tết doanh nghiệp 18/11 + 30/11) — từ 2026-10-10 thêm 3 mục "vào mùa cam" (nhắn riêng danh sách chờ → Giới thiệu Cam → chín tự nhiên, nhắc
~03/12, 06/12, 09/12 — chỉ đăng khi cam đã hái thật). Bài D đếm ngược Tết CHƯA vào hàng đợi (chờ chốt hạn
giao cuối). Cách thêm mục vào `data/social_queue.json` (mỗi mục: `topic_keyword`
khớp đúng 1 phần tiêu đề trong `posts_ready.md`, `channels` là danh sách kênh muốn lấy — lưu ý khớp
theo đúng tiền tố tiêu đề, vd bài có tiêu đề bắt đầu "Zalo/Facebook — ..." phải dùng channel
`"Zalo/Facebook"` chứ không phải `"Facebook"` riêng, xem logic `find_block()` trong
`next_social_post.py`). Kiểm tra/sửa task: `schtasks /query /tn NongSanNhaLam_SocialReminder`, xoá
bằng `schtasks /delete /tn NongSanNhaLam_SocialReminder /f`.

## Xin & lưu đánh giá khách hàng (từ 2026-09-20)

- Mẫu tin nhắn xin đánh giá: `content/templates/zalo.md` mục 5 — chỉ gửi cho khách đã mua ≥2 lần
  hoặc đã phản hồi tích cực, gửi sau tin cảm ơn vài ngày.
- Khi khách trả lời qua chat, Claude thêm nguyên văn vào `data/testimonials.json` (không sửa chữ,
  không bịa thêm nếu khách chưa gửi) rồi hỏi người dùng có muốn đăng lên website không.
- Chỉ thêm mục "Khách nói gì" lên `docs/san-day.html`/`docs/cam-duong-canh.html` khi đã có **ít nhất
  1 đánh giá thật** — không đăng section trống hay bịa đánh giá mẫu, vì sai với nguyên tắc trung thực
  của cả dự án.

## Công cụ nghiên cứu thị trường (Exa + browser-act, từ 2026-09-18)

- **Exa AI** (`web_search_exa`/`web_fetch_exa`, dùng ngay trong phiên chat khi được hỏi): nghiên cứu
  giá thị trường/đối thủ, tìm kênh bán mới (nhóm chợ B2B, quán chè, nhà hàng), tìm xu hướng để viết
  content. Không nhúng vào script tự động lặp lại — chỉ dùng tương tác theo yêu cầu, không vi phạm
  luật "không gọi API AI trả phí trong script" vì đây là Claude tự tra cứu trong chat, không phải
  script tự chạy.
- **browser-act** (`stealth-extract`/`screenshot`, CHỈ CHẾ ĐỘ ĐỌC): soi giá đối thủ trên
  Shopee/chợ online, hoặc chụp ảnh kiểm tra `docs/index.html`/`docs/en/index.html` hiển thị đúng.
  **TUYỆT ĐỐI KHÔNG** dùng để đăng nhập, đăng bài, bấm nút mua/đặt hàng hay bất kỳ hành động ghi/
  đổi trạng thái nào trên Facebook/Zalo/Shopee/TikTok Shop — vi phạm thẳng luật "không tự động đăng
  bài" bên dưới.

## Giới hạn đã thống nhất với người dùng

- KHÔNG tự động đăng bài lên Facebook/Zalo/Shopee/TikTok Shop (rủi ro vi phạm điều khoản chống bot +
  cần API key trả phí). Nội dung tạo ra để người dùng tự copy-paste đăng tay.
- KHÔNG gọi API AI trả phí bên ngoài (không có tích hợp OpenAI/Anthropic API riêng trong scripts).
- Website đã deploy qua GitHub Pages (repo public `nongvanhoang/nong-san-nha-lam`, thư mục `docs/`).
  Mỗi lần push lên nhánh `main`, GitHub tự cập nhật trang sau vài phút.
