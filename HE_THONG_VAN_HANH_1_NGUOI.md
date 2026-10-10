# Hệ Thống Vận Hành Doanh Nghiệp 1 Người (2026-10-01, thêm tab Tổng quan 2026-10-01)

**Cách nhanh nhất dùng file này**: mở `MO_APP_QUAN_LY.bat` → tab **"Tổng quan"** (mặc định hiện ra
đầu tiên) — gộp sẵn bài cần đăng hôm nay, hạn chót sắp tới (đọc từ `VIEC_CAN_LAM.md`), cảnh báo tồn
kho, tài chính tháng này, và khách quen lâu chưa quay lại mua — vào đúng 1 màn hình, không cần mở
từng tab/file riêng lẻ nữa.

_Đây là file ĐẦU TIÊN nên đọc khi không biết bắt đầu từ đâu — nó không thay thế các file khác, mà
gói gọn cách 4 mảng (nhịp vận hành, tài chính, quy trình, mục tiêu) khớp với nhau thành 1 hệ thống,
rồi trỏ đúng sang file chi tiết khi cần. Chỉ 1 người làm hết (sản xuất, bán hàng, giao hàng, sổ sách)
nên nguyên tắc số 1 là: **đơn giản hơn là đầy đủ** — thà bỏ sót 1 việc nhỏ còn hơn kiệt sức vì cố
làm hết mọi thứ mỗi ngày._

## 0. 4 mảng của hệ thống, mỗi mảng 1 câu trả lời

| Mảng | Câu hỏi nó trả lời | File chi tiết |
|---|---|---|
| **Nhịp vận hành** | Hôm nay/tuần này/tháng này làm gì, theo thứ tự nào? | Mục 1 bên dưới + `HUONG_DAN_KHAI_THAC.md` |
| **Quy trình (SOP)** | Việc lặp lại này làm đúng cách như thế nào? | `SOP.md` |
| **Tài chính** | Đang lãi hay lỗ thật? | Mục 2 bên dưới |
| **Mục tiêu** | Đi đúng hướng hay không, so với gì? | Mục 3 bên dưới |

## 1. Nhịp vận hành

### Hàng ngày (~20-30 phút, không tính thời gian đóng gói/giao hàng thật)
0. Mở tab "Tổng quan" 1 lần — nhìn nhanh có gì gấp (hạn chót, tồn kho, khách cần nhắn lại) trước khi
   làm các việc bên dưới.
1. Trả lời tin nhắn khách ngay khi có (SOP mục 3) — đây là việc duy nhất KHÔNG được để dồn, mất đơn
   nếu chậm.
2. Cuối ngày: ghi sổ mọi đơn hàng + chi phí phát sinh trong ngày (SOP mục 1, 10) — 30 giây/đơn.
3. Nếu hôm nay đến lịch nhắc đăng bài (mỗi 3 ngày, tự động) → đăng (SOP mục 8).
4. Nếu đang trong đợt gọi B2B → 8-10 cuộc (SOP mục 9), không hơn để tránh kiệt sức.

### Hàng tuần (1 buổi cố định, gợi ý sáng thứ Hai — trùng lúc bản tin tuần tự gửi)
1. Đọc `BAO_CAO_TUAN.txt` (tự động hiện ra).
2. Lướt `VIEC_CAN_LAM.md` — việc nào có hạn chót trong tuần này thì ưu tiên trước.
3. Nếu hết batch B2B đang gọi → xin Claude batch tiếp theo.

### Hàng tháng (đầu tháng, ~30-60 phút)
1. Chạy `python scripts/weekly_report.py --thang-nay` (hoặc tab "Chi phí" trong app) — xem lãi/lỗ
   tháng vừa qua, đối chiếu mục tiêu (mục 3 bên dưới).
2. Chạy `python scripts/kiem_tra_he_thong.py` (SOP mục 11) — 1 lệnh kiểm tra cả lịch tự động, hàng
   đợi đăng bài, file dữ liệu, mục tiêu, hạn chót — in ra đúng chỗ nào cần chú ý.
