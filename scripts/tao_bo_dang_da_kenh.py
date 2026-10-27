#!/usr/bin/env python3
"""Tạo bộ đăng bài đa kênh (Facebook, Zalo, Instagram, TikTok, YouTube Shorts, LinkedIn) cho
Thế Hưng Organic từ danh sách POSTS bên dưới — sửa chữ ở ĐÂY rồi chạy lại, không sửa file đầu ra.

Mỗi bài ra 1 thư mục content/dang_da_kenh/<dot>/NN_slug/ gồm:
  video.mp4    — chép từ content/video/output/ (video dọc 1080x1920, dùng chung mọi kênh)
  anh-bia.jpg  — ảnh bìa cắt từ video (cho YouTube/Instagram nếu cần chọn ảnh bìa)
  noi-dung.txt — chữ đăng cho từng kênh, link đã gắn mã nguồn để GoatCounter biết khách đến từ đâu
và 1 trang content/dang_da_kenh/<dot>/index.html mở trên máy để xem video + bấm chép chữ.

Ngoài ra chép chữ vào content/posts_ready.md (giữa 2 dòng đánh dấu) và chèn bài vào
data/social_queue.json để lịch nhắc đăng bài (scripts/next_social_post.py) nhắc đúng bài mới.

Chạy: C:/Users/Admin/AppData/Local/Python/bin/python.exe scripts/tao_bo_dang_da_kenh.py
"""
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
VIDEO_DIR = ROOT / "content" / "video" / "output"
DOT = "dot-1_2026-10"
OUT = ROOT / "content" / "dang_da_kenh" / DOT
POSTS_MD = ROOT / "content" / "posts_ready.md"
QUEUE = ROOT / "data" / "social_queue.json"
QUEUE_AT = 12  # chèn ngay sau mục đã nhắc gần nhất (next_index lúc soạn = 12)
SITE = "https://thehungorganic.com/"
ZALO = "0979 502 000"

TAG_SD = "#tinhbotsanday #sanday #sandaylangson #thehungorganic"
TAG_CAM = "#camduongcanh #camlangson #VietGAP #thehungorganic"

# Thứ tự kênh trong file chữ + trang xem trước. "src" là mã nguồn gắn vào link (utm_source).
CHANNELS = [
    ("fb", "Facebook", "facebook"),
    ("zalo", "Zalo", "zalo"),
    ("ig", "Instagram", None),
    ("tiktok", "TikTok", None),
    ("yt", "YouTube Shorts", "youtube"),
    ("li", "LinkedIn", "linkedin"),
]
BIO_NOTE = "(Instagram/TikTok không bấm được link trong bài: để link thehungorganic.com ở phần tiểu sử trang)"

