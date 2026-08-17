# Kế Hoạch Bán Hàng — Nông Sản Nhà Làm

_Cập nhật: 2026-07-03. Xem lại và điều chỉnh khi có số liệu đơn hàng thực tế (`data/orders.csv`)._

## Bối cảnh hiện tại

- **Tinh Bột Sắn Dây**: bán quanh năm, đang đúng mùa hè — nhu cầu giải nhiệt cao. Đây là sản phẩm
  chủ lực để đẩy mạnh **ngay bây giờ**.
- **Cam Đường Canh**: đang **trái mùa** (mùa thu hoạch ~tháng 11 âm lịch - tháng 1 năm sau, tức
  khoảng cuối 2026 - đầu 2027). Không chào bán lúc này, nhưng có thể bắt đầu "hâm nóng" khách hàng
  trước mùa.
- `data/orders.csv` và `data/production_log.csv` hiện **chưa có dữ liệu** — chưa ghi nhận đơn hàng
  nào. Ưu tiên bắt đầu ghi sổ ngay khi có đơn để theo dõi doanh thu/tồn kho chính xác từ đầu.
- Đã có 5 caption mẫu sẵn sàng đăng trong `content/posts_ready.md`.
- Website đã live (VN + EN), nhưng còn thiếu Facebook link, email, WhatsApp — đang để "CẦN CẬP NHẬT".
- **2026-07-26: đã thay xong ảnh minh hoạ stock bằng ảnh thật** (chọn từ 269 ảnh/video nhà chụp
  ngày 2026-07-25, xem `docs/assets/CREDITS.md`). Mục 2 ở Giai đoạn 1 dưới đây coi như xong.

## Giai đoạn 1 — Tháng 7-8/2026: Đẩy mạnh Tinh Bột Sắn Dây (mùa hè)

**Mục tiêu**: tăng đơn hàng đều đặn qua Zalo/Facebook, xây dựng uy tín bằng nội dung thật.

1. **Đăng bài đều đặn 2-3 lần/tuần** trên Facebook + Zalo, xoay vòng góc độ: giới thiệu sản phẩm,
   công dụng/cách dùng, hậu trường sản xuất (lọc/phơi), feedback khách cũ. Dùng caption có sẵn
   trong `content/posts_ready.md` làm khung, nhờ Claude viết thêm bài mới khi cần góc độ khác.
2. **✅ Đã xong (2026-07-26): ảnh/video thật** — đã thay 3 ảnh minh hoạ stock trong `docs/assets/`
   bằng ảnh thật chụp tại vườn/xưởng nhà mình. Còn 265+ ảnh/video thật chưa dùng tới trong
   `Hình Ảnh, Video/` — có thể dùng thêm cho caption Facebook/Zalo hoặc video ngắn TikTok/Reels.
3. **Hoàn thiện thông tin liên hệ**: điền Facebook link, email, WhatsApp vào `data/products.json`
   và bật lại trên cả 2 trang web (VN/EN) — quan trọng vì khách quốc tế không dùng được Zalo.
4. **Ghi sổ đầy đủ**: mỗi đơn hàng ghi ngay bằng `add_order.py` (nhớ quy đổi ra kg), mỗi mẻ sản xuất
   ghi bằng `add_batch.py`. Chạy `weekly_report.py` hàng tuần để theo dõi doanh thu và cảnh báo tồn kho.
5. **Đã quyết định (2026-07-05): mở Shopee/TikTok Shop, chỉ cho Tinh Bột Sắn Dây.** Sản phẩm khô, dễ
   đóng gói/ship qua sàn, đã có mô tả sản phẩm soạn sẵn trong `content/templates/shopee_tiktok.md`.
   **Không đưa Cam Đường Canh lên sàn** — trái tươi bán theo thùng 5-10kg khó đáp ứng SLA giao hàng/
   đổi trả của sàn, phí sàn ăn sâu vào biên lợi nhuận vốn đã mỏng của mặt hàng theo mùa ngắn. Việc
   đăng ký gian hàng cần bạn tự làm (Claude không tạo tài khoản bán hàng hộ được).
6. **B2B/sàn xuất khẩu (Alibaba, sàn giao dịch nông sản...): chưa mở, để giai đoạn sau.** Lý do:
   Tinh Bột Sắn Dây chưa có chứng nhận ATTP/HACCP (khách B2B/nhập khẩu nghiêm túc thường yêu cầu),
   Cam Đường Canh chưa có giấy kiểm dịch thực vật để xuất khẩu trái tươi. Việc cần làm trước: xin
   chứng nhận ATTP cho Tinh Bột Sắn Dây, rồi mới xem xét mở kênh B2B/xuất khẩu.

