# Kế Hoạch Khai Thác Data B2B — Tinh Bột Sắn Dây

_Chốt 2026-09-04. Tổng hợp lại toàn bộ kế hoạch đã thống nhất qua nhiều phiên làm việc — dùng file
này làm điểm bắt đầu mỗi khi quay lại việc B2B, thay vì đọc lại lịch sử chat._

## Tình trạng hiện tại

- **500 lead** trong `DANH_SACH_KHACH_HANG_B2B.csv`, chia 15 nhóm (A→O), 62 lead có email thật.
- **0 lượt liên hệ xác nhận** — đây là nút thắt thật, không phải thiếu data.
- Công cụ theo dõi: **[Sổ Gọi Khách](https://claude.ai/artifact/N7ySVZpN3mXcgBJz7SvCcJ)** —
  trang web riêng tư, mở trên điện thoại, chạm số để gọi/chạm email để gửi, đánh dấu trạng thái ngay.
  Sắp xếp sẵn theo đúng thứ tự ưu tiên bên dưới. **Đây là nơi làm việc chính**, không cần mở CSV.

## Nguyên tắc chỉ đạo (đừng phá vỡ)

1. **Không tìm thêm lead mới** cho đến khi liên hệ được ít nhất 50-100 lead hiện có. 500 lead đủ
   dùng nhiều tháng.
2. **Mục tiêu theo tuần, không theo tổng số lead** — nhìn "còn 490 lead chưa gọi" sẽ gây nản, chỉ
   nhìn "hôm nay gọi 8-10 cuộc".
3. **Việc dễ trước, việc khó sau** — đi tận nơi > gửi email > đăng 1 lần > gọi điện từng người, để
   xây đà trước khi làm việc khó nhất.
4. Có kết quả (kể cả "từ chối"/"không nghe máy") → báo lại → cập nhật `Trang_thai` trong CSV. Không
   im lặng bỏ qua, vì đó là cách duy nhất biết lead nào đã xử lý.

## Thứ tự triển khai

### Giai đoạn 0 — Phá băng (làm ngay, không cần "dám gọi điện")
| Việc | Chi tiết | Trạng thái |
|---|---|---|
| Đăng Facebook 1 lần | 2 group sỉ nguyên liệu chè, nội dung có sẵn | `content/templates/ban_si_quan_che.md` |
| Gửi email Nhóm N | 3 công ty quà Tết, **hạn chót thật tháng 10-11** | `content/templates/email_qua_tet_doanh_nghiep.md` |
| Đi tận nơi "sân nhà" Lạng Sơn | 12 mối: 2 khách sạn, 3 quán chè/trà sữa, 5 homestay, 2 cửa hàng thực phẩm sạch — lọc nhóm này trong Sổ Gọi Khách | Không tốn phí mẫu, phản hồi ngay |

### Giai đoạn 1 — Gọi điện trực tiếp (sau khi xong Giai đoạn 0)
Nhóm B (quán chè/trà sữa) + Nhóm F (đồ ăn cữ) — 2 nhóm này quán/spa nhỏ, ít đọc tin nhắn, gọi hiệu
quả hơn. Kịch bản + 25 số đầu tiên (Cao Bằng → Thái Nguyên → Bắc Ninh → Hải Phòng → Nam Định) đã có
sẵn ở `content/templates/kich_ban_goi_dien_quan_che.md`. Mục tiêu: 8-10 cuộc/ngày.

### Giai đoạn 2 — Cửa hàng/khách sạn có kênh chính thức (Nhóm H, J, K)
Gọi hoặc gửi email (nhiều mối đã có email thật). Nhóm J/K đã có mẫu email sẵn (2026-09-08) ở
`content/templates/email_thucpham_sach_dacsan.md`, 38 lead — lấy trực tiếp từ tab "Bán hàng hôm nay"
trong app local, lọc theo nhóm.

### Giai đoạn 3 — Kênh mới, thăm dò (Nhóm L, M — eat clean, nhà hàng Tây Bắc)
Chưa có tiền lệ thương mại, thử 2-3 mối mỗi nhóm trước khi mở rộng.

### Giai đoạn 4 — Nhà phân phối (Nhóm A)
Đòn bẩy cao nhất nhưng cần chuẩn bị kỹ hơn (họ hỏi số lượng/giá sỉ cụ thể) — làm sau khi đã quen
nhịp từ các nhóm dễ hơn.

### Không làm bây giờ
- **Nhóm D (xuất khẩu chính ngạch)** — khoá, chờ giấy ATTP.
- **Nhóm E (kiều bào)** — có thể làm sớm hơn D (không cần ATTP), nhưng ưu tiên thấp hơn các nhóm
  trong nước vì rủi ro hải quan + tốn công đóng gói quốc tế. Khi làm, bắt đầu bằng 1 gói mẫu <2kg gửi
  cửa hàng Việt tại Nhật (rủi ro thấp nhất).
- **Nhóm C, G** — mang tính thăm dò dài hạn, không kỳ vọng doanh thu sớm.

## Công cụ đã chuẩn bị sẵn

| File | Dùng khi nào |
|---|---|
| [Sổ Gọi Khách](https://claude.ai/artifact/N7ySVZpN3mXcgBJz7SvCcJ) | Dùng khi ở ngoài/trên điện thoại, không có máy tính — cần đồng bộ tay theo `scripts/sync_call_log_artifact.py` |
| App quản lý local, mục "Bán hàng hôm nay" (2026-09-08) — bấm `MO_APP_QUAN_LY.bat` | **Ưu tiên dùng khi đang ở máy tính** — đọc trực tiếp từ CSV nên luôn khớp 100%, không cần đồng bộ tay, có cả nút gọi/email + cập nhật trạng thái tại chỗ + bài cần đăng hôm nay |
| `DANH_SACH_KHACH_HANG_B2B.md` / `.csv` | Nguồn dữ liệu gốc, chi tiết đầy đủ từng lead |
| `content/templates/kich_ban_goi_dien_quan_che.md` | Kịch bản gọi điện Nhóm B, có sẵn 25 số đầu |
| `content/templates/email_qua_tet_doanh_nghiep.md` | Email 4 công ty quà Tết (Nhóm N) |
| `content/templates/email_thucpham_sach_dacsan.md` | Email mẫu Nhóm J (thực phẩm sạch) + Nhóm K (đặc sản quà biếu), 38 lead có email |
| `content/templates/ban_si_quan_che.md` | Bài đăng Facebook + mẫu nhắn tin Nhóm A/B |
| `DANH_SACH_GUI_HANG_LOAT.md` | Checklist chi tiết theo từng nhóm (đồng bộ đến ~418 lead, phần mới nhất lấy trực tiếp từ CSV) |

## Đồng bộ Sổ Gọi Khách (quy tắc đứng, tự làm không cần nhắc)

Mỗi khi `DANH_SACH_KHACH_HANG_B2B.csv` có thêm email mới hoặc thêm LEAD MỚI (sau khi tìm/xác minh),
Claude phải đồng bộ lại vào [Sổ Gọi Khách](https://claude.ai/artifact/N7ySVZpN3mXcgBJz7SvCcJ) bằng
`scripts/sync_call_log_artifact.py` (đọc artifact hiện tại → chạy script → publish lại đúng URL cũ)
trước khi báo hoàn tất cho người dùng — không để lệch dữ liệu giữa CSV và công cụ như đã từng xảy ra
(phát hiện 2026-09-08, artifact cũ dừng ở 62 email dù CSV đã có 146). Từ 2026-09-20, script này tự
thêm cả lead hoàn toàn mới (không chỉ điền email cho lead có sẵn) và tự sửa lại số "X mối liên hệ" —
không cần viết script riêng cho từng đợt thêm lead nữa.

## Cách cập nhật kết quả

Báo qua chat theo mẫu: "đã gọi/gửi [tên lead] — [kết quả]". Ví dụ: "đã gọi Cutisun — hẹn gọi lại
chiều mai", "đã gửi email SONA — chưa phản hồi". Sẽ được ghi vào cột `Trang_thai` trong CSV ngay.
