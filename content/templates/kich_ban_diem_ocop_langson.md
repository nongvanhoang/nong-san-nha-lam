# Kịch bản ghé trực tiếp — điểm bán OCOP tại Lạng Sơn (Nhóm I)

_Thêm 2026-09-01. Khác với các mẫu chào hàng qua Zalo/tin nhắn (`ban_si_quan_che.md`,
`ban_si_nha_phan_phoi.md`) — Nhóm I trong `DANH_SACH_KHACH_HANG_B2B.md` phần lớn chưa có SĐT công
khai, chỉ tiếp cận được bằng cách đến tận nơi. Đây là kịch bản nói trực tiếp + checklist mang theo,
dùng đúng giá thật từ `data/products.json` (không phải giá ước tính)._

## Ghé 211 & 115 Trần Đăng Ninh (cùng 1 trục đường, đi 1 buổi)

**Điểm 1 — 211 Trần Đăng Ninh (Minh Phát, trưng bày 200 sản phẩm OCOP, khách có cả người Đài
Loan/Quảng Tây).**
**Điểm 2 — 115 Trần Đăng Ninh (Cty An Gia, đang bán sẵn tinh bột nghệ)** — mở lời dễ nhất vì họ đã
quen bán "tinh bột đặc sản làm quà".

### Câu mở đầu (nói trực tiếp, không cần giấy)

> Chào anh/chị, em ở Nông Sản Nhà Làm, nhà em ở xã Vũ Lăng, làm tinh bột sắn dây thủ công — tự lọc
> tay, sấy bằng lò sấy riêng, không hoá chất, không tẩy trắng. Em thấy cửa hàng mình có bày sản phẩm
> OCOP/đặc sản làm quà [với điểm 115: "như tinh bột nghệ bên mình đang bán"], nên muốn hỏi thử: cửa
> hàng có nhận ký gửi thêm mặt hàng đặc sản địa phương không ạ? Em có mang theo mẫu để anh/chị dùng
> thử, không mất phí.

### Câu hỏi cần hỏi lại (đừng tự đoán/tự hứa)

- Hình thức hợp tác: ký gửi ăn phần trăm, hay mua đứt theo lô?
- Cửa hàng cần giấy tờ gì để nhận bán (giấy công bố chất lượng? hay chỉ cần tem nhãn đầy đủ thông
  tin là đủ)?
- Quy cách đóng gói nào bán chạy nhất ở đây — gói nhỏ 0,5kg làm quà, hay có khách mua số lượng lớn?
- Có cần sản phẩm đạt OCOP mới nhận bày không, hay chưa có cũng ký gửi được?

### Mang theo

- 2-3 gói mẫu nhỏ (đã có nhãn in sẵn từ `content/nhan_bao_bi/nhan-say-day-500g.svg`).
- Bảng giá thật: túi 0,5kg = 80.000đ · túi 1kg = 155.000đ (không đưa giá sỉ tại chỗ nếu chưa rõ hình
  thức hợp tác — hỏi trước, tính sau).
- Số Zalo/WhatsApp thật (+84 363 589 920) để họ liên hệ lại.

### Sau đó, ghé Sở NN&MT Lạng Sơn (118 Ba Sơn, ĐT 02053.870.353)

Hỏi thủ tục đăng ký OCOP — có OCOP sẽ mở khóa cả mạng lưới ~10 điểm bán OCOP toàn tỉnh cùng lúc,
không phải đi chào từng điểm.

## Backup, không cần đi cùng ngày

Cửa hàng OCOP Văn Lãng (chủ Chu Thị Hạnh, TT Na Sầm) — doanh thu công bố >400 triệu/nửa năm, nhưng
khác trục đường nên để chuyến sau.

## Sau khi đi

Báo lại kết quả (đồng ý/từ chối/hẹn sau) để cập nhật cột `Trang_thai` trong
`DANH_SACH_KHACH_HANG_B2B.csv` — không tự đánh dấu khi chưa xác nhận. Có đơn ký gửi thật, ghi vào
`data/orders.csv` với `channel` là `b2b-ocop-langson`.
