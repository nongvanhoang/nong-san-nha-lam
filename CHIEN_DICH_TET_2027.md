# Chiến Dịch Mùa Cam & Tết 2027

_Soạn 2026-09-30. Là bản cụ thể hoá Giai đoạn 2–3 trong `KE_HOACH_BAN_HANG.md` thành lịch có ngày. Tết Đinh
Mùi: **thứ Bảy 6/2/2027**. Cam Đường Canh vào mùa khoảng tháng 11 âm lịch (≈ giữa tháng 12/2026) — ngày chính
xác do vườn quyết định, các mốc dưới đây xê dịch theo._

## 0. Nút thắt thật: có bài nhưng chưa đăng

Kho `content/posts_ready.md` có sẵn ~59 bài, `LICH_DANG_BAI.md` đã xếp lịch đến tháng 10 — nhưng bảng checklist
mới có **1 ô ✅**, mọi bài từ 08/09 đều chưa đăng. Viết thêm bài lúc này không tăng doanh thu; **đăng đều mới tăng**.

**Quy tắc đến hết Tết (thay cho việc đăng 5 kênh):**
- **Chỉ bắt buộc 2 kênh: Facebook + Zalo** (nơi khách mua cam/quà Tết thật sự nhắn đặt hàng). Instagram, LinkedIn,
  YouTube: đăng khi rảnh, không tính là "trễ lịch".
- **15 phút mỗi sáng**: mở app quản lý → tab "Bán hàng hôm nay" → copy → đăng FB + Zalo → bấm "Đã đăng".
- Bỏ lỡ ngày nào thì **đăng bài của ngày đó luôn hôm sau**, không cố đuổi bù cả tuần.

## 1. Lịch chiến dịch

| Giai đoạn | Thời gian | Mục tiêu | Việc chính |
|---|---|---|---|
| **1. Hâm nóng + gom danh sách chờ** | 01/10 – 15/11 | Có người đăng ký chờ cam trước khi có hàng | Đăng bài "hẹn báo hàng mùa cam" (có sẵn, dòng ~810 `posts_ready.md`) **ngay tuần này**, đăng lại mỗi 2 tuần · Bài VietGAP · Ai nhắn/bình luận → ghi vào `data/danh_sach_cho.csv` · Theo dõi email quà Tết doanh nghiệp (Nhóm N) — DN chốt nhà cung cấp tháng 10–11 |
| **2. Mở đặt trước hộp quà Tết** | 15/11 – vào mùa | Chốt đơn trước, biết cần thu hoạch/đóng gói bao nhiêu | Bài A + B bên dưới · Chào B2B quà Tết (Bài B bản Zalo) · Đặt in hộp/tem (đi cùng việc tìm xưởng in đang treo) |
| **3. Vào mùa** | ≈ giữa 12/2026 – 20/01/2027 | Bán hết đợt đầu | **Nhắn riêng danh sách chờ TRƯỚC khi đăng công khai** (Tin nhắn C) · Đăng các bài "chỉ đăng khi vào mùa" có sẵn · Đổi schema website `PreOrder` → `InStock` (2 file, xem `KE_HOACH_BAN_HANG.md`) · Mỗi đơn ghi ngay bằng `add_order.py` |
| **4. Nước rút Tết** | 20/01 – hạn giao | Chốt đơn cuối, không nhận quá sức | Bài D (đếm ngược hạn giao) · Hạn chót nhận đơn giao trước Tết: `[CẦN CHỐT — hỏi đơn vị vận chuyển ngày nghỉ Tết 2027]` |
| **5. Sau Tết** | 10/02 – hết mùa | Giữ khách cho năm sau + bán nốt | Xin khách ảnh/nhận xét (lưu `data/testimonials.json`) · Cuối mùa ưu tiên khách quen |

## 2. Hộp quà Tết — cần chốt trước 15/11

Ý tưởng: ghép 2 sản phẩm thành quà biếu — cam là quà "tươi, mùa vụ, có VietGAP", sắn dây là quà "để được lâu,
thủ công". **Giá chưa chốt** — tính từ giá gốc + chi phí hộp + in + phí gửi, rồi báo lại để Claude điền vào bài.