## Giai đoạn 2 — Tháng 9-10/2026: Chuẩn bị & hâm nóng khách cho mùa Cam

**Mục tiêu**: xây danh sách khách quan tâm trước, để khi vào mùa là bán được ngay, tránh bị động.

1. Đăng 1-2 bài "sắp vào mùa cam" nhấn mạnh chứng nhận **VietGAP thật** (số 112/CN-TĐC-TT-20-0012) —
   đây là điểm khác biệt lớn so với cam trôi nổi ngoài chợ, nên khai thác kỹ trong nội dung.
2. Mời khách để lại Zalo/inbox để "báo khi có hàng" — tạo danh sách chờ, khi vào mùa nhắn trước tiên
   cho nhóm này (tăng tỷ lệ chốt đơn sớm, giảm rủi ro tồn kho cuối mùa).
3. Chụp thêm ảnh/video vườn cam thật (cây, quả, quá trình chăm sóc) để dùng khi vào mùa.
4. Bài Cam Đường Canh đã soạn sẵn trong `content/posts_ready.md`, có thể nhờ Claude viết thêm
   2-3 bài với góc độ khác (ví dụ nhấn VietGAP, nhấn "chín tự nhiên trên cây") để không lặp bài.

## Giai đoạn 3 — Tháng 11/2026 - Tháng 1/2027: Cao điểm mùa Cam Đường Canh

**Mục tiêu**: bán hết sản lượng thu hoạch, tận dụng đúng cửa sổ mùa vụ ngắn.

1. Đăng bài chính thức (bài đã soạn trước, đánh dấu "chỉ đăng khi vào mùa cam thật") ngay khi có
   hàng, ưu tiên nhắn trước cho danh sách khách đã chờ từ Giai đoạn 2.
2. Bán chéo: khách hỏi mua cam thì giới thiệu thêm Tinh Bột Sắn Dây (bán quanh năm) để tăng giá trị
   đơn hàng.
3. Theo dõi sát tồn kho qua `weekly_report.py` — vì chỉ bán theo thùng 5kg/10kg và mùa vụ ngắn, cần
   chủ động báo hết mùa/hết hàng đúng lúc, tránh nhận đơn vượt sản lượng thực tế.
4. Cuối mùa, nếu còn tồn, có thể ưu tiên khách quen / giảm nhẹ để bán hết trước khi cam hết mùa
   (không thúc chín trái nên không giữ được lâu ngoài mùa).

## Ma trận kênh B2B + B2C, trong nước + nước ngoài (cập nhật 2026-08-12)

_Thay cho khung "Tầng 1→2→3 làm tuần tự" cũ — theo yêu cầu triển khai đồng thời, tách theo **cái gì
làm song song được ngay** vs **cái gì bị luật/thực tế chặn thật, không thể bỏ qua**. Chi tiết từng
kênh đã tra cứu qua web thật (không đoán), nguồn ghi kèm._

### Nhóm A — Làm song song ngay, không chờ gì cả

| Kênh | Loại | Trạng thái / việc cần làm |
|---|---|---|
| Zalo/Facebook cá nhân | B2C trong nước | Đang chạy — vấn đề thật là **chưa đăng đều** (xem `LICH_DANG_BAI.md`), không phải thiếu kênh |
| **Bán sỉ cho quán chè/trà sữa/tiệm bánh** _(kênh mới, chưa khai thác)_ | **B2B trong nước** | Hợp pháp ở quy mô nhỏ lẻ chỉ cần **bản cam kết ATVSTP** với xã, KHÔNG bắt buộc giấy ATTP đầy đủ. Lưu ý định vị: thị trường sỉ chủ yếu bán "bột sắn" (bột năng, ~12-18k/kg) rẻ hơn nhiều "bột sắn dây" nhà mình — phải chào đúng phân khúc cao cấp/thủ công, không cạnh tranh giá với bột năng. Cách tiếp cận: tham gia nhóm Facebook "CHUYÊN SỈ NGUYÊN LIỆU NẤU CHÈ - TRÀ SỮA - PHA CHẾ" / "CHỢ SỈ NGUYÊN LIỆU NẤU CHÈ TRÀ SỮA VÀ ĐỒ ĂN VẶT" chào hàng trực tiếp, giá sỉ đề xuất ~90-110k/kg tuỳ số lượng (ước tính, chưa xác thực) |
| Yellow Pages Vietnam | B2B nước ngoài | Miễn phí, nhanh — nội dung đã soạn sẵn trong `DANG_KY_THU_MUC_XUAT_KHAU.md`, bạn tự đăng ký |
| Gọi VIETRADE hỏi điều kiện | B2B nước ngoài | Số đã có: (04) 39 347 628 |
| Gọi Sở Y tế Lạng Sơn hỏi ATTP có được miễn không | Điều kiện nền cho B2B chính ngạch | Số đã có: (0205) 3.812.258 — xem `GHI_CHU_ATTP.md` |