POSTS = [
    {
        "slug": "website-moi", "ngay": "Thứ 4 29/10", "ten": "Ra mắt website mới thehungorganic.com",
        "video": "gioi-thieu-thoc-doc", "link": "", "tags": TAG_SD,
        "fb": (
            "Hợp tác xã Thế Hưng Organic có website mới: thehungorganic.com 🌿\n\n"
            "Trên web, cả nhà xem được tận mắt từng bước làm ra Tinh Bột Sắn Dây: từ nương sắn dây ở Vũ Lăng, "
            "đào củ, rửa, nghiền lọc, đến lò sấy và đóng túi. Vườn Cam Đường Canh VietGAP cũng có ảnh thật từ "
            "lúc ra hoa đến lúc hái.\n\n"
            "✅ Xem giá, đặt hàng ngay trên web, giao toàn quốc\n"
            "✅ Cách pha, cách nấu sắn dây không vón cục\n"
            "✅ Đặt trước Cam Đường Canh mùa này\n\n"
            "👉 {link}\n📞 Zalo {zalo}"
        ),
        "zalo": "Nhà mình vừa có website mới, có đủ ảnh thật quy trình làm sắn dây và vườn cam. Anh chị ghé xem, đặt hàng ngay trên web cũng được ạ: {link}",
        "ig": "Website mới của Thế Hưng Organic đã lên 🌿 Từ nương sắn dây Vũ Lăng đến túi tinh bột, từ vườn cam đến thùng cam, xem tận mắt từng bước. Link ở phần tiểu sử.\n\n{tags} #langson #nongsanviet",
        "tiktok": "Nhà mình làm sắn dây và trồng cam ở Lạng Sơn, giờ có website rồi 🌿 Link ở trang cá nhân. {tags}",
        "yt_title": "Hợp tác xã Thế Hưng Organic - Sắn dây & Cam Đường Canh Lạng Sơn #shorts",
        "yt_desc": "Tinh Bột Sắn Dây và Cam Đường Canh VietGAP từ Vũ Lăng, Lạng Sơn.\nWebsite: {link}\nZalo: {zalo}",
    },
    {
        "slug": "cach-pha", "ngay": "Thứ 6 31/10", "ten": "Mẹo pha sắn dây không vón cục",
        "video": "san-day-cach-pha", "link": "cach-dung-tinh-bot-san-day.html", "tags": TAG_SD,
        "fb": (
            "Pha sắn dây bị vón cục? Gần như luôn do đổ nước sôi thẳng vào bột 😅\n\n"
            "Cách đúng nhà mình vẫn làm:\n"
            "1️⃣ Cho 1–2 thìa canh bột (15–20g) vào cốc\n"
            "2️⃣ Rót NƯỚC LẠNH vào trước, khuấy cho tan hết\n"
            "3️⃣ Rồi mới rót nước sôi, vừa rót vừa khuấy đến khi bột chuyển từ đục sang trong\n\n"
            "Thêm chút đường hoặc mật ong tuỳ khẩu vị. Hướng dẫn đầy đủ: {link}\n\n"
            "Tinh Bột Sắn Dây Thế Hưng Organic: túi 0,5kg 80.000đ, túi 1kg 155.000đ. Nhắn Zalo {zalo} là giao ngay."
        ),
        "zalo": "Mẹo nhỏ pha sắn dây không vón: hoà bột với nước lạnh trước, tan hết rồi mới rót nước sôi. Anh chị xem video và cách làm đầy đủ ở đây ạ: {link}",
        "ig": "Mẹo pha sắn dây không vón cục ✨ Nước lạnh trước, nước sôi sau. Cho bột vào cốc → rót nước lạnh, khuấy tan → rót nước sôi, khuấy tới khi trong. Cách làm đầy đủ ở link phần tiểu sử.\n\n{tags} #meovat #doanhealthy",
        "tiktok": "Pha sắn dây mà vón cục là do làm ngược bước này 👀 Nước lạnh trước, nước sôi sau! {tags} #meovat",
        "yt_title": "Mẹo pha tinh bột sắn dây không vón cục #shorts",
        "yt_desc": "Hoà bột với nước lạnh trước, tan hết rồi mới rót nước sôi.\nCách làm đầy đủ: {link}\nĐặt hàng Zalo: {zalo}",
    },
    {
        "slug": "hoa-san-day", "ngay": "Chủ nhật 02/11", "ten": "Hoa sắn dây màu tím trên nương",
        "video": "san-day-hoa-tim", "link": "san-day.html", "tags": TAG_SD,
        "fb": (
            "Nhiều người dùng sắn dây cả chục năm mà chưa từng thấy hoa của nó 💜\n\n"
            "Đây là hoa sắn dây trên nương nhà mình ở Vũ Lăng, Lạng Sơn: mọc thành chùm tím, giữa cánh có đốm vàng. "
            "Dưới lớp lá xanh này là củ sắn dây, nguyên liệu để nhà mình làm ra Tinh Bột Sắn Dây.\n\n"
            "Xem cả hành trình từ nương đến túi bột: {link}"
        ),
        "zalo": "Gửi anh chị mấy hình hoa sắn dây trên nương nhà mình, tím đẹp lắm ạ 💜 Cả quy trình từ nương đến túi bột ở đây: {link}",
        "ig": "Hoa sắn dây 💜 Mọc thành chùm tím trên nương nhà mình ở Vũ Lăng, Lạng Sơn. Dưới lớp lá này là củ làm ra tinh bột.\n\n{tags} #hoasanday #langson #vietnamcountryside",
        "tiktok": "Bạn đã bao giờ thấy hoa sắn dây chưa? 💜 Nương nhà mình ở Lạng Sơn {tags} #hoasanday",
        "yt_title": "Hoa sắn dây màu tím - ít ai từng thấy #shorts",
        "yt_desc": "Nương sắn dây của Hợp tác xã Thế Hưng Organic, Vũ Lăng, Lạng Sơn.\n{link}",
    },
    {
        "slug": "lo-say", "ngay": "Thứ 3 04/11", "ten": "Bên trong lò sấy tinh bột sắn dây",
        "video": "quy-trinh-say-san-day", "link": "san-day.html", "tags": TAG_SD,
        "fb": (
            "Vì sao nhà mình chuyển sang sấy bằng lò thay vì phơi nắng?\n\n"
            "Phơi ngoài trời thì phụ thuộc thời tiết, dễ dính bụi. Lò sấy chuyên dụng giữ nhiệt đều, bột khô đều từng khay, "
            "sạch hơn và không phải chờ nắng.\n\n"
            "Không hoá chất, không chất tẩy trắng. Màu trắng là màu tự nhiên của bột đã lọc kỹ.\n\n"
            "👉 Xem và đặt hàng: {link}\n📞 Zalo {zalo}"
        ),
        "zalo": "Nhà mình sấy tinh bột sắn dây bằng lò sấy chuyên dụng, khô đều, sạch, không phụ thuộc nắng mưa. Anh chị xem video và đặt hàng ở đây ạ: {link}",
        "ig": "Bên trong lò sấy 🔥 Từng khay tinh bột sắn dây sấy khô đều, không phụ thuộc nắng mưa, không hoá chất tẩy trắng. Link ở phần tiểu sử.\n\n{tags} #behindthescenes",
        "tiktok": "Bên trong lò sấy tinh bột sắn dây nhà mình 🔥 {tags} #quytrinh",
        "yt_title": "Bên trong lò sấy tinh bột sắn dây #shorts",
        "yt_desc": "Tinh bột sắn dây sấy bằng lò sấy chuyên dụng, không hoá chất tẩy trắng.\n{link}\nZalo: {zalo}",
    },
    {
        "slug": "cach-nau", "ngay": "Thứ 6 07/11", "ten": "Nấu sắn dây sánh trong cho cả nhà",
        "video": "san-day-cach-nau", "link": "cach-nau-che-san-day.html", "tags": TAG_SD,
        "fb": (
            "Trời bắt đầu lạnh, nhiều nhà chuyển sang nấu sắn dây chín hẳn thay vì pha nước 🍲\n\n"
            "Cách nấu:\n"
            "1️⃣ Hoà bột với nước lạnh cho tan hết\n"
            "2️⃣ Đổ vào nồi, để lửa nhỏ, khuấy liên tục\n"
            "3️⃣ Bột chuyển trong và sánh lại là chín, tắt bếp\n\n"
            "Ăn nóng hay để nguội đều ngon. Thêm đường phèn nấu thành chè cũng được. Công thức chè sắn dây: {link}\n\n"
            "📞 Đặt Tinh Bột Sắn Dây: Zalo {zalo}"
        ),
        "zalo": "Trời lạnh rồi, anh chị thử nấu sắn dây chín cho cả nhà nhé: hoà nước lạnh, lửa nhỏ, khuấy tới khi trong sánh. Công thức ở đây ạ: {link}",
        "ig": "Sắn dây nấu chín, sánh trong 🍲 Hoà nước lạnh → lửa nhỏ, khuấy đều → chuyển trong là chín. Công thức ở link phần tiểu sử.\n\n{tags} #monngon #chesanday",
        "tiktok": "Nấu sắn dây sánh trong, không vón 🍲 {tags} #chesanday #monngonmoingay",
        "yt_title": "Cách nấu tinh bột sắn dây sánh trong #shorts",
        "yt_desc": "Hoà nước lạnh, lửa nhỏ, khuấy đều đến khi trong sánh.\nCông thức: {link}\nZalo: {zalo}",
    },
    {
        "slug": "cam-hai-tai-vuon", "ngay": "Thứ 3 11/11", "ten": "Cam Đường Canh hái tại vườn: mở đặt trước",
        "video": "cam-hai-tai-vuon", "link": "dat-truoc.html?chon=cam10", "tags": TAG_CAM,
        "fb": (
            "Cam Đường Canh nhà mình: chín trên cây mới hái, không thúc chín 🍊\n\n"
            "Vườn cam của Hợp tác xã Thế Hưng Organic nằm dưới chân núi đá Vũ Lăng, Lạng Sơn, trồng theo tiêu chuẩn VietGAP. "
            "Cam hái từng quả, giữ cả cuống lá, xếp ngay vào thùng.\n\n"
            "Mùa cam khoảng tháng 11 âm lịch đến tháng 1 năm sau. Nhà mình đang nhận đặt trước:\n"
            "🍊 Thùng 5kg: 275.000đ\n🍊 Thùng 10kg: 500.000đ\n\n"
            "👉 Đặt trước: {link}\n📞 Zalo {zalo}"
        ),
        "zalo": "Mùa Cam Đường Canh sắp tới rồi ạ 🍊 Nhà mình nhận đặt trước thùng 5kg (275k) và 10kg (500k), chín cây mới hái. Anh chị đặt giữ hàng ở đây: {link}",
        "ig": "Cam Đường Canh chín cây mới hái 🍊 Vườn VietGAP dưới chân núi đá Vũ Lăng, Lạng Sơn. Đang nhận đặt trước thùng 5kg / 10kg, link ở phần tiểu sử.\n\n{tags} #mandarin #vietnamfruit",
        "tiktok": "Hái Cam Đường Canh ngay tại vườn 🍊 Chín cây mới hái, không thúc chín. {tags} #camtet",
        "yt_title": "Hái Cam Đường Canh tại vườn Lạng Sơn #shorts",
        "yt_desc": "Cam Đường Canh VietGAP, chín cây mới hái. Đặt trước thùng 5kg/10kg: {link}\nZalo: {zalo}",
    },
    {
        "slug": "hanh-trinh", "ngay": "Thứ 6 14/11", "ten": "Hành trình từ củ sắn dây tươi đến túi tinh bột",
        "video": "san-day-hanh-trinh-day-du", "link": "san-day.html", "tags": TAG_SD,
        "fb": (
            "Một túi Tinh Bột Sắn Dây đi qua những bước nào? 🌿\n\n"
            "Đào củ trên nương → rửa sạch đất → nghiền và lọc lấy tinh bột → để lắng, thay nước nhiều lần → "
            "sấy khô trong lò → đóng túi.\n\n"
            "Video này là cảnh thật ở nhà mình, không dựng cảnh. Không hoá chất, không chất tẩy trắng.\n\n"
            "👉 {link}\n📞 Zalo {zalo}"
        ),
        "zalo": "Anh chị xem trọn hành trình làm Tinh Bột Sắn Dây nhà mình, từ củ tươi đến túi bột ạ: {link}",
        "ig": "Từ củ sắn dây tươi đến túi tinh bột 🌿 Đào củ → rửa → nghiền lọc → lắng → sấy → đóng túi. Cảnh thật ở nhà mình. Link ở phần tiểu sử.\n\n{tags} #farmtotable #quytrinh",
        "tiktok": "Từ củ sắn dây đến túi tinh bột, toàn bộ quy trình ở nhà mình 🌿 {tags} #quytrinh #farmlife",
        "yt_title": "Quy trình làm tinh bột sắn dây từ củ tươi #shorts",
        "yt_desc": "Đào củ, rửa, nghiền lọc, lắng, sấy, đóng túi tại Hợp tác xã Thế Hưng Organic, Lạng Sơn.\n{link}\nZalo: {zalo}",
        "li": (
            "From fresh kudzu root to finished starch: every step at our cooperative in Lang Son, Vietnam.\n\n"
            "Harvest → wash → grind and filter → settle → kiln-dry → pack. No chemicals, no bleaching agents.\n\n"
            "We supply kudzu root starch for wholesale and export (minimum 100 kg). Specs and samples: {link_en}"
        ),
    },
    {
        "slug": "dong-goi-cam", "ngay": "Thứ 3 18/11", "ten": "Đóng gói Cam Đường Canh cẩn thận từng thùng",
        "video": "cam-dong-goi-can-than", "link": "dat-truoc.html?chon=cam10", "tags": TAG_CAM,
        "fb": (
            "Cam ngon mà đến tay khách bị dập thì cũng hỏng cả 😔 Nên khâu đóng gói nhà mình làm rất kỹ.\n\n"
            "Cam hái về phân loại, đóng thùng ngay trong ngày, từng quả xếp cẩn thận. "
            "Lỡ có quả dập khi nhận, anh chị quay lại lúc mở thùng và báo trong 24 giờ, nhà mình gửi bù hoặc hoàn tiền phần hư.\n\n"
            "🍊 Thùng 5kg: 275.000đ · Thùng 10kg: 500.000đ\n👉 Đặt trước: {link}\n📞 Zalo {zalo}"
        ),
        "zalo": "Cam nhà mình đóng thùng ngay trong ngày hái, xếp kỹ từng quả để đi xa không dập ạ 🍊 Đặt trước: {link}",
        "ig": "Đóng gói cẩn thận từng thùng cam 🍊 Hái về là phân loại, đóng thùng trong ngày. Đặt trước ở link phần tiểu sử.\n\n{tags}",
        "tiktok": "Đóng thùng Cam Đường Canh sao cho đi xa không dập 🍊 {tags} #donggoi",
        "yt_title": "Đóng gói Cam Đường Canh từng thùng #shorts",
        "yt_desc": "Cam Đường Canh VietGAP, đóng thùng 5kg/10kg trong ngày hái.\nĐặt trước: {link}\nZalo: {zalo}",
    },
    {
        "slug": "ban-si-xuat-khau", "ngay": "Thứ 6 21/11", "ten": "Nhận bán sỉ và xuất khẩu Tinh Bột Sắn Dây",
        "video": "san-day-gioi-thieu-xuat-khau", "link": "mua-si-san-day.html", "tags": TAG_SD,
        "fb": (
            "Quán chè, tiệm bánh, cửa hàng đặc sản cần nguồn Tinh Bột Sắn Dây ổn định? 🤝\n\n"
            "Hợp tác xã Thế Hưng Organic làm khoảng 10–20 tấn bột mỗi tháng, có túi 5kg và 10kg cho khách sỉ, "
            "giá theo số lượng. Khách nước ngoài nhận từ 100kg.\n\n"
            "👉 Thông tin sỉ: {link}\n📞 Zalo {zalo} · ✉️ hello@thehungorganic.com"
        ),
        "zalo": "Nhà mình nhận bán sỉ Tinh Bột Sắn Dây cho quán chè, tiệm bánh, cửa hàng đặc sản: túi 5kg/10kg, giá theo số lượng. Anh chị cần thì nhắn em báo giá ạ: {link}",
        "ig": "We supply kudzu root starch for wholesale and export 🌿 Made at our cooperative in Lang Son, Vietnam. No chemicals, no bleaching. Minimum 100 kg for export. Link in bio.\n\nNhận bán sỉ Tinh Bột Sắn Dây, túi 5kg/10kg.\n\n#kudzu #kudzustarch #vietnamexport #thehungorganic #tinhbotsanday",
        "tiktok": "Nhận bán sỉ & xuất khẩu tinh bột sắn dây Lạng Sơn 🌿 {tags} #bansi",
        "yt_title": "Kudzu root starch from Vietnam - wholesale & export #shorts",
        "yt_desc": "The Hung Organic Cooperative, Lang Son, Vietnam. Kudzu root starch, minimum 100 kg for export.\nSpecs & samples: {link_en}\nBán sỉ trong nước: {link}",
        "li": (
            "Looking for a reliable source of kudzu root starch?\n\n"
            "The Hung Organic Cooperative in Lang Son, Vietnam produces around 10–20 tonnes a month. "
            "Washed, ground, filtered and kiln-dried at our own facility. No chemicals, no bleaching agents.\n\n"
            "Export minimum order: 100 kg. Spec sheet and sample request: {link_en}\n"
            "Contact: hello@thehungorganic.com · WhatsApp +84 363 589 920"
        ),
        "link_en": "en/wholesale.html",
    },
]


