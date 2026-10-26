# Hướng Dẫn Khai Thác — Dùng Những Gì Đã Xây (2026-09-28)

_File này KHÁC `VIEC_CAN_LAM.md` (liệt kê việc còn treo, cần làm gì) — file này trả lời câu "tôi đã
có sẵn công cụ gì rồi, dùng nó như thế nào mỗi ngày/mỗi tuần?". Đọc 1 lần để nắm nhịp làm việc, sau
đó chỉ cần quay lại phần nào cần thôi._

## 0. Việc chạy sẵn, bạn không cần làm gì

Hai việc này đã cài vào Windows Task Scheduler, tự chạy nền, không cần mở app:

- **Mỗi 3 ngày, 9h sáng**: máy tự bật Notepad hiện bài đăng tiếp theo (nội dung + gợi ý ảnh/video) —
  file `BAI_DANG_HOM_NAY.txt`. Việc của bạn: đọc, copy, dán lên Facebook/Zalo/Instagram/TikTok thật
  (KHÔNG có bước tự động đăng — luật cứng của dự án). Xong thì thôi, không cần bấm gì để "tắt nhắc".
- **Mỗi thứ Hai, 9h sáng**: máy tự bật Notepad hiện báo cáo tuần — doanh thu, tồn kho, khách quen —
  file `BAO_CAO_TUAN.txt`. Nếu thấy toàn số 0, đó là dấu hiệu bạn quên ghi đơn hàng thật (xem mục 1).

Muốn xem 2 việc này đang chạy đúng lịch không: mở PowerShell, gõ
`schtasks /query /tn NongSanNhaLam_SocialReminder` hoặc `NongSanNhaLam_WeeklyDigest`.

## 1. Việc quan trọng nhất mỗi ngày: ghi đơn hàng thật

Toàn bộ báo cáo doanh thu/tồn kho/khách quen đã xây đều vô nghĩa nếu `data/orders.csv` trống —
**hiện tại file này đang trống hoàn toàn**, đây là lỗ hổng lớn nhất, không phải do thiếu công cụ mà
do chưa thành thói quen ghi.

**Cách ghi (30 giây/đơn, chọn 1 trong 2 cách):**
1. Bấm `MO_APP_QUAN_LY.bat` → mục "Ghi đơn hàng" — điền khách/sản phẩm/số lượng/đơn giá/kênh bán.
2. Hoặc nhờ Claude ngay trong chat: "ghi đơn khách X mua 2 túi 1kg sắn dây qua Zalo giá 155k/túi" —
   Claude tự chạy `add_order.py` đúng tham số.

**Lưu ý duy nhất cần nhớ**: luôn quy đổi số lượng ra **kg** (không phải theo thùng/túi) — ví dụ "2
thùng cam 10kg" thì số lượng ghi là 20kg, không phải 2. Cả 2 cách ghi ở trên đều tự làm đúng việc
này nếu bạn nói rõ số kg hoặc số thùng/túi + quy cách.

## 2. Nội dung mạng xã hội — lấy ảnh/video nhanh

Khi cần ảnh/video cho 1 bài viết (kể cả bài ngoài lịch nhắc 3 ngày/lần):

1. Mở `MO_APP_QUAN_LY.bat` → tab **"Thư viện Media"**.
2. Gõ từ khoá (tên sản phẩm, hoặc "chưa dùng" để lọc ảnh/video chưa lên bài nào) → bấm vào file cần
   → đường dẫn tự copy vào clipboard, dán thẳng vào nơi cần (Messenger, USB, app chỉnh sửa...).

Nếu ảnh chưa có logo/chú thích thương hiệu, chạy:
```
python content/video/make_branded_photo.py "<ảnh gốc>" "<chú thích>" "<ảnh ra>"
```
Tự thêm logo góc phải + dải chú thích, không cần mở Canva.

## 3. Khách hàng trong nước (B2B) — nhịp gọi điện hàng ngày

Mục tiêu: **8-10 cuộc/ngày**, không nhìn tổng "còn bao nhiêu lead chưa gọi" (gây nản) mà chỉ nhìn hôm
nay đã gọi bao nhiêu cuộc.

1. Mở [Sổ Gọi Khách](https://claude.ai/artifact/N7ySVZpN3mXcgBJz7SvCcJ) trên điện thoại (đã sắp sẵn
   theo đúng thứ tự ưu tiên Giai đoạn 0→4) hoặc mở `MO_APP_QUAN_LY.bat` → tab "Bán hàng hôm nay" nếu
   đang ở máy tính (luôn khớp CSV 100%, không cần đồng bộ tay như bản artifact).
