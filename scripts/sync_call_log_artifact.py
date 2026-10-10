"""
Dong bo DANH_SACH_KHACH_HANG_B2B.csv vao ban HTML cua "So Goi Khach" (artifact
hien co tren claude.ai). Lam 2 viec:
  1. Dien email moi tim duoc cho lead da co san trong artifact (khop theo ten,
     chi dien khi o trong).
  2. Them lead MOI trong CSV nhung chua co trong artifact (khop theo ten) -
     tu suy ra nhom (g) tu cot Nhom, va tier (t) bang cach lay tier PHO BIEN
     NHAT dang dung cho nhom do trong artifact hien tai (nhom hoan toan moi
     thi dung tier lon nhat + 1). Khong dong Trang_thai/ghi chu goi dien -
     phan do van bao qua chat de Claude cap nhat rieng vao CSV.
Cung tu cap nhat lai dong "X moi lien he" trong <p class="sub"> cho khop tong
so lead moi, khoi phai sua tay.

Cach dung (van can Claude lam ho 2 dau vi script khong tu goi duoc claude.ai):
  1. Nho Claude "doc" artifact So Goi Khach hien tai (action: read) - Claude se
     luu ban HTML dang xem duoc ra 1 file local (duong dan bao trong ket qua).
  2. Chay: python sync_call_log_artifact.py <duong_dan_html_vua_luu> [duong_dan_output.html]
     Neu bo qua duong_dan_output, mac dinh ghi de len chinh file input.
  3. Nho Claude publish lai file output do len dung URL artifact cu (action:
     publish, kem url= link goc) de cap nhat tai cho.

Lich su: ban dau (2026-09-08) chi dien email cho lead co san. Mo rong them
kha nang them lead moi + tu cap nhat dong dem (2026-09-20) sau khi phai viet
tay 1 script rieng de them 5 lead Nhat Ban - lan sau dung script nay la du.
"""
import json
import re
import csv
import sys
from collections import Counter
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "DANH_SACH_KHACH_HANG_B2B.csv"
LEADS_LINE_PATTERN = re.compile(r"const LEADS = (\[.*\]);")
SUB_COUNT_PATTERN = re.compile(r"(\d+) mối liên hệ")


def sync(input_html: Path, output_html: Path):
    text = input_html.read_text(encoding="utf-8")

    m = LEADS_LINE_PATTERN.search(text)
    if m is None:
        raise SystemExit("Khong tim thay dong 'const LEADS = [...]' trong file HTML - co the cau truc artifact da doi, kiem tra lai thu cong.")
    leads = json.loads(m.group(1))

    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    leads_by_name = {l["n"].strip(): l for l in leads}

    # tier pho bien nhat dang dung cho tung nhom (g), de suy ra tier cho lead nhom da biet
    tier_votes = {}
    for l in leads:
        tier_votes.setdefault(l["g"], Counter())[l["t"]] += 1
    tier_by_group = {g: counter.most_common(1)[0][0] for g, counter in tier_votes.items()}
    max_tier = max((l["t"] for l in leads), default=-1)

    filled = 0
    added = 0
    for row in rows:
        name = row.get("Ten", "").strip()
        if not name:
            continue
        nhom_raw = row.get("Nhom", "").strip()
        g = nhom_raw.split(" - ", 1)[0].strip() or "?"

        existing = leads_by_name.get(name)
        csv_email = row.get("Email", "").strip()

        if existing is not None:
            if csv_email and not existing.get("e"):
                existing["e"] = csv_email
                filled += 1
            continue

        # lead moi, chua co trong artifact - them vao
        if g not in tier_by_group:
            max_tier += 1
            tier_by_group[g] = max_tier
        new_lead = {
            "g": g,
            "n": name,
            "k": row.get("Khu_vuc", "").strip(),
            "p": row.get("SDT", "").strip(),
            "e": csv_email,
            "note": row.get("Ghi_chu", "").strip(),
            "sn": False,
            "t": tier_by_group[g],
        }
        leads.append(new_lead)
        leads_by_name[name] = new_lead
        added += 1

    new_array_json = json.dumps(leads, ensure_ascii=False, separators=(",", ":"))
    text = text[: m.start(1)] + new_array_json + text[m.end(1) :]
    text = SUB_COUNT_PATTERN.sub(f"{len(leads)} mối liên hệ", text)

    output_html.write_text(text, encoding="utf-8")

    total_with_email = sum(1 for l in leads if l.get("e"))
    print(f"Tong leads sau dong bo: {len(leads)}")
    print(f"Email dien moi lan nay: {filled}")
    print(f"Lead moi them vao: {added}")
    print(f"Tong co email sau dong bo: {total_with_email}")
    print(f"Da ghi ra: {output_html}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Dung: python sync_call_log_artifact.py <input.html> [output.html]")
        sys.exit(1)
    inp = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else inp
    sync(inp, out)