| Gói | Gồm | Giá gốc cộng lại (theo `products.json`) | Giá hộp quà |
|---|---|---|---|
| Gói nhỏ | Cam 5kg + Sắn dây 0,5kg | 275.000 + 80.000 = 355.000đ | `[CẦN CHỐT]` |
| Gói lớn | Cam 10kg + Sắn dây 1kg | 500.000 + 155.000 = 655.000đ | `[CẦN CHỐT]` |
| Gói doanh nghiệp | Theo số lượng, có thể in lời chúc/logo công ty | — | báo giá riêng |

Cần quyết: chi phí hộp/túi quà mỗi gói · có tặng thiệp viết tay không · gửi xa (ngoài miền Bắc) cam có giữ được
không — nếu không chắc, hộp quà chỉ nhận **giao miền Bắc**, tỉnh xa chỉ gửi sắn dây.

**Đề xuất giá của Claude (2026-10-10) — CHƯA CHỐT, bạn sửa/duyệt rồi Claude mới đưa lên web và bài đăng:**

| Gói | Hàng (giá lẻ) | + hộp, thẻ treo, thiệp | Giá đề xuất | Ghi chú |
|---|---|---|---|---|
| Gói nhỏ | 355.000đ | ~30.000đ **(giả định — thay bằng giá hộp thật)** | **399.000đ** | Dưới mốc 400k, khách dễ quyết |
| Gói lớn | 655.000đ | ~40.000đ **(giả định)** | **749.000đ** | Dưới mốc 750k |