2. Bấm số điện thoại/email trực tiếp trên trang, đọc theo kịch bản có sẵn nếu là Nhóm B (quán chè):
   `content/templates/kich_ban_goi_dien_quan_che.md` — hiện đang ở "Đợt gọi 3" (7 quán Ninh Bình).
3. **Gọi xong luôn báo lại kết quả cho Claude** (kể cả "không nghe máy") để cập nhật đúng trạng thái
   trong CSV — đây là bước duy nhất giữ dữ liệu không bị lệch.
4. Hết 1 đợt, nhắn Claude "cho tôi batch tiếp theo" để lấy danh sách/kịch bản mới.

Chi tiết chiến lược đầy đủ (nhóm nào làm trước, nhóm nào đang khoá): `KE_HOACH_KHAI_THAC_B2B.md`.

## 4. Khách hàng quốc tế (Nhóm E — kiều bào) — gửi mẫu thử

32 lead trải 12 quốc gia đã có sẵn tin nhắn/email soạn theo đúng tên từng lead, không cần tự điền gì:

1. Mở `content/templates/chao_hang_nhom_e_ca_nhan_hoa.md`.
2. **Gửi đúng thứ tự từ trên xuống** (đã sắp theo rủi ro hải quan tăng dần: Nhật Bản trước tiên, Úc
   cuối cùng) — không gửi đồng loạt nhiều nước cùng lúc khi chưa có kết quả thật nào.
3. Copy đúng đoạn của lead đó, điền tên bạn vào `[tên bạn]`, gửi qua đúng kênh ghi sẵn (email/điện
   thoại/Facebook).
4. Gửi xong, báo Claude để cập nhật CSV thành "Đã gửi mẫu — chờ qua hải quan".
5. Một vài lead có cách tiếp cận khác hẳn (không phải "chào mẫu"), đọc kỹ ghi chú trước khi gửi:
   Đồng Xuân Center (hỏi đầu mối, không gửi thẳng), Miss Linh/Tamda (xin đăng ký làm nhà cung cấp),
   Úc (chưa gửi gì cho đến khi tự tra BICON), 2 lead ở Mỹ (là dịch vụ vận chuyển, không phải khách).

## 5. Chuẩn bị gian hàng Shopee/TikTok Shop

Khi đã sẵn sàng đăng ký gian hàng thật (còn thiếu: quyết định chính sách đổi/trả ở `VIEC_CAN_LAM.md`
Nhóm 2, và ảnh #1 chờ nhãn in xong), mọi nội dung cần điền đã có sẵn ở `HO_SO_MANG_XA_HOI.md` mục 3:

- Tên gian hàng, giới thiệu gian hàng, mô tả sản phẩm — copy đúng đoạn.
- Tên sản phẩm (tiêu đề đăng bán) + bảng phân loại giá 0.5kg/1kg — mục "Tên sản phẩm + phân loại
  hàng khi đăng thật" (thêm 2026-09-28).
- 7/8 ảnh đã đóng thương hiệu sẵn trong `docs/assets/shopee/`, lấy nhanh qua tab "Thư viện Media".
- 2 video sẵn dùng ngay, không cần chờ nhãn (`content/video/output/`).
- 4 câu hỏi khách hay hỏi qua khung chat sàn đã soạn sẵn câu trả lời (hạn dùng, COD, hàng thật
  không, đổi trả) — cùng mục trên.

## 6. Khi không biết bắt đầu từ đâu

- Muốn biết **việc gì đang treo, ai cần làm gì** → `VIEC_CAN_LAM.md` (4 nhóm theo độ dễ/khó).
- Muốn biết **chiến lược B2B tổng thể** → `KE_HOACH_KHAI_THAC_B2B.md`.
- Muốn biết **hồ sơ từng kênh mạng xã hội đã điền gì, còn thiếu gì** → `HO_SO_MANG_XA_HOI.md`.
- Muốn Claude **đề xuất bước tiếp theo** → chỉ cần nhắn "đề xuất bước tiếp", Claude sẽ tự nhìn 3 file
  trên để đề xuất đúng việc còn thiếu, không lặp lại việc đã xong.

## 7. Trợ lý Claude tự nhắc & tự học (thêm 2026-09-29, lấy ý tưởng từ bộ ECC)

- **Mỗi lần mở Claude trong thư mục này**, Claude tự hiện số việc còn treo trong `VIEC_CAN_LAM.md`
  và 5 việc đầu tiên — không cần hỏi "còn gì cần làm".
- **Cuối buổi làm việc dài**, gõ `/rut-kinh-nghiem` → Claude tự rút những lần bạn đã sửa lại cách
  làm của nó (ví dụ cách xưng hô với khách, giá, cách viết bài) và ghi nhớ, lần sau không sai lại.
- **Viết bài bán hàng / nghiên cứu khách sỉ**: Claude có thêm 3 bộ kỹ năng `content-engine` (chuyển
  1 nội dung thành bài cho từng kênh Facebook/Zalo/TikTok), `article-writing` (bài dài) và
  `market-research` (nghiên cứu đối thủ, nhà nhập khẩu — luôn ghi nguồn). Chỉ cần nhắn yêu cầu như
  bình thường, Claude tự dùng.
- Khi phiên chat quá dài, Claude sẽ nhắc nên `/compact` (thu gọn) để khỏi tốn lượt dùng.

## 8. Ghi đơn ngay trên điện thoại (thêm 2026-09-30)

- Mở **Sổ Đơn Nhà Làm**: https://claude.ai/artifact/U6UNTk3bF9fiehZLdoQwEs (lưu vào màn hình chính điện
  thoại cho nhanh). Chọn Nông Sản hoặc Tiệm Cháo → bấm sản phẩm → số lượng → tên khách → **Lưu đơn**. ~30 giây.
