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
5. Nếu muốn theo đuổi B2B/xuất khẩu sau này: tìm hiểu thủ tục xin chứng nhận ATTP/HACCP cho cơ sở
   sản xuất Tinh Bột Sắn Dây trước.
