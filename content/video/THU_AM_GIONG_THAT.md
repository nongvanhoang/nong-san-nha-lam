# Thu âm giọng thật cho video giới thiệu (trang chủ)

Video đang dùng giọng máy (giọng nam miền Bắc). Giọng người nhà/anh Chiến đọc sẽ thật và ấm hơn hẳn.
Chỉ cần điện thoại, khoảng 15 phút.

## Cách thu

1. Vào phòng kín, đóng cửa, tắt quạt/tivi. Ngồi cạnh rèm, chăn, tủ quần áo càng tốt (đỡ vang).
2. Mở app **Ghi âm** có sẵn trên điện thoại. Cầm máy cách miệng khoảng 1 gang tay, hơi chếch sang
   một bên (để tiếng "p", "b" không phì vào mic).
3. **Mỗi đoạn dưới đây thu thành 1 file riêng.** Đọc lỗi thì đọc lại cả đoạn, giữ bản ưng nhất.
4. Đọc như đang kể cho khách đến thăm vườn nghe: chậm, rõ, không cần "đọc diễn cảm". Giọng địa phương
   càng tốt, đó chính là cái thật.
5. Đặt tên file đúng `doan-1`, `doan-2`, …, `doan-7` (đuôi .m4a/.mp3 gì cũng được), chép vào thư mục
   `content/video/giong_that/gioi-thieu-thoc/` rồi nhắn Claude: "đã có file thu âm, ghép vào video".

Số giây là thời lượng cảnh tương ứng: đọc **trong khoảng** đó thì lời khớp hình. Dài hơn vài giây cũng
không sao, máy tự lùi đoạn sau, sẽ báo nếu lệch nhiều.

| File | Đọc (≤ giây) | Lời |
|---|---|---|
| doan-1 | 8 | Ở xã Vũ Lăng, giữa những dãy núi đá vôi Bắc Sơn, Lạng Sơn, Hợp tác xã Thế Hưng Organic trồng sắn dây ngay trên mảnh đất quê mình. |
| doan-2 | 8 | Dây leo đã phủ kín giàn. Hoa sắn dây nở tím cả nương, còn củ thì lặng lẽ lớn dần dưới đất. |
| doan-3 | 7 | Đến mùa, cả gốc củ được đào lên. Củ to, chắc, vẫn còn nguyên đất. |
| doan-4 | 19 | Củ được cân ngay tại xưởng, rửa thật sạch đất cát, rồi đưa vào máy nghiền, ép lấy nước bột. Nước bột khuấy đều, để lắng xuống đáy bể. Rồi thay nước, khuấy, lắng, lọc đi lọc lại nhiều lượt, cho đến khi bột thật trắng, thật trong. |
| doan-5 | 23 | Bột ướt được nặn thành từng miếng, xếp lên khay, đưa vào lò sấy nhiều tầng. Nhiệt độ cài sẵn, nên bột khô đều, chẳng phụ thuộc nắng mưa. Không hoá chất, không chất tẩy trắng. Màu trắng ấy là màu tự nhiên của bột. Ra lò là đóng túi ngay, có sẵn quanh năm. |
| doan-6 | 19 | Cùng với sắn dây là Cam Đường Canh, trồng theo tiêu chuẩn VietGAP. Cam để chín tự nhiên trên cây, không thúc chín. Quả mọng nước, ngọt thanh. Khoảng tháng mười một âm lịch, cam được hái tay đúng mùa, phân loại, đóng thùng cẩn thận, rồi gửi đi khắp cả nước. |
| doan-7 | 7 | Thế Hưng Organic. Nông sản thật, từ vùng núi Bắc Sơn. *(đọc chậm, chắc giọng: đây là câu chốt)* |

Muốn sửa lời cho đúng cách nói của nhà mình thì cứ sửa khi đọc, chỉ cần báo lại để cập nhật phụ đề.

## Phần kỹ thuật (cho Claude)

Thêm `"recorded": "content/video/giong_that/gioi-thieu-thoc"` vào `narration` trong
`configs/gioi-thieu-thoc.json` (giữ nguyên `text` + `align`), rồi chạy
`python make_process_video.py --config configs/gioi-thieu-thoc.json --chi-am-thanh` và xuất bản web
1280:720 như `dung_lai_va_xuat_web.sh`. Script tự lọc ồn (afftdn), cắt lặng, đặt đoạn theo `align`,
chuẩn hoá âm lượng. Nếu lời sửa khác `text` thì sửa `text` + `captions` cho khớp. Thư mục `giong_that/`
đã gitignore (file thu âm gốc, giọng người thật, không cần lên repo public).