- Tab **Khách chờ cam**: ai hẹn "báo khi có cam" thì thêm vào đây; vào mùa bấm "Chưa báo" → "Đã báo" sau khi nhắn.
- Tab **Đã ghi**: doanh thu hôm nay / 7 ngày; ghi nhầm thì bấm "Xoá" 2 lần (chỉ xoá được đơn chưa đồng bộ).
- Mỗi tối hoặc cuối tuần nhắn Claude **"đồng bộ đơn"** → đơn tự chép về `data/orders.csv` (quy ra kg đúng
  luật sổ) và sổ của Tiệm Cháo, rồi báo cáo tuần chạy như cũ.
- Dữ liệu khách (tên, SĐT) nằm trong kho riêng tư trên claude.ai của bạn — không ai khác đọc được.

## 9. Trang đặt trước trên website (thêm 2026-10-10)

`https://thehungorganic.com/dat-truoc.html` — khách tự chọn hàng (cam 5kg/10kg, hộp quà Tết, sắn dây),
điền tên + SĐT, bấm gửi → tin nhắn soạn sẵn tới **Zalo 0979 502 000** (khách dán rồi gửi), WhatsApp
hoặc email `hello@`. Web KHÔNG lưu gì — mọi phiếu đến qua tin nhắn, nên:

- Nhận được tin "ĐẶT TRƯỚC — thehungorganic.com" trên Zalo → sao chép tin → mở **Sổ Đơn** (mục 8) → tab
  "Khách chờ cam" → dán vào ô "Dán phiếu ĐẶT TRƯỚC" → **Tách phiếu** → kiểm tra → **Thêm**. ~10 giây.
  Đừng ghi thẳng vào `data/danh_sach_cho.csv` — "đồng bộ đơn" ghi đè file đó từ Sổ Đơn.
  Mã nguồn trang Sổ Đơn: `scripts/artifacts/so_don_nha_lam.html` (sửa file này rồi đăng lại cùng link).
- Các bài trong hàng đợi nhắc đăng (hẹn báo mùa cam, hộp quà Tết, quà doanh nghiệp, bài vào mùa) đã có sẵn
  link đặt trước chọn sẵn hàng.
- **Link chọn sẵn hàng để dán vào bài đăng**: thêm `?chon=` vào cuối link — `dat-truoc.html?chon=cam5`,
  `?chon=cam10`, `?chon=qua-nho`, `?chon=qua-lon`, `?chon=sd05`, `?chon=sd1`, nhiều món cách nhau dấu
  phẩy (`?chon=qua-nho,sd1`).
- Khi chốt giá hộp quà: nhắn Claude để thay dòng "giá báo khi nhà mình nhắn lại" bằng giá thật
  (`data-price` trong `docs/dat-truoc.html`).
