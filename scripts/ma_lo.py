"""Mã lô + QR truy xuất cho Tinh Bột Sắn Dây / Cam Đường Canh.

Chạy bằng C:/Users/Admin/AppData/Local/Python/bin/python.exe scripts/ma_lo.py <lệnh>

  xuat              Ghi docs/lo/lots.json từ data/production_log.csv (trang tra cứu thehungorganic.com/lo/ đọc file này).
                    Chỉ đưa lên web: mã lô, sản phẩm, ngày làm, hạn dùng — KHÔNG đưa số lượng/ghi chú (thông tin kinh doanh).
  tem <MÃ LÔ>       Tạo tờ tem dán A4 (4 x 9 tem 50 x 30 mm) cho 1 lô: content/tem_lo/<MÃ LÔ>.html + .pdf
                    Mỗi tem có QR dẫn tới thehungorganic.com/lo/?ma=<MÃ LÔ>, số lô, NSX, HSD. Tự chạy "xuat" trước.
  qr-bao-bi         Tạo content/nhan_bao_bi/qr-tra-cuu-lo.svg (QR cố định in trên bao bì → trang tra cứu lô).

Ghi mẻ mới bằng app quản lý / scripts/add_batch.py như cũ: mã lô tự đặt dạng SD-261027-01.
Sau khi "xuat" phải đẩy docs/lo/lots.json lên GitHub thì trang tra cứu mới thấy lô mới.
"""
import csv
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

import segno

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "data" / "production_log.csv"
LOTS_JSON = ROOT / "docs" / "lo" / "lots.json"
TEM_DIR = ROOT / "content" / "tem_lo"
LOOKUP = "https://thehungorganic.com/lo/"
CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe"
# Chủ shop báo HSD sắn dây "2/3 năm" (2026-10-27) → in mức thấp 24 tháng. Cam là quả tươi: không in HSD.
SHELF_MONTHS = {"SD": 24}


def rel(p):
    try:
        return p.relative_to(ROOT)
    except ValueError:
        return p


def add_months(d, m):
    y, mo = divmod(d.month - 1 + m, 12)
    y += d.year
    mo += 1
    for day in (d.day, 30, 29, 28):
        try:
            return date(y, mo, day)
        except ValueError:
            continue


def load_lots():
    if not LOG.exists():
        return []
    lots = []
    with open(LOG, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            code = (r.get("batch_id") or "").strip()
            try:
                made = datetime.strptime(r["date"], "%Y-%m-%d").date()
            except (KeyError, ValueError):
                continue
            if not code:
                continue
            kind = code.split("-")[0]
            exp = add_months(made, SHELF_MONTHS[kind]) if kind in SHELF_MONTHS else None
            lots.append({"lot": code, "kind": kind, "product": r.get("product", ""),
                         "made": made.isoformat(), "expires": exp.isoformat() if exp else None})
    return lots


def xuat():
    lots = load_lots()
    LOTS_JSON.parent.mkdir(parents=True, exist_ok=True)
    tmp = LOTS_JSON.with_suffix(".tmp")
    tmp.write_text(json.dumps({"updated": date.today().isoformat(), "lots": lots}, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(LOTS_JSON)
    print(f"Đã ghi {len(lots)} lô vào {rel(LOTS_JSON)}")
    return lots


def qr_svg(data, style=""):
    # SVG gọn: nền trắng + 1 path, viền 2 ô (đủ để máy quét đọc trên nền kraft)
    q = segno.make(data, error="m")
    rows = list(q.matrix)
    n = len(rows) + 4
    d = "".join(f"M{x + 2},{y + 2}h1v1h-1z" for y, row in enumerate(rows) for x, v in enumerate(row) if v)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" shape-rendering="crispEdges"{style}><rect width="{n}" height="{n}" fill="#fff"/><path d="{d}" fill="#000"/></svg>'


def qr_bao_bi():
    out = ROOT / "content" / "nhan_bao_bi" / "qr-tra-cuu-lo.svg"
    out.write_text(qr_svg(LOOKUP), encoding="utf-8")
    print("Đã tạo", rel(out), "→", LOOKUP)


def vn(d):
    return datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m/%Y")


def tem(code):
    lots = {l["lot"]: l for l in xuat()}
    if code not in lots:
        sys.exit(f"Không thấy lô {code} trong data/production_log.csv. Ghi mẻ trước (app quản lý hoặc add_batch.py).")
    l = lots[code]
    name = "Tinh Bột Sắn Dây" if l["kind"] == "SD" else ("Cam Đường Canh" if l["kind"] == "CAM" else l["product"])
    qr = qr_svg(f"{LOOKUP}?ma={code}", ' class="qr"')
    made_label = "NSX / MFD" if l["kind"] != "CAM" else "Ngày hái / Picked"
    exp = f'<div><span>HSD / EXP</span><b>{vn(l["expires"])}</b></div>' if l["expires"] else ""
    one = f"""<div class="t">{qr}<div class="i"><div class="p">{name}</div><div><span>Số lô / Lot</span><b>{code}</b></div><div><span>{made_label}</span><b>{vn(l["made"])}</b></div>{exp}<div class="s">Quét xem lô này · Scan for batch info</div></div></div>"""
    html = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Tem lô {code}</title>
<style>
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:"Be Vietnam Pro",Arial,sans-serif;color:#1c2a20}}
.sheet{{width:210mm;height:297mm;padding:13.5mm 5mm;display:grid;grid-template-columns:repeat(4,50mm);grid-auto-rows:30mm}}
.t{{display:flex;align-items:center;gap:2mm;padding:2mm;border:.2mm dashed #bbb}}
.qr{{width:24mm;height:24mm;flex:none}}
.i{{font-size:6.2pt;line-height:1.25;display:grid;gap:.6mm;min-width:0}}
.i span{{display:block;color:#55615a;font-size:5.2pt}}
.i b{{font-size:7.4pt;letter-spacing:.02em}}
.p{{font-weight:700;font-size:6.6pt;color:#173f23}}
.s{{font-size:4.8pt;color:#55615a}}
</style></head><body><div class="sheet">{one * 36}</div></body></html>"""
    TEM_DIR.mkdir(parents=True, exist_ok=True)
    h = TEM_DIR / f"{code}.html"
    h.write_text(html, encoding="utf-8")
    pdf = TEM_DIR / f"{code}.pdf"
    prof = Path.home() / "AppData" / "Local" / "Temp" / "thoc-tem-chrome"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--user-data-dir={prof}", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", h.resolve().as_uri()], check=True, capture_output=True)
    print("Đã tạo tờ tem:", rel(pdf), "(36 tem 50x30mm, in trên giấy decal A4 rồi cắt theo nét đứt)")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "xuat":
        xuat()
    elif cmd == "tem" and len(sys.argv) > 2:
        tem(sys.argv[2].strip().upper())
    elif cmd == "qr-bao-bi":
        qr_bao_bi()
    else:
        print(__doc__)
