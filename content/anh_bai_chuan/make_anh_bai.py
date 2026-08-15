"""
Bộ ảnh bài chuẩn — ghép ảnh sản phẩm thật với khung thương hiệu (logo + tên) cố định,
tông màu đồng bộ với website (ink #14100c / gold #c9a227 / gold-soft #e6c878).
Chạy: python content/anh_bai_chuan/make_anh_bai.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS = os.path.join(ROOT, "docs", "assets")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

SIZE = 1080
BAR_H = 200
INK = (20, 16, 12, 235)       # #14100c, gần như đen, hơi trong suốt để lộ ảnh phía dưới
GOLD = (201, 162, 39, 255)    # #c9a227
GOLD_SOFT = (230, 200, 120, 255)  # #e6c878

FONT_BOLD = r"C:\Windows\Fonts\cambriab.ttf"
FONT_REG = r"C:\Windows\Fonts\cambria.ttc"

BRAND = "NÔNG SẢN NHÀ LÀM"

JOBS = [
    {
        "src": os.path.join(ROOT, "Hình Ảnh, Video", "Cam Đường Canh", "cam-duongcanh-hoaquanon-05.jpg"),
        "out": "post-cam-vuon-quanon.jpg",
        "subtitle": "Cam Đường Canh · VietGAP",
    },
    {
        "src": os.path.join(ASSETS, "tinh-bot-san-day-real-01.jpg"),
        "out": "post-che-san-day.jpg",
        "subtitle": "Tinh Bột Sắn Dây · Lạng Sơn",
    },
    {
        "src": os.path.join(ASSETS, "san-day-banhkhonut-real.jpg"),
        "out": "post-chao-si-san-day.jpg",
        "subtitle": "Tinh Bột Sắn Dây · Bán sỉ",
    },
]


def square_crop(im):
    w, h = im.size
    s = min(w, h)
    left = (w - s) // 2
    top = (h - s) // 3  # lệch lên trên chút để không cắt mất phần chủ thể hay nằm giữa-dưới khung ảnh
    top = min(top, h - s)
    return im.crop((left, top, left + s, top + s)).resize((SIZE, SIZE), Image.LANCZOS)


def make_one(src, out_name, subtitle):
    im = Image.open(src).convert("RGB")
    im = ImageOps.exif_transpose(im)
    im = square_crop(im)
    canvas = im.convert("RGBA")

    # thanh gradient tối ở đáy để chữ luôn đọc được trên mọi ảnh nền
    grad = Image.new("L", (1, BAR_H), color=0)
    for y in range(BAR_H):
        a = int(235 * (y / BAR_H) ** 1.4)
        grad.putpixel((0, y), a)
    grad = grad.resize((SIZE, BAR_H))
    overlay = Image.new("RGBA", (SIZE, BAR_H), INK[:3] + (0,))
    overlay.putalpha(grad)
    canvas.alpha_composite(overlay, (0, SIZE - BAR_H))

    # logo tròn góc trái dưới
    logo = Image.open(os.path.join(ASSETS, "icon-512.png")).convert("RGBA")
    logo_size = 96
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    logo_pos = (36, SIZE - BAR_H // 2 - logo_size // 2 - 6)
    canvas.alpha_composite(logo, logo_pos)

    draw = ImageDraw.Draw(canvas)
    text_x = logo_pos[0] + logo_size + 24
    f_brand = ImageFont.truetype(FONT_BOLD, 42)
    f_sub = ImageFont.truetype(FONT_REG, 32)
    brand_y = SIZE - BAR_H // 2 - 44
    sub_y = brand_y + 52
    draw.text((text_x, brand_y), BRAND, font=f_brand, fill=GOLD)
    draw.text((text_x, sub_y), subtitle, font=f_sub, fill=GOLD_SOFT)

    # viền vàng mảnh quanh toàn bộ khung, đồng bộ nhận diện với logo
    draw.rectangle([0, 0, SIZE - 1, SIZE - 1], outline=GOLD, width=4)

    canvas.convert("RGB").save(os.path.join(OUT_DIR, out_name), quality=92)


def main():
    made = []
    for job in JOBS:
        make_one(job["src"], job["out"], job["subtitle"])
        made.append(job["out"])
    with open(os.path.join(OUT_DIR, "_log.txt"), "w", encoding="utf-8") as f:
        f.write("Da tao: " + ", ".join(made) + "\n")


if __name__ == "__main__":
    main()