### Nhóm B — Cần 1 cuộc gọi xác nhận trước khi bắt tay làm

| Kênh | Loại | Việc cần xác nhận |
|---|---|---|
| **Buudien.vn** (Postmart cũ, đổi tên 31/3/2024, Vietnam Post vẫn vận hành) | B2B/B2C trong nước | **Voso đã ngừng hoạt động từ 2023** — bỏ hẳn khỏi kế hoạch. Buudien.vn còn sống, hotline **1900 565 657**, nongsan.buudien.vn cho hàng cao cấp — gọi hỏi rõ: (1) Tinh Bột Sắn Dây chưa ATTP có đăng ký được không, (2) phí/hoa hồng hiện tại, (3) có hỗ trợ logistics lạnh cho Cam Đường Canh không |
| **OCOP tỉnh Lạng Sơn** cho Cam Đường Canh | B2B trong nước (mở cửa vào siêu thị/đặc sản) | Nộp online qua `ocop.langson.gov.vn`. Đợt xét toàn quốc: hồ sơ trước 30/4 hoặc 30/10 hàng năm — đợt 2 năm nay còn kịp nếu chuẩn bị sớm. Gọi **Sở Nông nghiệp và Môi trường Lạng Sơn (0205) 3870327 / 3870353** hỏi: đầu mối cấp xã sau khi bỏ cấp huyện (xã Vũ Lăng giờ báo cáo thẳng lên tỉnh), và VietGAP đã có đủ làm minh chứng chưa |

### Nhóm C — Thử nghiệm nhỏ trước khi mở rộng (rủi ro thật, không phải chỉ thủ tục)

- **Gửi lẻ cho người Việt ở nước ngoài qua VNPost EMS** (B2C xuất khẩu, kênh "nhẹ" không cần ATTP
  vì không phải xuất khẩu chính ngạch) — **có rủi ro hải quan thật, không phải cứ gửi là được**:
  - Đức: được phép, miễn giấy tờ nếu ≤2kg/kiện.
  - Nhật: **(đính chính 2026-08-13)** không có "ngưỡng miễn kiểm 100kg/năm" như ghi trước đây — tra
    trực tiếp customs.go.jp không thấy căn cứ, con số 100kg chỉ áp dụng riêng cho gạo mang theo hành
    lý cá nhân. Quy tắc thật dựa trên **mục đích sử dụng** (cá nhân/không kinh doanh mới được miễn
    khai báo thương mại), không phải theo cân nặng — kiện gửi để bán vẫn phải khai báo và có thể bị
    kiểm tra dù nhỏ. Vẫn qua kiểm dịch thực vật tại bưu điện.
  - Hàn Quốc: hàng có thể bị giữ kiểm tra bởi MFDS.
  - **Úc: rủi ro cao nhất** — quét máy + chó nghiệp vụ, hàng dễ bị giữ/tiêu huỷ nếu không tra trước
    điều kiện trên BICON (bicon.agriculture.gov.au).
  - Mỹ: chưa xác nhận được — cần gọi APHIS (301-851-3300) trước khi gửi lô đầu.
  - **Cách làm an toàn**: gửi thử 1 kiện <2kg cho người quen ở Đức hoặc Nhật trước (rủi ro thấp
    nhất), dán đúng tờ khai hải quan CN22/23 ghi rõ "cassava starch / tinh bột sắn dây, thực phẩm",
    xem có bị giữ không rồi mới tính mở rộng sang Hàn/Úc/Mỹ.
- **Vựa sỉ/chợ đầu mối** tại Hà Nội cho Cam Đường Canh cuối mùa (B2B trong nước, xem Giai đoạn 3
  mục 4) — vẫn đúng như kế hoạch cũ.

### Nhóm D — Vẫn bị chặn thật, không thể làm "đồng thời" cùng nhóm A/B/C

- **B2B chính ngạch xuất khẩu (Alibaba, sàn giao dịch nông sản)** — luật yêu cầu ATTP trước, không
  có cách hợp pháp nào bỏ qua bước này. Chờ kết quả cuộc gọi Sở Y tế (Nhóm A).
  chi tiết hồ sơ nếu vẫn cần xin giấy: `GHI_CHU_ATTP.md`.