def make_link(path, src, slug):
    if src is None:
        return SITE
    sep = "&" if "?" in path else "?"
    return f"{SITE}{path}{sep}utm_source={src}&utm_medium=social&utm_campaign={slug}"


def channel_text(p, key, src):
    if key == "yt":
        if "yt_title" not in p:
            return None
        body = p["yt_title"] + "\n\n" + p["yt_desc"]
    else:
        body = p.get(key)
        if body is None:
            return None
    link_en = make_link(p.get("link_en", "en/wholesale.html"), src or "instagram", p["slug"])
    return body.format(link=make_link(p["link"], src, p["slug"]), link_en=link_en,
                       zalo=ZALO, tags=p["tags"])


def cover(video, dest):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2", "-i", str(video),
                    "-frames:v", "1", "-q:v", "3", str(dest)], check=True)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    cards, md_blocks = [], []
    for i, p in enumerate(POSTS, 1):
        folder = OUT / f"{i:02d}_{p['slug']}"
        folder.mkdir(exist_ok=True)
        src_video = VIDEO_DIR / f"{p['video']}.mp4"
        if not src_video.exists():
            sys.exit(f"Thiếu video {src_video} — dựng bằng content/video/make_process_video.py trước.")
        dst = folder / "video.mp4"
        if not dst.exists() or dst.stat().st_mtime < src_video.stat().st_mtime:
            shutil.copy2(src_video, dst)
        cover(dst, folder / "anh-bia.jpg")

        texts = [(label, channel_text(p, key, src)) for key, label, src in CHANNELS]
        texts = [(label, t) for label, t in texts if t]
        rel = f"content/dang_da_kenh/{DOT}/{folder.name}/video.mp4"
        lines = [f"{p['ten']}", f"Ngày đăng gợi ý: {p['ngay']}", f"Video: {rel}", BIO_NOTE, ""]
        for label, t in texts:
            lines += [f"===== {label} =====", t, ""]
        (folder / "noi-dung.txt").write_text("\n".join(lines), encoding="utf-8")

        for label, t in texts:
            md_blocks.append(f"## {label} — {p['ten']} (đa kênh {DOT})\n\n_Video: `{rel}`_\n\n{t}\n\n---\n")
        cards.append((i, p, folder.name, texts))

    write_index(cards)
    write_posts_md(md_blocks)
    write_queue()
    print(f"Xong {len(POSTS)} bài → {OUT}")


