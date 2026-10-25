"""Cắt phần hình (lá, củ sắn dây, núi) từ ảnh thiết kế bao bì gốc thành PNG nền trong suốt, mép mờ,
để ghép vào bản in sạch (scripts/tao_bao_bi.js). Chữ trên bản gốc bị sai dấu nên KHÔNG lấy chữ, chỉ lấy hình.
"""
from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content/nhan_bao_bi/thiet-ke-2026-10-25"
OUT = ROOT / "content/nhan_bao_bi/bao-bi-moi/anh"
CREAM = np.array([245, 241, 226])

def ramp(n, f):
    r = np.ones(n)
    if f:
        k = int(n * f)
        r[:k] = np.linspace(0, 1, k) ** 1.5
    return r

def cut(src, box, name, fade=(0, 0, 0, 0), key=False, flip=False):
    """fade = (trái, trên, phải, dưới) tỷ lệ mép làm mờ; key = xoá nền kem quanh lá."""
    im = Image.open(SRC / src).convert("RGB").crop(box)
    a = np.array(im).astype(float)
    h, w = a.shape[:2]
    al = np.outer(ramp(h, fade[1]) * ramp(h, fade[3])[::-1], ramp(w, fade[0]) * ramp(w, fade[2])[::-1])
    if key:
        d = np.sqrt(((a - CREAM) ** 2).sum(2))
        k = np.clip((d - 14) / 30, 0, 1)
        k = np.array(Image.fromarray((k * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))) / 255
        al = al * k
    out = Image.fromarray(np.dstack([a, al * 255]).astype(np.uint8), "RGBA")
    if flip:
        out = out.transpose(Image.FLIP_LEFT_RIGHT)
    out.save(OUT / f"{name}.png", optimize=True)
    print(name, out.size)

OUT.mkdir(parents=True, exist_ok=True)
# Củ sắn dây + bát bột (mặt trước), bỏ con dấu ORGANIC bên phải và chữ bên trái
cut("tui-500g-mat-truoc.jpg", (330, 990, 975, 1745), "cu-va-bot", fade=(0.10, 0.22, 0.12, 0.04))
# Núi đồi (mặt sau)
cut("tui-500g-mat-sau.jpg", (0, 440, 1385, 740), "nui-doi", fade=(0.22, 0.35, 0.06, 0.18))
# Đống củ có lá (mặt sau)
cut("tui-500g-mat-sau.jpg", (815, 700, 1385, 1165), "dong-cu", fade=(0.12, 0.12, 0, 0.08))
# Lá trang trí 4 góc (tách khỏi nền kem)
cut("tui-500g-mat-truoc.jpg", (0, 0, 330, 540), "la-goc-trai", key=True)
cut("tui-500g-mat-truoc.jpg", (0, 0, 330, 540), "la-goc-phai", key=True, flip=True)
cut("tui-500g-mat-sau.jpg", (0, 1600, 330, 2000), "la-duoi-trai", key=True)
cut("tui-500g-mat-sau.jpg", (1060, 1600, 1385, 2000), "la-duoi-phai", key=True)
