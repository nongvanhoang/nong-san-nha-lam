"""Chuyển website từ nongsannhalam.com sang tên miền mới (thehungorganic.com).

Chạy thử (chỉ đếm, không sửa):  python scripts/doi_ten_mien.py
Chạy thật:                       python scripts/doi_ten_mien.py --lam-that

Chỉ đổi ĐỊA CHỈ WEB (link, canonical, og:image, sitemap, chữ "nongsannhalam.com" hiện trên trang).
GIỮ NGUYÊN email hello@nongsannhalam.com cho tới khi hộp thư ở tên miền mới đã nhận được thư thật.
Chỉ chạy thật SAU KHI tên miền mới đã trỏ về GitHub Pages (xem bước trong VIEC_CAN_LAM.md),
nếu không web sẽ không vào được.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
OLD, NEW = "nongsannhalam.com", "thehungorganic.com"
# không đụng tới địa chỉ email @nongsannhalam.com
PAT = re.compile(r"(?<![@\w.-])" + re.escape(OLD))

FILES = [p for p in (ROOT / "docs").rglob("*") if p.suffix in {".html", ".xml", ".txt", ".js", ".json", ".webmanifest"}]
FILES += [ROOT / "docs" / "CNAME", ROOT / "scripts" / "tao_trang_noi_dung.py", ROOT / "content" / "kenh_assets" / "banner" / "make_banners.py",
          ROOT / "scripts" / "tao_bao_bi.js"]


def main():
    global PAT
    do_it = "--lam-that" in sys.argv
    # --email: chỉ đổi hello@nongsannhalam.com -> hello@thehungorganic.com (chạy khi hộp thư mới đã nhận thư thật)
    if "--email" in sys.argv:
        PAT = re.compile(r"(?<=@)" + re.escape(OLD))
        FILES.extend(p for p in ROOT.rglob("*.md") if "node_modules" not in p.parts)
    total = 0
    for p in FILES:
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        n = len(PAT.findall(s))
        if not n:
            continue
        total += n
        print(f"{n:4d}  {p.relative_to(ROOT)}")
        if do_it:
            p.write_text(PAT.sub(NEW, s), encoding="utf-8")
    print(("ĐÃ ĐỔI" if do_it else "Sẽ đổi"), total, "chỗ")


if __name__ == "__main__":
    main()
