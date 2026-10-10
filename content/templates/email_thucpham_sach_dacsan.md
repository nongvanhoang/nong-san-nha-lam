# Email chào hàng — Nhóm J (cửa hàng thực phẩm sạch/hữu cơ) và Nhóm K (đặc sản quà biếu)

_Thêm 2026-09-08. Giai đoạn 2 trong `KE_HOACH_KHAI_THAC_B2B.md` — 38 lead đã có email xác minh
(20 Nhóm J, 18 Nhóm K), lấy đầy đủ trong `DANH_SACH_KHACH_HANG_B2B.csv` hoặc tab "Bán hàng hôm nay"
trong app local. Khác Nhóm N (chỉ 4 công ty, viết riêng từng thư), nhóm này đông hơn nên dùng
**1 mẫu chung**, tự điền tên cửa hàng, gửi lần lượt — không cần viết riêng 38 bức._

## Mẫu 1 — Nhóm J (cửa hàng thực phẩm sạch/hữu cơ)

**Chủ đề:** Tinh bột sắn dây thủ công Lạng Sơn — nguyên liệu sạch cho [Tên cửa hàng]

> Kính gửi anh/chị phụ trách nhập hàng — [Tên cửa hàng],
>
> Em là đại diện Nông Sản Nhà Làm, cơ sở nhỏ tại Lạng Sơn chuyên làm tinh bột sắn dây thủ công — tự lọc tay, sấy bằng lò sấy chuyên dụng riêng, không hoá chất, không tẩy trắng, không phải bột sắn (bột năng) giá rẻ thường thấy.
>
> Em thấy [Tên cửa hàng] đang tập trung vào thực phẩm sạch/hữu cơ nên muốn hỏi thử: bên mình có đang tìm thêm nguồn nguyên liệu nấu chè/pha nước có nguồn gốc rõ ràng, làm thủ công tại nhà không ạ? Em có thể gửi mẫu dùng thử trước, không mất phí.
>
> Rất mong nhận được phản hồi ạ.
>
> Trân trọng,
> Nông Sản Nhà Làm — Lạng Sơn
> Zalo/Hotline: 0979 502 000
> Email: hello@nongsannhalam.com

## Mẫu 2 — Nhóm K (cửa hàng đặc sản/quà biếu)

**Chủ đề:** Đặc sản Lạng Sơn — Tinh bột sắn dây thủ công cho [Tên cửa hàng]

> Kính gửi anh/chị phụ trách sản phẩm — [Tên cửa hàng],
>
> Em là đại diện Nông Sản Nhà Làm, cơ sở nhỏ tại Lạng Sơn chuyên làm tinh bột sắn dây thủ công — tự lọc tay, sấy bằng lò sấy chuyên dụng riêng, không hoá chất, không tẩy trắng.
>
> Em thấy [Tên cửa hàng] đang kinh doanh đặc sản vùng miền làm quà biếu, nên muốn hỏi thử: bên mình có đang tìm thêm đặc sản mới cho gian hàng không ạ? Sắn dây Lạng Sơn có câu chuyện "đặc sản gia đình làm thủ công" thật, đóng gói đẹp, hợp làm quà.
>
> Em có thể gửi mẫu dùng thử và báo giá sỉ nếu anh/chị quan tâm. Rất mong nhận được phản hồi ạ.
>
> Trân trọng,
> Nông Sản Nhà Làm — Lạng Sơn
> Zalo/Hotline: 0979 502 000
> Email: hello@nongsannhalam.com

## Danh sách gửi (lấy tên đúng cột "Ten" trong CSV để điền vào [Tên cửa hàng])

Nhóm J (dùng Mẫu 1): Nong San Ngon, CleverFood, Soi Bien, Nam An Market, Organicfood.vn, Vườn Xanh
Organic, Go Green, Organica (TP.HCM), Vietnam VEG, Co.op Food (Cần Thơ), SATRAFOODS (Cần Thơ), Thiên
An Mart, F5 Fruit Shop, Family Fruits, Tứ Phương, Luxuryfoods, Thực Phẩm Sạch Tâm Food, 3F Food Mart,
Thực Phẩm Sạch Nha Trang, Mailan Food.

Nhóm K (dùng Mẫu 2): DOGIFOOD, Khonia, Huong Viet, Ut Ha Dac San, Dac San Chinh Goc, Vigift, Siêu
thị Đặc sản Đại Lộc Phát, Quà Miền Trung, Hương Đà, Đặc Sản Mộc Truly Huế's, Huế Gourmet, Quà Huế
Online, Tinh Hoa Huế, SEAVY, Dalavi, Berryland, Trạm Quà Vàng Danh, Đặc sản Tây Nguyên Bập Bùng.

Email đầy đủ từng lead xem trong `DANH_SACH_KHACH_HANG_B2B.csv` (lọc cột Nhom = "J - ..." hoặc
"K - ...") hoặc mở app local, tab "Bán hàng hôm nay" — bấm thẳng vào email là mở soạn thư luôn.

## Gửi nhanh bằng mail-merge (thêm 2026-09-09)

Đã xuất sẵn 2 file cho mail-merge (Gmail + Google Sheets) — **KHÔNG dùng công cụ campaign kiểu
Brevo/Mailchimp** (dễ bị khoá tài khoản vì danh sách này chưa opt-in, và có thể ảnh hưởng luôn email
đơn hàng thật). Mail-merge vẫn gửi TỪNG email riêng biệt qua Gmail thật của bạn, chỉ nhanh hơn gửi
tay, an toàn hơn campaign:

- `content/templates/mail_merge_nhom_J.csv` (20 dòng, cột `Email Address` + `Ten_cua_hang`)
- `content/templates/mail_merge_nhom_K.csv` (18 dòng, cùng cấu trúc)

**Cách dùng (1 lần cài, dùng lại được mãi)**:
1. Cài tiện ích miễn phí **Yet Another Mail Merge (YAMM)** từ Google Workspace Marketplace (tìm
   "YAMM" trong Google Sheets → Tiện ích bổ sung → Lấy tiện ích bổ sung). Miễn phí 50 email/ngày với
   Gmail thường — đủ dùng cho cả 2 nhóm này trong 1 ngày.
2. Tạo 1 Google Sheet mới, import file `mail_merge_nhom_J.csv` vào (File → Nhập).
3. Trong Gmail, soạn 1 bản nháp (draft) dùng đúng nội dung **Mẫu 1** ở trên — chỗ nào có
   `[Tên cửa hàng]` thì thay bằng `{{Ten_cua_hang}}` (đúng tên cột trong sheet).
4. Mở Sheet → menu YAMM → Start Mail Merge → chọn đúng bản nháp vừa soạn → gửi.
5. Lặp lại bước 2-4 với `mail_merge_nhom_K.csv` và nội dung **Mẫu 2**.

**Nhóm N (4 email) vẫn nên gửi tay từng cái như hướng dẫn ở trên** — mỗi thư viết riêng cho từng công
ty, không hợp mail-merge (vốn dùng 1 mẫu chung).

## Sau khi gửi

Báo lại kết quả qua chat hoặc cập nhật trực tiếp trong app local (tab "Bán hàng hôm nay" → nút "Cập
nhật" ở đúng dòng khách đó) — không cần nhớ số dòng trong CSV.