- **Shopee/TikTok Shop** — không bị luật chặn, chỉ chặn vì cần bạn tự đăng ký tài khoản (đã quyết
  định mở từ 2026-07-05, vẫn chưa đăng ký).
- **Cam Đường Canh xuất khẩu trái tươi** — cần giấy kiểm dịch thực vật, không tương xứng quy mô hộ
  gia đình hiện tại. Hướng khả thi hơn về sau là chế biến (mứt cam, nước cam cô đặc) — chưa tính vội.

## Thứ tự triển khai tối ưu (chốt 2026-08-12)

_Xếp theo đòn bẩy/công sức — không phải làm hết cùng lúc theo nghĩa đen, mà làm việc rẻ+lời nhất
trước. Việc #1 (gọi hỏi ATTP) người dùng tự nhận lo, không cần Claude nhắc lại._

| # | Việc | Trạng thái |
|---|---|---|
| 1 | Gọi Sở Y tế Lạng Sơn hỏi ATTP có được miễn không | 🔵 User tự lo, chủ động hoãn lại (không phải bị kẹt) |
| 2 | Đăng bài Zalo/Facebook theo `LICH_DANG_BAI.md` (Tuần 3-5 đã soạn xong) | Chờ đăng |
| 3 | Chào hàng sỉ quán chè/trà sữa + đặc sản OCOP Lạng Sơn — 4 tin nhắn điền sẵn tên/SĐT + 1 kịch bản đến tận nơi ở `content/templates/chao_hang_san_sang_gui.md` (soạn 08-17) | Sẵn sàng gửi/đi ngay |
| 4 | Gọi Buudien.vn hỏi điều kiện — 1900 565 657 | Chưa gọi |
| 5 | Đăng ký Yellow Pages Vietnam | Chưa đăng ký |
| 6 | Gọi VIETRADE — (04) 39 347 628 | Chưa gọi |
| 7 | Gọi Sở NN&MT hỏi đầu mối OCOP — (0205) 3870327 | Chưa gọi, chưa gấp |
| song song | Ghi đơn hàng/mẻ sản xuất thật ngay khi có | Vẫn trống |
| để sau | Đăng ký Shopee/TikTok Shop, thử gửi kiện hàng đi Đức/Nhật | Chưa bắt đầu |

## Giới hạn cần nhớ khi thực hiện

- Không tự động đăng bài (rủi ro khoá tài khoản) — mọi nội dung Claude soạn, bạn tự đăng tay.
- Không xuất khẩu Cam Đường Canh (trái tươi, chưa có giấy kiểm dịch thực vật) — chỉ Tinh Bột Sắn
  Dây mới nhận trao đổi xuất khẩu.
- Không tự thêm chứng nhận cho Tinh Bột Sắn Dây — định vị trung thực "gia đình sản xuất nhỏ, thủ công".
- Không đăng file PDF gốc chứng nhận VietGAP công khai (có thông tin thành viên khác trong HTX).

## Việc cần bạn chủ động làm (Claude không tự làm được)

1. ~~Chụp/quay ảnh video thật (sắn dây + vườn cam)~~ — ✅ đã có (2026-07-25), đã lên web (2026-07-26).
2. Cung cấp Facebook link, email, WhatsApp để điền vào website và `products.json`.
3. Tự đăng ký gian hàng Shopee/TikTok Shop cho Tinh Bột Sắn Dây (đã quyết định mở — xem Giai đoạn 1,
   mục 5).
4. Bắt đầu ghi đơn hàng thật ngay khi có, để các báo cáo/cảnh báo tồn kho có ý nghĩa.
5. Nếu muốn theo đuổi B2B/xuất khẩu sau này: gọi hỏi Sở Y tế tỉnh Lạng Sơn (0205) 3.812.258 xem hộ
   nhà mình có thuộc diện miễn giấy ATTP không (xem `GHI_CHU_ATTP.md` để biết cần hỏi gì/chuẩn bị gì).
6. **Mới (2026-08-12)**: gọi hotline Buudien.vn **1900 565 657** hỏi có nhận Tinh Bột Sắn Dây chưa
   ATTP không + phí; gọi Sở Nông nghiệp và Môi trường Lạng Sơn **(0205) 3870327** hỏi đầu mối OCOP
   cấp xã sau sáp nhập; thử chào hàng sỉ trong 1-2 nhóm Facebook nguyên liệu pha chế cho quán chè.