3. Đặt/xem lại mục tiêu tháng tới nếu cần.

### Theo mùa/chiến dịch (không cố định, đọc khi tới lúc)
- Hồ sơ OCOP (hạn 30/10/2026): `OCOP_2026.md`.
- Mùa Cam & Tết 2027: `CHIEN_DICH_TET_2027.md`.
- Chiến lược B2B tổng thể: `KE_HOACH_KHAI_THAC_B2B.md`.

## 2. Tài chính — biết lãi hay lỗ thật (thêm 2026-10-01)

Trước đây hệ thống chỉ theo dõi **doanh thu** (bán được bao nhiêu), không trừ **chi phí** (mua
nguyên liệu, in nhãn, bao bì, vận chuyển, quảng cáo...) — nên không ai biết đang thực sự lãi hay lỗ.
Giờ đã có đủ 2 vế:

- **Ghi chi phí**: `MO_APP_QUAN_LY.bat` → tab "Chi phí", hoặc nhờ Claude chạy `add_expense.py` (xem
  SOP mục 10). Làm ngay mỗi lần chi tiền — không ghi thì số lãi hiện ra sẽ cao giả.
- **Xem lãi/lỗ**: tab "Chi phí" trong app (tháng này) hoặc tab "Báo cáo" (theo khoảng ngày tuỳ chọn),
  hoặc `python scripts/weekly_report.py --thang-nay`.
- **Dữ liệu gốc**: `data/expenses.csv` (chi phí), `data/orders.csv` (doanh thu) — cùng cơ chế ghi an
  toàn (ghi file tạm rồi thay thế) như mọi sổ sách khác trong dự án.

## 3. Mục tiêu tăng trưởng — khung đo, KHÔNG tự đặt số

Claude không tự bịa mục tiêu doanh thu/lợi nhuận — đây là quyết định kinh doanh của bạn. Khung dưới
đây chỉ để bạn điền số thật khi sẵn sàng, không phải số đã có sẵn:

| Chỉ số | Cách xem | Mục tiêu tháng này |
|---|---|---|
| Doanh thu/tháng | `weekly_report.py --thang-nay` | `[CẦN BẠN ĐẶT]` → điền `doanh_thu_thang_vnd` vào `data/muc_tieu.json` |
| Lợi nhuận/tháng | cùng lệnh trên | `[CẦN BẠN ĐẶT]` → điền `loi_nhuan_thang_vnd` vào `data/muc_tieu.json` |
| Số khách quen (≥2 đơn) | `weekly_report.py --khach-quen` | theo dõi xu hướng, không cần số cố định |
| Số lead B2B đã liên hệ | Sổ Gọi Khách / tab "Bán hàng hôm nay" | theo nhịp 8-10 cuộc/ngày ở SOP mục 9 |
| Kênh bán hàng đang hoạt động | tự đếm (Facebook/Zalo/Shopee khi mở) | mở thêm kênh khi kênh cũ đã ổn định, không mở dồn dập |

Một khi điền số vào `data/muc_tieu.json`, mọi báo cáo (`--thang-nay`, tab "Chi phí") tự so sánh %
đạt được — không cần tính tay.

**Gợi ý cách đặt mục tiêu lần đầu** (không bắt buộc theo): nhìn doanh thu 1-2 tháng gần nhất (nếu đã
có dữ liệu thật trong `orders.csv`) làm mốc, đặt mục tiêu tháng tới cao hơn một chút (vd +10-20%)
thay vì đặt số lớn xa vời rồi nản vì không đạt.

## 4. Khi hệ thống này cần cập nhật

Thêm 1 mục mới vào đây khi: có quy trình lặp lại mới (→ thêm vào `SOP.md`), có cách đo mới (→ thêm
vào mục 3), hoặc nhịp làm việc hàng ngày/tuần/tháng thực tế đổi khác với mục 1. Đừng để file này lạc
hậu so với `CLAUDE.md`/`VIEC_CAN_LAM.md` — khi 2 bên mâu thuẫn, tin vào file nào mới cập nhật gần
đây hơn và sửa lại bên kia cho khớp.
