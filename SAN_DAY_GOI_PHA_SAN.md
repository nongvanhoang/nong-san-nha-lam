# Bước Tiếp Theo — Sắn Dây Gói Pha Sẵn

_Soạn 2026-07-28, tiếp theo đề xuất trong `MO_RONG_SAN_PHAM.md` mục 3._

## Vì sao làm bước này ngay bây giờ

Khác với Mứt/Siro Cam (phải đợi mùa cam ~T11/2026 mới có nguyên liệu thật để thử), sản phẩm này
**không phụ thuộc mùa vụ** — Sắn Dây đã có sẵn quanh năm, kênh Shopee/TikTok Shop cũng đã mở. Đây là
việc có thể bắt tay làm ngay tuần này, không phải chờ gì cả.

## Hai phương án phụ liệu — nên thử cả hai, để khách chọn

| Phương án | Gói kèm | Ghi chú |
|---|---|---|
| A | Sắn Dây + đường phèn | Dễ bảo quản (đường phèn khô, không hỏng), chi phí thấp hơn |
| B | Sắn Dây + hạt sen khô | Sang hơn, giá bán có thể cao hơn, nhưng cần kiểm tra hạt sen có bị mốc/mọt trước khi đóng gói |

Không cần chọn 1 — có thể bán song song 2 biến thể trên Shopee/TikTok Shop, để khách tự chọn theo
sở thích/ngân sách.

## Gợi ý đóng gói

- Mỗi gói nhỏ = khẩu phần 1 lần pha (đủ cho 1 ly), đóng túi zip nhỏ có tem dán tay — giữ đúng cảm
  giác "nhà làm" thay vì bao bì công nghiệp.
- Không thêm chứng nhận nào lên bao bì (đúng nguyên tắc đã thống nhất — Sắn Dây định vị trung thực
  "gia đình sản xuất nhỏ, thủ công", không có ATTP).
- Có thể đóng theo set 5 gói / 10 gói để tiện bán trên sàn (giống cách đang bán túi 0.5kg/1kg hiện
  tại trong `data/products.json`).

## Việc cần bạn chủ động làm trước

1. **Tìm nguồn phụ liệu**: đường phèn và hạt sen khô — kiểm tra giá sỉ, hạn sử dụng, nơi mua tin cậy
   (để giữ đúng tinh thần "nguyên liệu sạch" như Sắn Dây và Cam).
2. **Cân thử tỷ lệ mỗi gói**: ví dụ 1 gói Sắn Dây pha 1 ly cần bao nhiêu gram bột + bao nhiêu gram
   đường phèn/hạt sen — cân thử vài lần để ra định lượng chuẩn, dễ lặp lại.
3. **Đóng gói mẫu**: làm thử 5-10 gói, tự pha thử xem tỷ lệ có vừa miệng không, chỉnh lại nếu cần.

## Bảng ghi log thử nghiệm

| Lần thử | Ngày làm | Phương án (A/B) | Định lượng/gói | Vị (nếm) | Ghi chú |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

## Sau khi có kết quả

Khi chốt được định lượng chuẩn + tính được giá vốn, báo lại để:
- Thêm biến thể mới vào `data/products.json` (dạng `variant` mới của Sắn Dây).
- Viết mô tả sản phẩm cho Shopee/TikTok Shop dựa trên `content/templates/shopee_tiktok.md`.

---

## Tổng kết tiến độ 3 đề xuất mở rộng

| Đề xuất | Trạng thái |
|---|---|
| 1. Mứt/Siro Cam | Đã có kế hoạch thử nghiệm (`THU_NGHIEM_MUT_SIRO_CAM.md`), chờ bạn thực hiện |
| 2. Combo quà Tết | Đã có ý tưởng (`MO_RONG_SAN_PHAM.md` mục 2), chưa cần chốt gấp — còn thời gian đến trước T11/2026 |
| 3. Sắn Dây gói pha sẵn | Đã có kế hoạch thử nghiệm (file này), chờ bạn thực hiện |

Cả 3 đề xuất trong `MO_RONG_SAN_PHAM.md` giờ đều đã có bước hành động cụ thể đi kèm. Bước tiếp theo
thực sự phụ thuộc vào bạn — thử nghiệm thực tế (cân đo, nếm thử, ghi log) là việc Claude không làm
thay được. Khi có kết quả từ bất kỳ thử nghiệm nào, quay lại báo tôi để tính giá và viết nội dung
giới thiệu.
