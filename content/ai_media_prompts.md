# Prompt tạo ảnh/video AI (tạm dùng trước khi có ảnh/video thật)

Đây là các prompt tiếng Anh (AI tạo ảnh/video hiểu tiếng Anh tốt nhất), dán trực tiếp vào công cụ
bạn có (Midjourney, DALL·E/ChatGPT Images, Nano Banana, Sora, Pika...). Tải ảnh/video về, đặt vào
`docs/assets/` rồi nhờ Claude thay vào `docs/index.html` / `docs/en/index.html`.

**Lưu ý quan trọng khi chọn ảnh AI ra:**
- Không chọn ảnh nào có chữ/logo/tem nhãn bị lỗi (AI hay vẽ chữ sai) — nếu ảnh dính chữ lạ, tạo lại
  hoặc chọn ảnh không có chữ.
- Không dùng ảnh AI để "chứng minh" VietGAP hay bất kỳ giấy tờ nào — chứng nhận đã ghi bằng chữ thật
  trên web rồi, ảnh chỉ minh hoạ sản phẩm/khung cảnh, không vẽ tem/nhãn giả.
- Đây vẫn là ảnh minh hoạ, không phải ảnh thật — khi có ảnh/video tự chụp, ưu tiên thay thế dần vì
  khách tin ảnh thật hơn nhiều (xem README).

---

## 1. Tinh Bột Sắn Dây

### 1a. Ảnh sản phẩm (hero ảnh trên web, tỉ lệ 4:3 hoặc 1:1)
```
Product photo of a small paper pouch of white starch powder (Vietnamese arrowroot/kudzu starch),
rustic kraft packaging with a simple twine tie, no visible brand text or logo, placed on a wooden
table with natural sunlight from the side, a few dried arrowroot roots and a wooden spoon with
white powder next to it, warm homemade/artisanal mood, shallow depth of field, soft shadows,
no people, no readable text on packaging
```

### 1b. Ảnh hậu trường (quy trình lọc/phơi — cho bài "hậu trường sản xuất")
```
Close-up photo of hands straining white starch milk through cloth into a large basin, water
dripping, traditional Vietnamese rural kitchen setting, natural daylight, documentary food-process
photography style, warm tones, no faces visible, focus on hands and liquid motion
```
```
Photo of white starch spread thinly on trays drying under strong natural sunlight in a rural
Vietnamese countryside yard, blue sky, simple bamboo or wooden trays, documentary style, bright
and clean, no people
```

### 1c. Ảnh lifestyle (ly nước pha / chè sắn dây)
```
Top-down photo of a glass of milky-white arrowroot starch drink with ice cubes, condensed on the
glass, sitting on a wooden table with a small spoon beside it, bright natural light, minimal
clean background, appetizing food photography style
```

### 1d. Video ngắn (Sora/Pika, 10-15s, dùng cho TikTok/Reels)
```
A short documentary-style video: close-up of hands filtering white starch milk through cloth into
a basin, water dripping slowly; cut to trays of white starch powder drying under bright sunlight
in a rural Vietnamese yard; cut to a hand packing the dried white powder into a small kraft paper
pouch. Warm natural lighting throughout, calm and authentic homemade mood, no text overlay, no
faces, 15 seconds
```

---

## 2. Cam Đường Canh

### 2a. Ảnh sản phẩm (thùng cam, tỉ lệ 4:3 hoặc 1:1)
```
Product photo of a wooden crate filled with small Vietnamese tangerines (cam đường canh, thin
orange-green peel), some loose fruits scattered beside the crate on a rustic wooden surface,
natural daylight, vibrant orange color, a few green leaves still attached to some fruits, no
visible text or labels on the crate, clean warm background
```

### 2b. Ảnh cây/vườn (cho phần giới thiệu HTX/VietGAP bằng chữ)
```
Photo of a citrus tree branch heavy with small ripe orange tangerines, green leaves, natural
outdoor orchard setting in northern Vietnam, soft morning sunlight, shallow depth of field
background of more citrus trees, no people, no signage, realistic photography style
```

### 2c. Ảnh cận cảnh (bổ cam / múi cam)
```
Close-up photo of a peeled Vietnamese tangerine (cam đường canh) split into segments on a wooden
plate, juicy texture visible, bright natural light, a few whole tangerines and green leaves beside
it, appetizing food photography, no text
```

### 2d. Video ngắn (Sora/Pika, 10-15s)
```
A short documentary-style video: slow pan across a citrus orchard with ripe orange tangerines on
the trees in soft morning light; cut to a hand gently picking a ripe tangerine; cut to tangerines
being placed into a wooden crate. Warm natural outdoor lighting, calm authentic farm mood, no text
overlay, no faces close-up, 15 seconds
```

---

## Gợi ý tỉ lệ khung hình theo chỗ dùng
- Ảnh hero trên web (`docs/index.html`): 4:3 hoặc 16:9
- Ảnh vuông cho Facebook/Zalo post: 1:1
- Video TikTok/Reels: 9:16 dọc (thêm `--ar 9:16` nếu dùng Midjourney cho ảnh nền, hoặc chọn khung
  dọc trực tiếp trong tool video)