def write_index(cards):
    parts = []
    for i, p, folder, texts in cards:
        boxes = "".join(
            f'<div class="ch"><div class="chh"><b>{html.escape(l)}</b><button onclick="cp(this)">Chép</button></div>'
            f'<textarea readonly rows="{min(18, t.count(chr(10)) + 3)}">{html.escape(t)}</textarea></div>' for l, t in texts)
        parts.append(
            f'<section><div class="v"><video src="{folder}/video.mp4" poster="{folder}/anh-bia.jpg" controls preload="none"></video></div>'
            f'<div class="t"><p class="d">Bài {i} · {html.escape(p["ngay"])}</p><h2>{html.escape(p["ten"])}</h2>'
            f'<label class="done"><input type="checkbox" data-k="{p["slug"]}"> Đã đăng xong</label>{boxes}</div></section>')
    page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bộ đăng đa kênh {DOT}</title><style>
body{{margin:0;background:#f6f3ec;color:#22301f;font:16px/1.5 system-ui,sans-serif}}main{{max-width:1100px;margin:auto;padding:16px}}
h1{{font-family:Cambria,Georgia,serif;margin:.4em 0;overflow-wrap:anywhere}}.note{{background:#fff;border-left:4px solid #c9a227;padding:10px 14px;border-radius:6px}}
section{{display:grid;grid-template-columns:260px 1fr;gap:20px;background:#fff;border-radius:12px;padding:16px;margin:18px 0;box-shadow:0 1px 3px #0001}}
video{{width:100%;border-radius:8px;background:#000;aspect-ratio:9/16}}h2{{margin:.1em 0 .4em;font-family:Cambria,Georgia,serif}}.d{{margin:0;color:#7a6a3a;font-weight:600}}
.ch{{margin:10px 0}}.chh{{display:flex;justify-content:space-between;align-items:center}}textarea{{width:100%;box-sizing:border-box;font:14px/1.45 system-ui;border:1px solid #ddd;border-radius:6px;padding:8px}}
button{{background:#2f5d34;color:#fff;border:0;border-radius:6px;padding:5px 14px;cursor:pointer}}.done{{display:inline-block;margin:4px 0;font-weight:600}}
@media(max-width:700px){{section{{grid-template-columns:minmax(0,1fr);padding:12px}}.v{{max-width:260px}}}}</style></head><body><main>
<h1>Bộ đăng đa kênh: {len(cards)} bài ({DOT})</h1>
<p class="note">Mỗi bài: tải <b>video.mp4</b> trong thư mục bài lên mọi kênh (cùng 1 file), rồi bấm <b>Chép</b> chữ của kênh đó dán vào.
Instagram và TikTok không bấm được link trong bài, nên để link <b>thehungorganic.com</b> ở phần tiểu sử trang. Link trong chữ Facebook/Zalo/YouTube đã gắn mã nguồn để GoatCounter biết khách đến từ kênh nào.</p>
{''.join(parts)}</main><script>
function cp(b){{var t=b.parentNode.nextElementSibling;t.select();navigator.clipboard?navigator.clipboard.writeText(t.value):document.execCommand('copy');b.textContent='Đã chép';setTimeout(function(){{b.textContent='Chép'}},1500)}}
document.querySelectorAll('[data-k]').forEach(function(c){{try{{c.checked=localStorage.getItem('dk-'+c.dataset.k)==='1'}}catch(e){{}}
c.onchange=function(){{try{{localStorage.setItem('dk-'+c.dataset.k,c.checked?'1':'0')}}catch(e){{}}}}}});
</script></body></html>"""
    (OUT / "index.html").write_text(page, encoding="utf-8")


def write_posts_md(blocks):
    start, end = f"<!-- BAT DAU {DOT} -->", f"<!-- HET {DOT} -->"
    text = POSTS_MD.read_text(encoding="utf-8")
    new = f"{start}\n\n" + "\n".join(blocks) + f"\n{end}"
    if start in text:
        a, b = text.index(start), text.index(end) + len(end)
        text = text[:a] + new + text[b:]
    else:
        text = text.rstrip() + "\n\n" + new + "\n"
    POSTS_MD.write_text(text, encoding="utf-8")


def write_queue():
    q = json.loads(QUEUE.read_text(encoding="utf-8"))
    have = {it["topic_keyword"] for it in q["items"]}
    add = [{"topic_keyword": f"{p['ten']} (đa kênh {DOT})",
            "channels": [label for key, label, src in CHANNELS if channel_text(p, key, src)]}
           for p in POSTS]
    add = [it for it in add if it["topic_keyword"] not in have]
    if add:
        # Bài mới thế chỗ các bài cũ ngay sau con trỏ; bài cũ dời xuống cuối hàng đợi để các bài
        # Quà Tết phía sau gần như giữ nguyên ngày nhắc.
        items = q["items"]
        moved = items[QUEUE_AT:QUEUE_AT + len(add) - 1]
        q["items"] = items[:QUEUE_AT] + add + items[QUEUE_AT + len(moved):] + moved
        QUEUE.write_text(json.dumps(q, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
