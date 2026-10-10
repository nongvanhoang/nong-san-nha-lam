#!/usr/bin/env python3
"""Dong thuong hieu 1 anh that: dai chu chu thich o duoi (giong dung phong cach video da
dung trong make_process_video.py - Cambria Bold, chu trang, nen den mo) + logo tron o goc
tren phai. Dung khi can bo anh dong bo cho 1 kenh (vd gian hang Shopee/TikTok Shop) ma
khong co Canva.

Chay: python make_branded_photo.py <anh_goc.jpg> "<chu thich>" <anh_ra.jpg>
"""
import subprocess
import sys
import tempfile
from pathlib import Path

FONT_BOLD = "C:/Windows/Fonts/cambriab.ttf"
LOGO = Path(__file__).resolve().parent.parent.parent / "docs" / "assets" / "icon-512.png"
TARGET_WIDTH = 1080
CAPTION_BAND_HEIGHT = 260
LOGO_SIZE = 96
LOGO_MARGIN = 24


def esc_filter_path(p):
    """Escape cho dung BEN TRONG filtergraph (-filter_complex, textfile=/fontfile=)."""
    return str(p).replace("\\", "/").replace(":", "\\:")


def make_branded_photo(src: Path, caption: str, out: Path):
    if not src.exists():
        raise SystemExit(f"Khong tim thay anh goc: {src}")
    if not LOGO.exists():
        raise SystemExit(f"Khong tim thay logo: {LOGO}")

    with tempfile.TemporaryDirectory() as tmp:
        # dung textfile= + expansion=none - BAT BUOC, vi chu thich co the chua ky tu "%"
        # (vd "100% Say Tu Nhien") va drawtext mac dinh bat cu phap mo rong %{...}, lam
        # CA DONG CHU BIEN MAT IM LANG (exit code van 0) neu khong tat expansion.
        cap_file = Path(tmp) / "caption.txt"
        cap_file.write_text(caption, encoding="utf-8")

        filter_complex = (
            f"[0:v]scale={TARGET_WIDTH}:-2[scaled];"
            f"[scaled]drawbox=x=0:y=ih-{CAPTION_BAND_HEIGHT}:w=iw:h={CAPTION_BAND_HEIGHT}:"
            f"color=black@0.55:t=fill[boxed];"
            f"[boxed]drawtext=fontfile='{esc_filter_path(FONT_BOLD)}':expansion=none:"
            f"textfile='{esc_filter_path(cap_file)}':fontcolor=white:fontsize=44:"
            f"line_spacing=8:x=(w-text_w)/2:y=h-{CAPTION_BAND_HEIGHT - 70}[texted];"
            f"[1:v]scale={LOGO_SIZE}:{LOGO_SIZE}[logo];"
            f"[texted][logo]overlay=W-w-{LOGO_MARGIN}:{LOGO_MARGIN}[out]"
        )

        out.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            "ffmpeg", "-y",
            "-i", str(src),
            "-i", str(LOGO),
            "-filter_complex", filter_complex,
            "-map", "[out]",
            "-q:v", "3",
            str(out),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if result.returncode != 0:
            print("ffmpeg failed:", result.stderr[-3000:], file=sys.stderr)
            sys.exit(1)
    print(f"Da tao: {out}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Dung: python make_branded_photo.py <anh_goc.jpg> "<chu thich>" <anh_ra.jpg>')
        sys.exit(1)
    make_branded_photo(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]))
