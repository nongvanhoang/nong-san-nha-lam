# SOP — Quy Trình Chuẩn Cho Từng Việc Lặp Lại (2026-10-01)

_Mục đích: mỗi việc lặp đi lặp lại có 1 cách làm cố định, viết ra giấy thay vì chỉ nhớ trong đầu —
để (a) không quên bước nào khi làm vội, và (b) sau này nếu thuê người phụ (đóng gói, trả lời tin
nhắn...) có thể đưa đúng SOP mà giao việc được ngay, không phải giải thích lại từ đầu mỗi lần. Đây
là quy trình, không phải nơi quyết định — khi 1 bước cần quyết định (giá, chính sách), SOP trỏ sang
đúng file có quyết định đó, không tự đặt thêm quy tắc mới ở đây._

## 1. Có đơn hàng mới (khách nhắn Zalo/Facebook/gọi điện)

1. Xác nhận với khách: sản phẩm, quy cách (0.5kg/1kg sắn dây hoặc 5kg/10kg cam), số lượng, địa chỉ
   giao, cách thanh toán (chuyển khoản/COD). **Khách quen**: app tự tra sổ địa chỉ khi gõ đúng tên
   (ô "SĐT khách"/"Địa chỉ giao" tự điền) — chỉ cần xác nhận lại địa chỉ cũ còn đúng không, không cần
   hỏi lại từ đầu.
2. Báo giá đúng theo `data/products.json` (không tự giảm giá tuỳ hứng — nếu muốn giảm, đó là quyết
   định, ghi vào `note` khi ghi đơn để nhớ lý do).
3. Ghi đơn ngay (trong vòng vài phút, đừng để dồn cuối ngày — dễ quên/nhớ sai số):
   - Mở `MO_APP_QUAN_LY.bat` → "Ghi đơn hàng", điền thêm SĐT/địa chỉ nếu khách mới (tự lưu vào
     `data/customers.csv` cho lần sau), hoặc
   - Nhắn Claude: "ghi đơn khách [tên] mua [số lượng] [quy cách] [sản phẩm] qua [kênh] giá [giá],
     SĐT [số], địa chỉ [địa chỉ]"
   - **Luôn quy số lượng ra kg** (vd "2 thùng cam 10kg" → qty=20, unit=kg).
4. Đóng gói + giao hàng theo mục 2 bên dưới.
5. Khi khách đã nhận và trả tiền xong, cập nhật trạng thái đơn thành "đã giao" (nói với Claude hoặc
   sửa trong app).

## 2. Đóng gói & giao hàng

1. Cân đúng khối lượng theo quy cách đã bán (0.5kg/1kg sắn dây, 5kg/10kg cam).
2. Dán nhãn đúng sản phẩm (xem `content/nhan_bao_bi/` khi có nhãn in thật — trước đó dùng bao bì tạm
   + ghi tay thông tin cơ bản: tên sản phẩm, khối lượng, SĐT liên hệ).
3. Đóng gói chống va đập/ẩm khi gửi xa (sắn dây: túi kín tránh ẩm; cam: thùng carton có lót).
4. Giao trực tiếp (nội thành/gần) hoặc gửi qua đơn vị vận chuyển — ghi mã vận đơn vào `note` của đơn
   hàng nếu gửi xa, để tra cứu khi khách hỏi.
5. Báo khách khi đã gửi/giao xong, kèm lời cảm ơn — đây cũng là lúc tự nhiên xin đánh giá nếu khách
   vui vẻ (xem mục 4).

## 3. Trả lời khách hỏi mua (chưa chốt đơn)

1. Trả lời trong ngày, càng nhanh càng tốt — khách hỏi nhiều nơi cùng lúc, chậm là mất đơn.
2. Dùng đúng giọng điệu đã thống nhất trong `CLAUDE.md` (gần gũi, xưng "nhà mình", không phóng đại
   công dụng y tế).
3. Nếu khách chưa chốt ngay, đừng để im — dùng mẫu nhắn lại sau vài ngày ở
   `content/templates/nhan_tin_truc_tiep.md` (Mẫu 2: "khách cũ/từng hỏi nhưng chưa chốt").
4. Câu hỏi thường gặp đã có câu trả lời soạn sẵn ở `HO_SO_MANG_XA_HOI.md` mục 3 (hạn dùng, COD, hàng
   thật không, đổi trả) — dùng được cho cả khách nhắn trực tiếp, không chỉ riêng Shopee.

## 4. Khiếu nại / đổi trả

