"""Tạo ảnh đại diện logo THOC vừa khung TRÒN (Facebook, Zalo, Shopee, TikTok, Instagram, YouTube cắt ảnh đại diện thành hình tròn).
Logo gốc hình bầu dục nằm ngang nên bị cắt 2 đầu — script này bỏ viền bầu dục, vẽ lại viền tròn và đặt nội dung vào giữa.
Chạy: python scripts/tao_logo_tron.py  → ghi vào content/kenh_assets/logo-tron/
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs/assets/logo-thoc.jpg"
OUT = ROOT / "content/kenh_assets/logo-tron"
GREEN = (27, 94, 42)
S = 4  # vẽ to gấp 4 rồi thu nhỏ cho viền mịn

src = Image.open(SRC).convert("RGB")
w, h = src.size
cx, cy, a, b = 617.5, 412, 560, 376  # viền bầu dục ngoài (đo từ ảnh gốc)

def content(inner=0.9, text=True):
    """Phần ruột logo (bỏ viền bầu dục), nền trong suốt."""
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse([cx - a * inner, cy - b * inner, cx + a * inner, cy + b * inner], fill=255)
    rgb = np.array(src).astype(int)
    # độ "không trắng" làm alpha để ghép lên nền bất kỳ không bị viền xám
    alpha = np.clip((765 - rgb.sum(2)) * 255 / 300, 0, 255).astype(np.uint8)
    alpha = np.minimum(alpha, np.array(mask))
    if not text:
        alpha[620:, :] = 0
    im = src.convert("RGBA")
    im.putalpha(Image.fromarray(alpha))
    return im.crop(im.getbbox())

def fit_in_circle(img, radius):
    """Thu nhỏ để MỌI điểm có màu nằm trong vòng tròn bán kính radius."""
    al = np.array(img.split()[3]) > 40
    ys, xs = np.where(al)
    hh, ww = al.shape
    d = np.sqrt((xs - ww / 2) ** 2 + (ys - hh / 2) ** 2).max()
    k = radius / d
    return img.resize((round(ww * k), round(hh * k)), Image.LANCZOS)

def badge(size, rings=True, text=True, name="x"):
    big = size * S
    can = Image.new("RGBA", (big, big), (255, 255, 255, 255))
    d = ImageDraw.Draw(can)
    r = big / 2
    if rings:
        m = big * 0.035
        d.ellipse([m, m, big - m, big - m], outline=GREEN, width=round(big * 0.022))
        m2 = big * 0.075
        d.ellipse([m2, m2, big - m2, big - m2], outline=GREEN, width=round(big * 0.006))
        inner_r = r - big * 0.11
    else:
        inner_r = r * 0.86
    c = fit_in_circle(content(text=text), inner_r)
    # dịch lên một chút cho cân mắt (rễ nặng phía dưới)
    can.alpha_composite(c, (round(r - c.width / 2), round(r - c.height / 2)))
    out = can.resize((size, size), Image.LANCZOS).convert("RGB")
    p = OUT / f"{name}.png"
    out.save(p, optimize=True)
    print(p.relative_to(ROOT))

OUT.mkdir(parents=True, exist_ok=True)
badge(1080, rings=True, text=True, name="logo-tron-day-du-1080")     # có viền tròn + chữ HTX
badge(1080, rings=False, text=False, name="logo-tron-bieu-tuong-1080")  # chỉ biểu tượng, dễ nhìn khi ảnh nhỏ
badge(1080, rings=True, text=False, name="logo-tron-vien-1080")       # biểu tượng + viền tròn, không chữ
