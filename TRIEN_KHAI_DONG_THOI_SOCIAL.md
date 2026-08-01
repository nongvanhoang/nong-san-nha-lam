# Đề Xuất Triển Khai Đồng Thời Trên Social

_Soạn 2026-07-28. Phát hiện: `content/posts_ready.md` hiện có **17 bài đã soạn sẵn nhưng chưa bài
nào được đánh dấu `[Đã đăng]`** — nghĩa là có sẵn một kho nội dung tốt (dựa trên ảnh/video thật quay
2026-07-25/26) đang nằm im, đúng lúc cần đẩy mạnh Sắn Dây mùa hè theo Giai đoạn 1 của
`KE_HOACH_BAN_HANG.md`. Đề xuất dưới đây là lịch đăng đồng thời nhiều kênh, dùng đúng nội dung có
sẵn — không cần soạn thêm mới ngay._

**Nhắc lại giới hạn đã thống nhất**: Claude không tự đăng bài lên bất kỳ nền tảng nào — đây là lịch
để bạn tự copy-paste đăng tay theo đúng ngày/kênh đề xuất.

## Đợt 1 — Đăng ngay (cùng ngày, nhiều kênh cùng lúc)

Chủ đề: **"Thu hoạch thật, không dàn dựng"** — mạnh nhất vì có video thật đi kèm, nên đẩy đồng thời
để câu chuyện nhất quán khi khách lướt qua nhiều kênh cùng lúc.

| Kênh | Nội dung dùng | Vị trí trong `posts_ready.md` |
|---|---|---|
| Facebook | "Quy mô thu hoạch thật, không phải làm cho có" | dòng 69 |
| Zalo | "Báo khách quen có ảnh/video thật mới" | dòng 105 |
| TikTok/Reels | Video thu hoạch củ sắn dây (`san-day-video-thuhoach-dung-01.mp4`) | dòng 54 |

## Đợt 2 — Cách đợt 1 khoảng 3-4 ngày (giữ nhịp 2-3 bài/tuần theo kế hoạch)

Chủ đề: **Cách dùng + hậu trường phơi bột** — hướng vào nhu cầu giải nhiệt mùa hè.

| Kênh | Nội dung dùng | Vị trí |
|---|---|---|
| Facebook | "3 cách dùng tinh bột sắn dây giải nhiệt ngày hè" | dòng 30 |
| Zalo/Facebook | "Từ video thật đến túi tinh bột, không giấu gì cả" | dòng 113 |
| TikTok/Reels | Video hậu trường phơi sắn dây | dòng 88 (khu vực dòng 87-101) |
| Shopee/TikTok Shop | Mô tả sản phẩm Tinh Bột Sắn Dây | dòng 262 — **kiểm tra lại xem gian hàng đã đăng ký xong chưa (việc bạn tự làm, Giai đoạn 1 mục 5); nếu xong rồi thì dùng bài này hoàn thiện listing** |

## Đợt 3 — Song song, tần suất thấp hơn (1 bài/~1-2 tuần) — hâm nóng khách chờ mùa Cam

Không cần đợi đến Giai đoạn 2 (T9-10) mới bắt đầu — bài này đã sẵn và dùng ảnh quả non thật, có thể
bắt đầu sớm nhẹ nhàng, xen kẽ giữa các đợt Sắn Dây ở trên, không lấn át chủ lực mùa hè.

| Kênh | Nội dung dùng | Vị trí |
|---|---|---|
| Facebook + Zalo | "Cập nhật vườn cam, quả non đã đậu trên cành" | dòng 9 |

## Nội dung cũ nên bỏ qua (đã có bản mới hơn/tốt hơn thay thế)

Không đề xuất xoá ngay (để bạn tự quyết), nhưng khi đăng theo lịch trên thì **không cần dùng** các
bài sau vì đã trùng ý hoặc dựa trên ảnh minh hoạ cũ (trước khi có ảnh/video thật):

- Dòng 187 "Hậu trường sản xuất Tinh Bột Sắn Dây" (07-05) → đã có bản thay thế mạnh hơn ở Đợt 2.
- Dòng 209 "TikTok — Video hậu trường phơi sắn dây" (07-05, chỉ là kịch bản dự kiến) → file đã tự
  ghi chú "video này đã thay thế", có video thật ở Đợt 2 rồi.
- Dòng 238 "Công dụng / cách dùng Tinh Bột Sắn Dây" (07-03) → bản 07-26 "3 cách dùng..." chi tiết
  và hấp dẫn hơn.
- Dòng 130 "Mời khách để lại hẹn báo hàng mùa cam" (07-06) → trùng mục đích với bài Đợt 3, bản 07-26
  mới hơn (có ảnh quả non thật) nên dùng bản đó thay vì bản cũ chỉ có chữ.

Các bài "soạn trước cho mùa tới" nhấn VietGAP / chín tự nhiên trên cây (dòng 147, 167, 277) — **giữ
nguyên, chưa đăng**, để dành đúng cho Giai đoạn 2 (T9-10/2026) như kế hoạch gốc, không đăng sớm kẻo
lặp ý với Đợt 3 ở trên.

## Sau khi đăng

Đánh dấu `[Đã đăng]` vào đầu tiêu đề từng bài trong `content/posts_ready.md` sau khi đăng thật, để
lần sau biết bài nào dùng rồi — hiện chưa bài nào được đánh dấu nên khó biết đã đăng gì.

Khi đăng hết nội dung có sẵn ở 3 đợt trên, báo lại để soạn thêm — có thể dùng subagent
`sales-content-writer` để ra content mới đồng bộ cho cả 3 kênh cùng lúc.