**Chính sách đã công bố trên website (2026-10-19)**: không nhận đổi trả hàng đã mở/đã dùng; **đổi mới hoặc
hoàn tiền** nếu hàng hư hỏng do vận chuyển, giao sai loại/số lượng, hoặc lỗi sản xuất — khách quay video lúc mở
hàng, báo Zalo trong 24 giờ. Website đã HỨA điều này → phải làm đúng, xử lý trong ngày, không tranh cãi (mùa cam
trước trên Shopee có khách chấm 1 sao vì "báo shop mà không được đền" — đừng lặp lại). Ghi lại khiếu nại (dù xử lý
xong) vào `note` của đơn hàng đó, để biết nếu 1 mẻ sản xuất nào đó có vấn đề lặp lại.

## 5. Xin đánh giá khách hàng

Theo đúng quy trình đã có ở `CLAUDE.md` mục "Xin & lưu đánh giá khách hàng": chỉ xin khách đã mua
≥2 lần hoặc đã phản hồi tích cực, dùng mẫu ở `content/templates/zalo.md` mục 5, lưu nguyên văn vào
`data/testimonials.json`, không sửa chữ/không bịa.

## 6. Sản xuất 1 mẻ Tinh Bột Sắn Dây

1. Đào củ sắn dây tươi trong ngày (không để qua đêm trước khi chế biến).
2. Nghiền, lọc tay nhiều lượt qua vải đến khi sạch cợn.
3. Sấy bằng lò sấy chuyên dụng (không còn phơi nắng từ 2026-08-11) đến khi khô hoàn toàn.
4. Đóng gói theo quy cách 0.5kg/1kg, dán nhãn.
5. Ghi mẻ sản xuất ngay: `MO_APP_QUAN_LY.bat` → "Ghi mẻ sản xuất", hoặc nhờ Claude chạy `add_batch.py`
   — luôn quy ra kg để `weekly_report.py` tính tồn kho đúng.

## 7. Thu hoạch Cam Đường Canh (theo mùa)

1. Thu hoạch đúng độ chín tự nhiên trên cây (không thúc chín bằng hoá chất — đúng tiêu chuẩn VietGAP
   đã chứng nhận).
2. Phân loại, đóng thùng 5kg/10kg (chỉ bán theo thùng, không bán lẻ theo kg).
3. Ghi mẻ thu hoạch bằng `add_batch.py` giống mục 6.
4. Ưu tiên nhắn trước cho danh sách chờ (`data/danh_sach_cho.csv`) trước khi đăng công khai — đúng
   Giai đoạn 3 trong `CHIEN_DICH_TET_2027.md`.

## 7b. Đóng thùng cam chống dập (thêm 2026-10-20)

Lý do: cả 3 đánh giá xấu (1–4 sao) mùa trước trên Shopee đều vì **cam dập/hư khi đi đường xa**; khách khen
nhiều nhất cũng nhắc "đóng thùng xốp chắc chắn". Làm đủ các bước dưới đây cho MỌI thùng gửi qua vận chuyển.

1. **Hái lúc quả ráo**: không hái khi còn mưa/sương đọng; hái xong để cam nơi thoáng mát vài giờ cho vỏ se rồi
   mới đóng — quả ướt đóng kín dễ úng, mốc.
2. **Loại kỹ trước khi xếp**: bỏ quả dập, nứt, mềm, có vết thâm; cắt cuống sát (cuống dài đâm thủng quả khác).
3. **Thùng xốp có lỗ thoáng**, đáy lót giấy/lá. Xếp từng lớp, quả to nằm dưới; giữa các lớp lót giấy chống sốc
   hoặc giấy báo; xếp **vừa khít, không để lắc**, nhưng không nén ép quả.
4. Dán băng dính chắc, ghi ngoài thùng: **"HÀNG DỄ DẬP — NHẸ TAY — KHÔNG XẾP NẶNG LÊN TRÊN"**.
5. **Chọn tuyến**: gửi gần (miền Bắc) bình thường; gửi xa (miền Trung/Nam) chọn dịch vụ nhanh nhất, **không gửi
   vào chiều thứ Sáu/trước ngày lễ** (hàng dễ nằm kho qua cuối tuần).
6. Nhắn khách khi gửi: mã vận đơn + "nhận hàng mở thùng ngay, để nơi thoáng; quay video lúc mở để nếu có quả
   hư nhà mình đổi/bù ngay".
7. Khách báo hư kèm video → **trong ngày** gửi bù hoặc hoàn tiền phần hư (theo mục 4), ghi vào `note` của đơn và
   ghi lại tuyến/hãng vận chuyển để biết tuyến nào hay hỏng.