Cơ sở: hộp quà trái cây Tết trên thị trường phổ biến 350.000–850.000đ ([Tuổi Trẻ](https://tuoitre.vn/nld-phu-nu/cho-nghia-tan.html)) —
2 mức trên nằm giữa khoảng đó. Giá lẻ của nhà mình (cam ~50-55k/kg) đã thấp hơn mặt bằng (`VIEC_CAN_LAM.md` Nhóm 2),
nên hộp quà KHÔNG giảm giá thêm — phần chênh chỉ bù hộp/thẻ/thiệp. Chưa gồm phí ship. Nếu 1 hộp trơn đắt hơn
giả định, cộng phần chênh vào giá. Doanh nghiệp đặt ≥10 hộp: báo giá riêng.

**Hạn chốt đơn giao trước Tết (đề xuất, Tết Đinh Mùi = 06/02/2027):** Tết 2026, GHTK chỉ nhận lấy hàng **liên miền
trước 22 tháng Chạp**, **nội miền trước 24 tháng Chạp** ([thông báo GHTK](https://ghtk.vn/tin-cho-nha-ban/thong-bao-chi-tiet-lich-nghi-tet-am-lich-2026-cua-ghtk/)).
Áp cùng khoảng cách cho 2027 và chừa 2 ngày đóng gói → **nhận đơn cuối 26/01/2027 (khoảng 19 tháng Chạp)** cho
toàn quốc; miền Bắc có thể nhận đến **28/01/2027**. Bài D đăng **21/01/2027**. Kiểm tra lại khi các hãng ra lịch
Tết 2027 (thường đầu tháng 1) — nếu khác thì dời theo hãng.

**Mẫu mã đã phác sẵn (2026-10-03)**: thẻ treo `content/nhan_bao_bi/the-qua-tet.svg` — đúng phong
cách "Mộc & Thật", dùng chung cho cả 2 gói (có dòng trống viết tay "Gói:"/"Giá:" nên không phải in
lại khi chốt giá). Chỉ cần mua hộp/túi quà trơn (kraft hoặc trong suốt) + buộc thẻ này vào, không cần
đặt in hộp riêng — rẻ và nhanh hơn, đúng tinh thần "gia đình sản xuất nhỏ" đã chọn cho Shopee. Khi có
giá, gửi thẻ này kèm file nhãn sắn dây cho xưởng in quen (cùng 1 lần đặt).

## 3. Bài mới soạn sẵn (chỉ những bài còn thiếu — phần còn lại dùng kho có sẵn)

### Bài A — Facebook/Zalo: Mở đặt trước hộp quà Tết (đăng từ 15/11)

> Tết năm nay biếu gì cho bố mẹ, ông bà mà vừa ngon vừa biết rõ nguồn gốc?
>
> Nhà mình ghép 2 thứ tự tay làm ra thành hộp quà Tết:
> 🍊 **Cam Đường Canh** vườn nhà — thành viên HTX Nhung Giang, có chứng nhận VietGAP, chín tự nhiên trên cây
> 🌾 **Tinh bột sắn dây** lọc tay, sấy lò sấy riêng, không hoá chất, không tẩy trắng
>
> Gói nhỏ: cam 5kg + sắn dây 0,5kg — `[GIÁ]`
> Gói lớn: cam 10kg + sắn dây 1kg — `[GIÁ]`
>
> Cam chỉ có khoảng 3 tháng mỗi năm nên nhà mình nhận **đặt trước**, vào mùa là hái và gửi theo thứ tự đặt.
> 👉 Đặt trước trong 1 phút: nongsannhalam.com/dat-truoc.html?chon=qua-nho
> Hoặc nhắn Zalo 0979 502 000 để giữ suất nhé!

### Bài B — Quà Tết doanh nghiệp (Facebook + tin nhắn Zalo cho khách B2B; LinkedIn nếu có trang)

> Công ty mình đang chọn quà Tết cho nhân viên, đối tác?
>
> Thế Hưng Organic nhận đặt **hộp quà Tết số lượng lớn**: Cam Đường Canh Lạng Sơn (VietGAP số
> 112/CN-TĐC-TT-20-0012) kết hợp tinh bột sắn dây thủ công — quà đặc sản, có nguồn gốc rõ ràng, kiểm chứng được.
>
> Nhận in lời chúc theo yêu cầu. Báo giá theo số lượng — gửi phiếu nhanh tại nongsannhalam.com/dat-truoc.html?chon=qua-lon (ghi số lượng vào ô Ghi chú), hoặc nhắn Zalo 0979 502 000 / email hello@nongsannhalam.com.
> Doanh nghiệp thường chốt quà từ tháng 11, nên nhắn sớm để nhà mình giữ đủ hàng ạ.

### Tin nhắn C — Nhắn riêng từng người trong danh sách chờ (ngày cam vào mùa)

> Chào [tên] ạ, bên mình là Thế Hưng Organic đây. Hôm trước anh/chị có hẹn báo khi có Cam Đường Canh — **cam nhà
> mình vào mùa rồi**, đợt đầu hái hôm `[ngày]`. Vì anh/chị đăng ký trước nên mình nhắn trước khi đăng công khai
> ạ. Anh/chị lấy thùng 5kg (275.000đ) hay 10kg (500.000đ), hay hộp quà Tết ạ?

_(Nhắn từng người, không gửi hàng loạt kiểu spam — sau khi nhắn, đổi cột `da_bao` trong `data/danh_sach_cho.csv` thành ngày nhắn.)_

### Bài D — Đếm ngược hạn giao trước Tết (đăng ≈ 5 ngày trước hạn chót)

> Còn **5 ngày** là nhà mình chốt đơn giao trước Tết rồi ạ (hạn cuối `[ngày]`).
>
> Sau ngày đó bên vận chuyển nghỉ Tết, đơn đặt muộn sẽ giao sau Tết. Ai còn định biếu cam, biếu sắn dây thì nhắn
> sớm để kịp nhé — Zalo 0979 502 000 🍊

## 4. Đo kết quả (để biết chiến dịch có hiệu quả thật không)

- **Danh sách chờ**: số dòng trong `data/danh_sach_cho.csv` (mục tiêu do bạn đặt: `[ ]` người trước 15/11).
- **Đơn hàng**: mọi đơn ghi bằng `add_order.py` với `--channel` đúng nguồn (`zalo`, `facebook`, `b2b-qua-tet`,
  `danh-sach-cho`...) — cuối mùa `weekly_report.py` sẽ cho biết kênh nào ra đơn thật, năm sau dồn sức vào đó.
- **Không ghi đơn = không biết chiến dịch có hiệu quả không.** Đây là việc quan trọng ngang với việc đăng bài.

## 5. Tuần này (30/09 – 06/10)

- [ ] Đăng bài "hẹn báo hàng mùa cam" lên FB + Zalo (đã có sẵn, không cần viết)
- [ ] Đăng bài lịch 02/10 "Cam Đường Canh: hoa đến quả non" (video đã dựng sẵn)
- [ ] Chốt: hộp quà Tết có làm không, chi phí hộp bao nhiêu → báo lại để điền giá vào Bài A/B
- [ ] Xem hộp thư: công ty quà Tết Nhóm N đã trả lời chưa (`content/templates/email_qua_tet_doanh_nghiep.md`)
