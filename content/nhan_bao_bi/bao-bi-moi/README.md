# Bao bì Tinh Bột Sắn Dây THOC — bản in sạch (2026-10-25)

Làm lại từ thiết kế gốc trong `../thiet-ke-2026-10-25/`. Phần hình (lá, củ, núi) được giữ lại, còn toàn bộ chữ được gõ lại vì bản gốc sai dấu: "TỊNH", "SĂN".

## File gửi xưởng in: thư mục `pdf/`

| File | Khổ (rộng × cao) | Dùng cho |
|---|---|---|
| tui-500g-mat-truoc.pdf + tui-500g-mat-sau.pdf | 160 × 240 mm | Túi đứng 500g |
| tui-1kg-mat-truoc.pdf + tui-1kg-mat-sau.pdf | 200 × 300 mm | Túi đứng 1kg |
| bao-5kg.pdf | 350 × 525 mm | Bao 5kg (in cả 2 mặt giống nhau) |
| bao-10kg.pdf | 400 × 600 mm | Bao 10kg (in cả 2 mặt giống nhau) |

Thư mục `png/` chỉ dùng để xem trước, không gửi in.

**Khổ trên là khổ tạm.** Hỏi xưởng in khổ túi/bao thật và phần chừa mép (miệng zip, đường hàn, nếp gấp đáy). Báo lại để chạy lại cho đúng khổ: sửa `DESIGNS` trong `scripts/tao_bao_bi.js` rồi chạy `node scripts/tao_bao_bi.js`.

## Phải điền trước khi in (đang để chữ ĐỎ)

- **Số tự công bố sản phẩm**: điền vào `SO_TCB` ở đầu `scripts/tao_bao_bi.js`.
- **Mã vạch GS1**: xin mã rồi đặt vào ô đỏ "MÃ VẠCH" ở mặt sau.
- **NSX / HSD / Số lô**: để trống có chủ đích, đóng dấu theo từng mẻ hoặc dán tem lô in từ `scripts/ma_lo.py tem <mã>`.
- **QR mặt sau** (từ 2026-10-27) dẫn tới thehungorganic.com/lo/ (tra cứu số lô). QR cũ trỏ tên miền cũ, đã thay — in bản PDF mới.

## Đã bỏ so với bản gốc, và lý do

- Con dấu "ORGANIC – Hàng sản sạch": chưa thấy giấy chứng nhận hữu cơ cho sắn dây. Khi có giấy sẽ thêm lại, kèm số giấy và đơn vị cấp.
- "Tốt cho sức khỏe", "An toàn cho sức khỏe", "giàu dưỡng chất": là câu nói về công dụng, dễ bị yêu cầu chứng minh. Đã thay bằng sự thật về cách làm: "Lọc tay · Sấy lò · Không tẩy trắng".
- Logo tròn kiểu cũ ("Hợp tác xã Thế Hưng" có hình núi và củ sắn): đã thống nhất dùng một logo **THOC**.

## Lưu ý cho xưởng in

- Hình lá, củ và núi là ảnh, không phải nét vẽ. Ở khổ bao 10kg, ảnh sẽ hơi mềm, in bao dệt thì vẫn chấp nhận được. Nếu xưởng cần nét hơn, họ có thể dùng lại file gốc của người thiết kế cho riêng phần hình.
- Font chữ đã nhúng sẵn trong PDF (Be Vietnam Pro và Dancing Script, có đủ dấu tiếng Việt).
- **Luôn xem bản in thử trước khi in cả lô.**