8. (Tuỳ chọn, bạn quyết) thùng 10kg gửi xa cho thêm 2–3 quả bù hao — rẻ hơn nhiều so với 1 đánh giá 1 sao.

## 8. Đăng bài mạng xã hội theo lịch

1. Hệ thống tự nhắc mỗi 3 ngày (xem `HUONG_DAN_KHAI_THAC.md` mục 0) → đọc `BAI_DANG_HOM_NAY.txt`.
2. Copy nguyên văn, dán lên đúng kênh, đăng kèm ảnh/video (lấy nhanh qua tab "Thư viện Media").
3. Bấm "Đã đăng" trong app (tab "Bán hàng hôm nay") để tự nhớ trong ngày.
4. Hết hàng đợi (`data/social_queue.json`) → báo Claude để soạn thêm từ kho `posts_ready.md`.

## 9. Gọi/nhắn khách B2B

1. Mở tab **"Tổng quan"** → mục "Hôm nay nên gọi/nhắn B2B" — đã tự lọc 10 lead "Chưa liên hệ" ưu
   tiên cao nhất, không cần tự lọc/cuộn bảng B2B đầy đủ. Hoặc mở [Sổ Gọi Khách](https://claude.ai/artifact/N7ySVZpN3mXcgBJz7SvCcJ)
   khi ở ngoài/trên điện thoại.
2. Gọi theo kịch bản tương ứng nhóm (`content/templates/kich_ban_goi_dien_quan_che.md` cho Nhóm B).
3. **Luôn báo lại kết quả** (kể cả "không nghe máy") để cập nhật đúng trạng thái ở tab "Bán hàng hôm
   nay" — đây là bước hay bị bỏ qua nhất, làm mất giá trị của cả hệ thống theo dõi. Lead vừa cập nhật
   trạng thái sẽ tự rơi khỏi danh sách "Hôm nay nên gọi" lần sau, không cần làm gì thêm.

## 10. Ghi chi phí

Mỗi lần chi tiền cho việc kinh doanh (mua nguyên liệu, in nhãn, bao bì, vận chuyển, quảng cáo, dụng
cụ...), ghi ngay — đừng dồn cuối tháng vì sẽ quên khoản nhỏ:

1. Mở `MO_APP_QUAN_LY.bat` → tab "Chi phí", hoặc nhờ Claude chạy `add_expense.py`.
2. Chọn đúng hạng mục (nguyên liệu, bao bì/nhãn, vận chuyển, quảng cáo, in ấn, dụng cụ/máy móc, giấy
   tờ/pháp lý, khác).
3. `weekly_report.py` và tab "Báo cáo"/"Chi phí" sẽ tự tính lãi/lỗ dựa trên doanh thu đã ghi (mục 1)
   trừ chi phí đã ghi ở đây — không ghi chi phí thì số lãi hiện ra sẽ cao giả, không phản ánh đúng.

## 11. Kiểm tra sức khoẻ hệ thống (hàng tháng)

Chạy 1 lệnh duy nhất: `python scripts/kiem_tra_he_thong.py` — tự kiểm tra cả 7 việc dưới đây, in ra
✅/⚠️/❌ cho từng mục thay vì phải tự nhớ kiểm tra tay:

- Lịch tự động (`NongSanNhaLam_SocialReminder`, `NongSanNhaLam_WeeklyDigest`) còn chạy/có bị tắt không.
- Hàng đợi đăng bài còn đủ bao lâu (`data/social_queue.json`), cảnh báo khi còn ≤7 ngày.
- File dữ liệu (CSV/JSON) đọc được, không lỗi định dạng.
- **An toàn git** (thêm 2026-10-02): mọi file có thể chứa dữ liệu khách hàng/kinh doanh thật
  (`orders.csv`, `customers.csv`, `expenses.csv`, `production_log.csv`, `posted_log.csv`,
  `DANH_SACH_KHACH_HANG_B2B.csv`, `muc_tieu.json`) có thực sự nằm trong `.gitignore` không — phòng
  sự cố lặp lại kiểu lộ dữ liệu khách thật lên GitHub công khai.
- **Backup OneDrive** (thêm 2026-10-02): mọi file dữ liệu đang có đã có bản sao trong
  `OneDrive/NongSanNhaLam-Backup/latest` chưa.
- Mục tiêu tháng (`data/muc_tieu.json`) đã đặt số chưa.
- Hạn chót đang theo dõi (từ `VIEC_CAN_LAM.md`) còn bao nhiêu ngày, có cái nào đã trễ không.
