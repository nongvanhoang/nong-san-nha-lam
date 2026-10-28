"""Dựng các trang nội dung của thehungorganic.com theo cùng một khung (đầu trang, chân trang, thanh đặt hàng).

Chạy: C:/Users/Admin/AppData/Local/Python/bin/python.exe scripts/tao_trang_noi_dung.py
Ghi đè các file trong docs/ có tên trong PAGES. Muốn sửa chữ một trang: sửa ở đây rồi chạy lại,
đừng sửa tay file HTML (lần chạy sau sẽ ghi đè).
Nguyên tắc nội dung: chỉ viết điều có thật (giá lấy từ data/products.json, chứng nhận VietGAP đúng số giấy),
không nói sắn dây chữa bệnh, không gắn chứng nhận hữu cơ khi chưa thấy giấy.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = "https://thehungorganic.com/"

prods = json.load(open(ROOT / "data" / "products.json", encoding="utf-8"))["products"]
PRICE = {v["package"]: v["price_vnd"] for p in prods for v in p["variants"]}


def vnd(n):
    return f"{n:,}".replace(",", ".") + "đ"


P05, P1 = vnd(PRICE["túi 0.5kg"]), vnd(PRICE["túi 1kg"])
C5, C10 = vnd(PRICE["thùng 5kg"]), vnd(PRICE["thùng 10kg"])
DATE = "2026-10-25"

ARTICLES = [  # (file, tiêu đề ngắn, mô tả 1 câu, ảnh)
    ("phan-biet-bot-san-day-that-gia.html", "Cách phân biệt bột sắn dây thật và bột pha trộn", "5 cách thử ngay tại nhà: nhìn, bóp, ngửi, hoà nước lạnh và pha nước sôi.", "g-sd4-1200.webp"),
    ("bot-san-day-khac-bot-nang.html", "Bột sắn dây khác bột năng thế nào?", "Hai loại bột trắng trông giống nhau nhưng khác củ, khác cách dùng.", "g-sd2-1200.webp"),
    ("cach-nau-che-san-day.html", "Cách nấu chè sắn dây hạt sen và 3 món dễ làm", "Chè sắn dây hạt sen, chè đậu xanh, sắn dây sữa và thạch sắn dây.", "p2-loc-800.webp"),
    ("uong-san-day-dung-cach.html", "Uống sắn dây thế nào cho đúng?", "Pha sống hay nấu chín, uống lượng bao nhiêu, ai nên hỏi bác sĩ trước.", "cta-say-800.webp"),
    ("cach-chon-cam-duong-canh.html", "Cách chọn cam Đường Canh ngon, mọng nước", "Nhìn vỏ, cầm tay, xem cuống và cách bảo quản cam được lâu.", "g-cam1-1200.webp"),
    ("cach-dung-tinh-bot-san-day.html", "Cách pha tinh bột sắn dây không vón cục", "Mẹo hoà nước lạnh trước, khi nào nên nấu chín và các món khác.", "g-sd1-1200.webp"),
]

NAV = [("san-day.html", "Sắn Dây"), ("cam-duong-canh.html", "Cam Đường Canh"), ("qua-tet-2027.html", "Quà Tết"),
       ("cam-nang.html", "Cẩm nang"), ("ve-chung-toi.html", "Về chúng tôi")]


def head(f, title, desc, img, kind="article", schema=""):
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Thế Hưng Organic</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{f}">
<meta name="theme-color" content="#173f23">
<meta property="og:type" content="{kind}">
<meta property="og:locale" content="vi_VN">
<meta property="og:site_name" content="Thế Hưng Organic">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}assets/{img}">
<meta property="og:url" content="{SITE}{f}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="manifest.json">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,500;9..144,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/home.css">
{schema}<script>document.documentElement.classList.add("js");</script>
</head>
<body>
<a href="#main" class="skip-link">Bỏ qua tới nội dung</a>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="ck" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></symbol>
</svg>
"""


def nav(f, en_href="en/index.html"):
    items = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == f else ""}>{t}</a></li>' for h, t in NAV)
    return f"""
<nav class="nav" id="nav" aria-label="Chính">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="assets/logo-thoc-mark.png" alt="Logo THOC" width="42" height="42"><span>Thế Hưng Organic</span></a>
    <ul>{items}</ul>
    <div class="lang"><a href="{f}" aria-current="page">VI</a><a href="{en_href}" lang="en">EN</a></div>
    <details class="menu"><summary aria-label="Mở menu"><svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg></summary>
      <ul>
        <li><a href="index.html">Trang chủ</a></li>
        <li><a href="san-day.html">Tinh Bột Sắn Dây</a></li>
        <li><a href="cam-duong-canh.html">Cam Đường Canh</a></li>
        <li><a href="qua-tet-2027.html">Quà Tết 2027</a></li>
        <li><a href="mua-si-san-day.html">Mua sỉ sắn dây</a></li>
        <li><a href="cam-nang.html">Cẩm nang</a></li>
        <li><a href="ve-chung-toi.html">Về chúng tôi</a></li>
        <li><a href="dat-truoc.html">Đặt hàng</a></li>
      </ul>
    </details>
    <a class="btn" href="dat-truoc.html">Đặt hàng</a>
  </div>
</nav>
"""


FOOT = """
<footer class="foot">
  <div class="wrap">
    <div class="top">
      <div>
        <p class="name">Thế Hưng Organic</p>
        <ul>
          <li><a href="https://zalo.me/0979502000">Zalo 0979 502 000</a></li>
          <li><a href="tel:0979502000">Gọi 0979 502 000</a></li>
          <li><a href="mailto:hello@thehungorganic.com">hello@thehungorganic.com</a></li>
        </ul>
      </div>
      <ul><li><b>Sản phẩm</b></li><li><a href="san-day.html">Tinh Bột Sắn Dây</a></li><li><a href="cam-duong-canh.html">Cam Đường Canh</a></li><li><a href="qua-tet-2027.html">Quà Tết 2027</a></li><li><a href="mua-si-san-day.html">Mua sỉ sắn dây</a></li></ul>
      <ul><li><b>Mua hàng</b></li><li><a href="dat-truoc.html">Đặt hàng</a></li><li><a href="giao-hang-doi-tra.html">Giao hàng &amp; đổi trả</a></li><li><a href="https://shopee.vn/shop/1700409288" target="_blank" rel="noopener">Shopee</a></li><li><a href="https://www.facebook.com/profile.php?id=61593265823967" target="_blank" rel="noopener">Facebook</a></li></ul>
      <ul><li><b>Tìm hiểu</b></li><li><a href="ve-chung-toi.html">Về chúng tôi</a></li><li><a href="cam-nang.html">Cẩm nang</a></li><li><a href="index.html#faq">Hỏi đáp</a></li></ul>
    </div>
    <div class="legal"><p>© Hợp tác xã Thế Hưng Organic (THOC), Thôn Liên Lạc, xã Vũ Lăng, Lạng Sơn</p><a href="#main">Lên đầu trang ↑</a></div>
  </div>
</footer>

<div class="bar" id="bar" role="region" aria-label="Đặt hàng nhanh">
  <span class="sum" aria-live="polite"></span>
  <a class="btn go" href="dat-truoc.html">Gửi phiếu đặt hàng →</a>
  <span class="quick"><a href="tel:0979502000">Gọi</a><a href="https://zalo.me/0979502000">Zalo</a><a class="btn" href="dat-truoc.html">Đặt hàng</a></span>
</div>

<script src="assets/track.js"></script>
<script src="assets/shop.js"></script>
</body>
</html>
"""


def phead(crumbs, h1, lead=""):
    c = " / ".join(f'<a href="{h}">{t}</a>' if h else t for h, t in crumbs)
    lp = f'<p style="margin-top:12px;font-size:1.08rem;color:var(--muted);max-width:640px">{lead}</p>' if lead else ""
    return f"""
<main id="main" tabindex="-1">
  <header class="phead">
    <div class="wrap" style="max-width:780px">
      <p class="crumbs">{c}</p>
      <h1>{h1}</h1>{lp}
    </div>
  </header>
"""


def var_row(i, name, sub, price):
    pr = vnd(price) if price else "Nhắn báo giá"
    dp = price or ""
    return (f'<li class="var" data-id="{i}" data-price="{dp}"><a href="dat-truoc.html?chon={i}" class="nm">{name}<small>{sub}</small></a>'
            f'<span class="pr"{"" if price else " style=\"font-size:.86em\""}>{pr}</span><span class="step"><button type="button" data-d="-1" aria-label="Bớt 1 {name}">−</button>'
            f'<output aria-live="polite">0</output><button type="button" data-d="1" aria-label="Thêm 1 {name}">+</button></span></li>')


def buy_sd(title="Mua Tinh Bột Sắn Dây", big=False):
    rows = [var_row("sd05", "Túi 0,5kg", "Dùng thử, làm quà nhỏ", PRICE["túi 0.5kg"]),
            var_row("sd1", "Túi 1kg", "Gia đình dùng thường xuyên", PRICE["túi 1kg"])]
    if big:
        rows += [var_row("sd5", "Túi 5kg", "Quán chè, nhà hàng", None), var_row("sd10", "Túi 10kg", "Mua sỉ, đại lý", None)]
    return f"""
  <section id="mua" aria-labelledby="t-mua">
    <div class="wrap" style="max-width:780px">
      <article class="prod rise">
        <div class="img" style="aspect-ratio:16/9"><img src="assets/v2/sd-tui-1200.webp" srcset="assets/v2/sd-tui-640.webp 640w, assets/v2/sd-tui-1200.webp 1200w" sizes="(max-width:800px) 100vw, 780px" alt="Túi tinh bột sắn dây của hợp tác xã" width="1200" height="900" loading="lazy"></div>
        <div class="body">
          <h3 id="t-mua">{title}</h3>
          <p class="desc">Có sẵn quanh năm. Lọc tay, sấy lò, không tẩy trắng, không phụ gia.</p>
          <ul class="vars">{''.join(rows)}</ul>
          <div class="acts">
            <a class="btn" id="buyGo" data-def="sd1" href="dat-truoc.html?chon=sd1">Đặt hàng ngay</a>
            <a class="btn ghost" href="san-day.html">Xem chi tiết sản phẩm</a>
          </div>
        </div>
      </article>
    </div>
  </section>"""


def buy_cam():
    rows = [var_row("cam5", "Thùng 5kg", "Đặt trước mùa mới", PRICE["thùng 5kg"]),
            var_row("cam10", "Thùng 10kg", "Đặt trước mùa mới", PRICE["thùng 10kg"])]
    return f"""
  <section id="mua" aria-labelledby="t-mua">
    <div class="wrap" style="max-width:780px">
      <article class="prod rise">
        <div class="img" style="aspect-ratio:16/9"><img src="assets/v2/cam-bo-1200.webp" alt="Cam Đường Canh vừa hái" width="1200" height="900" loading="lazy"></div>
        <div class="body">
          <h3 id="t-mua">Đặt trước Cam Đường Canh mùa mới</h3>
          <p class="desc">Vườn đạt VietGAP, chín tự nhiên trên cây. Thu hoạch khoảng tháng 11 âm lịch đến tháng 1 năm sau, đặt trước chưa cần thanh toán.</p>
          <ul class="vars">{''.join(rows)}</ul>
          <div class="acts">
            <a class="btn" id="buyGo" data-def="cam10" href="dat-truoc.html?chon=cam10">Đặt trước</a>
            <a class="btn ghost" href="cam-duong-canh.html">Xem chi tiết</a>
          </div>
        </div>
      </article>
    </div>
  </section>"""


def related(skip):
    items = "".join(f'<li><a href="{f}">{t}</a></li>' for f, t, *_ in ARTICLES if f != skip)
    return f"""
    <h2>Đọc thêm</h2>
    <ul>{items}</ul>"""


def article_schema(f, title, desc, img):
    return ('<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
        "image": f"{SITE}assets/v2/{img}", "author": {"@type": "Organization", "name": "Thế Hưng Organic"},
        "publisher": {"@type": "Organization", "name": "Hợp tác xã Thế Hưng Organic"},
        "datePublished": DATE, "mainEntityOfPage": f"{SITE}{f}"}, ensure_ascii=False, indent=2) + "\n</script>\n")


def faq_schema(qas):
    return ('<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]},
        ensure_ascii=False, indent=2) + "\n</script>\n")


def faq_html(qas):
    return "".join(f'<details class="acc"><summary>{q}</summary><p>{a}</p></details>' for q, a in qas)


def figure(img, alt, w=1200, h=900):
    return f'<figure><img src="assets/v2/{img}" alt="{alt}" width="{w}" height="{h}" loading="lazy"></figure>'


# ---------------------------------------------------------------- BÀI VIẾT
def art(f, body, buy):
    t = next(a for a in ARTICLES if a[0] == f)
    _, title, desc, img = t
    html = head(f, title, desc, "home/og-cam-nang.jpg", schema=article_schema(f, title, desc, img)) + nav(f, "en/san-day.html")
    html += phead([("index.html", "Trang chủ"), ("cam-nang.html", "Cẩm nang"), ("", title.split("?")[0][:40])], title, desc)
    html += f'  <article class="article wrap">\n{body}\n{related(f)}\n  </article>\n' + buy + "\n</main>\n" + FOOT
    return html


A_PHANBIET = f"""
    {figure("g-sd4-1200.webp", "Bột sắn dây vừa sấy, còn nguyên dạng tảng và vảy")}
    <p>Bột sắn dây thật đắt hơn bột năng, bột mì nhiều lần, nên trên thị trường có không ít loại bị pha thêm. Không có cách thử nào ở nhà chắc chắn 100%, nhưng gộp 5 dấu hiệu dưới đây lại thì bạn sẽ đoán khá đúng.</p>

    <h2>1. Nhìn hình dạng</h2>
    <p>Bột sắn dây lọc và sấy theo cách truyền thống thường ở dạng <strong>tảng, vảy, hạt to nhỏ không đều</strong>, sờ thấy hơi ráp. Bột mịn đều như bột mì, không còn vảy nào, là dấu hiệu nên hỏi kỹ người bán (có thể đã nghiền nhỏ, cũng có thể đã pha bột khác).</p>

    <h2>2. Nhìn màu</h2>
    <p>Màu tự nhiên là <strong>trắng ngà, trắng hơi ánh xanh</strong>, không trắng tinh như vôi. Bột trắng xoá, sáng loá bất thường có thể đã qua tẩy trắng.</p>

    <h2>3. Bóp và nghe</h2>
    <p>Bốc một nắm bóp mạnh trong tay: bột sắn dây thật thường kêu <strong>"kin kít", "sột sột"</strong> và rời ra khi buông tay. Bột năng, bột mì bóp thấy mịn, bám tay, ít tiếng.</p>

    <h2>4. Ngửi</h2>
    <p>Mùi thơm nhẹ, mát, rất khó tả. Nếu có mùi chua, mùi hôi mốc hay mùi hoá chất thì không nên dùng.</p>

    <h2>5. Thử với nước</h2>
    <ol class="howsteps">
      <li><strong>Nước lạnh:</strong> cho 1 thìa bột vào cốc nước lạnh, khuấy rồi để yên. Bột sắn dây lắng xuống đáy khá nhanh, nước phía trên trong lại.</li>
      <li><strong>Nước sôi:</strong> hoà bột với chút nước lạnh, rồi rót nước sôi vào và khuấy. Bột sắn dây chuyển từ đục sang <strong>trong, hơi sánh</strong>, có mùi thơm nhẹ.</li>
    </ol>
    <p class="anote">Đây là các mẹo kinh nghiệm, không thay được kiểm nghiệm trong phòng thí nghiệm. Cách chắc chắn nhất vẫn là mua của người biết rõ nguồn gốc: thấy được nương trồng, nơi lọc và sấy bột.</p>

    <h2>Bột của nhà mình làm thế nào</h2>
    <p>Củ sắn dây đào từ nương dưới chân núi đá ở xã Vũ Lăng (Bắc Sơn, Lạng Sơn), rửa sạch, nghiền, rồi <strong>lọc và lắng nhiều lượt bằng tay</strong> đến khi bột trắng trong. Bột ướt được sấy trong lò sấy nhiều tầng, không phơi bụi, <strong>không tẩy trắng, không pha thêm gì</strong>. Bạn có thể xem ảnh và video từng bước ở <a href="san-day.html#quy-trinh">trang sản phẩm</a>.</p>"""

A_BOTNANG = f"""
    {figure("g-sd2-1200.webp", "Bột sắn dây dạng tảng trên khay sấy")}
    <p>Cùng là bột trắng, cùng làm sánh món ăn, nên nhiều người hay nhầm. Thật ra đây là hai loại bột làm từ hai loại củ khác nhau.</p>

    <h2>Khác nhau từ củ</h2>
    <ul>
      <li><strong>Bột sắn dây</strong> làm từ củ của cây sắn dây, một loại dây leo. Củ to, nhiều xơ, lượng bột lấy ra ít nên giá cao.</li>
      <li><strong>Bột năng</strong> (bột đao, tinh bột khoai mì) làm từ củ sắn ăn được (khoai mì), trồng rất nhiều nên giá rẻ hơn hẳn.</li>
    </ul>

    <h2>So sánh nhanh</h2>
    <div class="cards" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr));margin:18px 0">
      <div class="card"><div class="b"><h3>Bột sắn dây</h3><ul><li>Dạng tảng, vảy, hạt không đều</li><li>Bóp kêu kin kít</li><li>Thường pha nước uống, nấu chè</li><li>Giá cao hơn</li></ul></div></div>
      <div class="card"><div class="b"><h3>Bột năng</h3><ul><li>Bột mịn đều</li><li>Bóp mịn, bám tay</li><li>Làm bánh bột lọc, trân châu, tạo sánh canh, súp</li><li>Giá rẻ hơn</li></ul></div></div>
    </div>

    <h2>Có dùng thay cho nhau được không?</h2>
    <p>Trong nấu ăn, khi chỉ cần <strong>tạo độ sánh</strong> (súp, nước sốt, chè), hai loại có thể thay nhau, bột năng sánh và dai hơn một chút. Nhưng nếu bạn muốn <strong>pha nước sắn dây uống</strong> theo kiểu truyền thống thì phải dùng bột sắn dây: bột năng pha nước sôi sẽ ra một chất dẻo quánh, không ai uống như vậy.</p>

    <h2>Vì sao có bột sắn dây pha bột năng?</h2>
    <p>Vì bột năng rẻ hơn nhiều mà màu trắng giống nhau. Muốn tự thử ở nhà, xem bài <a href="phan-biet-bot-san-day-that-gia.html">cách phân biệt bột sắn dây thật và bột pha trộn</a>.</p>"""

A_CHE = f"""
    {figure("p2-loc-800.webp", "Lắng lọc bột sắn dây tại xưởng của hợp tác xã", 800, 1000)}
    <p>Bột sắn dây khi chín sẽ trong và sánh mịn, rất hợp làm chè và món tráng miệng mát. Nguyên tắc chung cho mọi món: <strong>luôn hoà bột với nước lạnh trước</strong> rồi mới đổ vào nồi đang sôi, khuấy đều tay để không vón cục.</p>

    <h2>1. Chè sắn dây hạt sen</h2>
    <p><strong>Nguyên liệu (4 bát):</strong> 100g hạt sen tươi hoặc khô, 40–50g bột sắn dây, 80–100g đường phèn, 1 lít nước, vài giọt nước hoa bưởi nếu thích.</p>
    <ol class="howsteps">
      <li>Hạt sen khô ngâm 2–3 tiếng, bỏ tim. Ninh hạt sen với 1 lít nước đến khi chín mềm.</li>
      <li>Cho đường phèn vào, khuấy tan.</li>
      <li>Hoà bột sắn dây với khoảng 150ml nước lạnh, khuấy tan hết.</li>
      <li>Hạ lửa nhỏ, vừa đổ từ từ bột vào nồi vừa khuấy đều một chiều, đến khi chè chuyển trong và sánh thì tắt bếp.</li>
      <li>Để nguội, thêm vài giọt nước hoa bưởi. Ăn nóng hoặc ăn lạnh đều ngon.</li>
    </ol>

    <h2>2. Chè đậu xanh sắn dây</h2>
    <p>Nấu 150g đậu xanh đã cà vỏ với 1,2 lít nước đến khi nhừ, thêm đường vừa ăn. Hoà 40g bột sắn dây với nước lạnh, đổ vào nồi và khuấy ở lửa nhỏ đến khi chè sánh trong. Có thể thêm chút nước cốt dừa khi ăn.</p>

    <h2>3. Sắn dây sữa</h2>
    <p>Hoà 1–2 thìa bột sắn dây với ít nước lạnh, rót nước sôi vào khuấy đến khi trong, để nguội bớt rồi thêm sữa tươi hoặc sữa đặc tuỳ khẩu vị. Thêm đá nếu muốn uống lạnh.</p>

    <h2>4. Thạch sắn dây</h2>
    <p>Đun 500ml nước với đường vừa ăn. Hoà 50g bột sắn dây với 150ml nước lạnh, đổ vào nồi và khuấy liên tục ở lửa nhỏ đến khi hỗn hợp đặc, trong. Đổ ra khuôn, để nguội rồi cho vào tủ lạnh khoảng 2 tiếng, cắt miếng ăn với nước cốt dừa hoặc mật ong.</p>
    <p class="anote">Lượng đường và bột chỉ để tham khảo, bạn tăng giảm theo khẩu vị. Muốn món sánh đặc hơn thì tăng bột, muốn lỏng hơn thì tăng nước.</p>"""

A_UONG = f"""
    {figure("cta-say-800.webp", "Bột sắn dây trên khay lò sấy", 800, 1000)}
    <p>Nước sắn dây là món giải nhiệt quen thuộc của nhiều gia đình Việt, nhất là ngày hè. Dưới đây là những lưu ý theo kinh nghiệm dân gian để uống cho dễ chịu.</p>

    <h2>Pha sống hay nấu chín?</h2>
    <ul>
      <li><strong>Pha nước sôi</strong> (hoà bột với nước lạnh trước, rót nước sôi vào đến khi trong): cách phổ biến nhất, bột đã chín một phần. Xem chi tiết ở bài <a href="cach-dung-tinh-bot-san-day.html">cách pha không vón cục</a>.</li>
      <li><strong>Nấu chín hẳn</strong> trên bếp lửa nhỏ: nhiều gia đình chọn cách này cho trẻ nhỏ, người bụng yếu hoặc khi trời lạnh, vì theo dân gian sắn dây có tính mát, nấu chín sẽ dịu hơn.</li>
      <li><strong>Hoà nước lạnh uống ngay</strong> (không qua nước sôi): một số nơi vẫn uống kiểu này, nhưng bột còn sống, dễ đầy bụng với người tiêu hoá kém. Nhà mình khuyên nên pha nước sôi hoặc nấu chín.</li>
    </ul>

    <h2>Uống bao nhiêu là vừa?</h2>
    <p>Thường mỗi lần 1–2 thìa canh (khoảng 15–20g), một ngày một ly là đủ. Sắn dây là thực phẩm, uống điều độ như các món khác, không phải uống càng nhiều càng tốt.</p>

    <h2>Ai nên hỏi bác sĩ trước?</h2>
    <ul>
      <li>Phụ nữ đang mang thai hoặc cho con bú.</li>
      <li>Trẻ nhỏ, người cao tuổi hay lạnh bụng, đi ngoài.</li>
      <li>Người đang điều trị bệnh hoặc đang dùng thuốc thường xuyên.</li>
    </ul>
    <p class="anote">Tinh bột sắn dây là thực phẩm, không phải thuốc và không thay thế thuốc chữa bệnh. Các công dụng "giải nhiệt, mát" là kinh nghiệm dân gian, không phải khuyến nghị y tế.</p>

    <h2>Không thích uống? Thử nấu món</h2>
    <p>Bột sắn dây còn dùng nấu chè, làm thạch, tạo sánh cho súp. Xem <a href="cach-nau-che-san-day.html">4 món dễ làm với sắn dây</a>.</p>"""

A_CAM = f"""
    {figure("g-cam1-1200.webp", "Cam Đường Canh chín trên cây")}
    <p>Cam Đường Canh nhỏ hơn cam sành, vỏ mỏng, múi mọng và ngọt đậm. Vài mẹo dưới đây giúp bạn chọn được quả ngon, dù mua ở chợ hay đặt online.</p>

    <h2>1. Nhìn vỏ</h2>
    <p>Quả chín đều trên cây thường có <strong>vỏ màu cam đậm hoặc cam hơi đỏ</strong>, bóng nhẹ, da căng mịn. Vỏ có vài đốm nâu nhỏ tự nhiên là bình thường. Tránh quả vỏ nhăn nheo, mềm nhũn hay có chỗ thâm dập.</p>

    <h2>2. Cầm thử</h2>
    <p>Chọn quả <strong>cầm thấy nặng tay</strong> so với kích thước, đó thường là quả nhiều nước. Bóp nhẹ thấy hơi đàn hồi là vừa; quá cứng có thể chưa chín tới, quá mềm có thể đã để lâu.</p>

    <h2>3. Xem cuống</h2>
    <p>Cuống còn tươi, lá đi kèm còn xanh là cam mới hái. Cuống khô đen, rụng hẳn thì cam đã để nhiều ngày.</p>

    <h2>4. Chín cây hay chín ép?</h2>
    <p>Cam chín tự nhiên trên cây có màu chuyển từ từ, đôi khi còn vệt xanh nhẹ gần cuống, vị ngọt đậm có chút chua thanh. Cam vàng đều tăm tắp nhưng ăn nhạt có thể đã hái non rồi xử lý cho đổi màu.</p>

    <h2>5. Bảo quản để cam tươi lâu</h2>
    <ul>
      <li>Mở thùng ngay khi nhận, nhặt riêng quả dập (nếu có) ra ăn trước.</li>
      <li>Để nơi thoáng mát, tránh nắng; không đóng kín trong túi nilon.</li>
      <li>Muốn để lâu hơn thì cho vào ngăn mát tủ lạnh.</li>
    </ul>
    <p>Cam của nhà mình trồng tại vườn đạt <strong>chứng nhận VietGAP</strong> ở Lạng Sơn, chỉ hái khi đã chín trên cây, thu hoạch khoảng tháng 11 âm lịch đến tháng 1 năm sau. Hàng hư do vận chuyển được đổi mới hoặc hoàn tiền, xem <a href="giao-hang-doi-tra.html">chính sách đổi trả</a>.</p>"""


# ---------------------------------------------------------------- TRANG CHÍNH
def p_about():
    f = "ve-chung-toi.html"
    t = "Về Hợp tác xã Thế Hưng Organic"
    d = "Hợp tác xã ở xã Vũ Lăng, Lạng Sơn: trồng sắn dây giữa núi đá, tự lọc và sấy Tinh Bột Sắn Dây, và vườn Cam Đường Canh đạt VietGAP."
    org = ('<script type="application/ld+json">\n' + json.dumps({
        "@context": "https://schema.org", "@type": "Organization", "name": "Hợp tác xã Thế Hưng Organic",
        "alternateName": ["THOC", "Thế Hưng Organic", "The Hung Organic Cooperative"], "url": SITE,
        "logo": f"{SITE}assets/logo-thoc.jpg", "email": "hello@thehungorganic.com", "telephone": "+84979502000",
        "address": {"@type": "PostalAddress", "streetAddress": "Thôn Liên Lạc", "addressLocality": "Xã Vũ Lăng",
                    "addressRegion": "Lạng Sơn", "addressCountry": "VN"},
        "sameAs": ["https://www.facebook.com/profile.php?id=61593265823967", "https://shopee.vn/shop/1700409288"]},
        ensure_ascii=False, indent=2) + "\n</script>\n")
    body = f"""
    {figure("vung-hoa-800.webp", "Nương sắn dây dưới chân núi đá vôi ở Vũ Lăng", 800, 1000)}
    <p><strong>Hợp tác xã Thế Hưng Organic (THOC)</strong> là hợp tác xã nông nghiệp ở xã Vũ Lăng, vùng núi đá vôi Bắc Sơn, tỉnh Lạng Sơn. Các thành viên trồng và tự chế biến hai sản phẩm chính: <a href="san-day.html">Tinh Bột Sắn Dây</a> và <a href="cam-duong-canh.html">Cam Đường Canh</a>.</p>

    <h2>Sắn dây: tự trồng, tự lọc, tự sấy</h2>
    <p>Sắn dây được trồng trên nương dưới chân núi đá. Củ đào về được rửa sạch, nghiền, rồi <strong>lọc và lắng nhiều lượt bằng tay</strong> đến khi bột trắng trong. Từ năm 2026, hợp tác xã đã đầu tư <strong>lò sấy nhiều tầng</strong> thay cho phơi nắng, nên bột khô đều, không bám bụi và không phụ thuộc thời tiết. Bột không tẩy trắng, không pha thêm gì.</p>
    <ol class="howsteps">
      <li>Trồng giữa núi đá, dây leo phủ kín giàn.</li>
      <li>Đào củ, đưa về xưởng trong ngày.</li>
      <li>Rửa sạch, nghiền nát, ép lấy nước bột.</li>
      <li>Lọc và lắng nhiều lượt, thay nước đến khi bột trắng trong.</li>
      <li>Sấy lò nhiều tầng, nhiệt độ cài sẵn.</li>
      <li>Ra lò là đóng túi.</li>
    </ol>

    <h2>Cam Đường Canh đạt VietGAP</h2>
    <p>Vườn cam của hợp tác xã đạt <strong>chứng nhận VietGAP số 112/CN-TĐC-TT-20-0012</strong>, theo tiêu chuẩn TCVN 11892-1:2017, do Công ty Cổ phần Khoa học và Công nghệ NATEK cấp ngày 23/12/2025, hiệu lực đến 22/12/2028. Giấy chứng nhận ghi tên cũ của hợp tác xã là <em>Hợp tác xã Cây Ăn Quả Nhung Giang</em> (đã đổi tên thành Hợp tác xã Thế Hưng Organic).</p>
    <p>Cam chỉ hái khi đã chín trên cây, mùa thu hoạch khoảng tháng 11 âm lịch đến tháng 1 năm sau. Ngoài mùa, nhà mình nhận đặt trước và báo khi có hàng.</p>
    {figure("cam-vuon-toan-canh-900.webp", "Toàn cảnh vườn Cam Đường Canh của hợp tác xã dưới chân núi đá Vũ Lăng", 900, 676)}

    <h2>Điều nhà mình cam kết</h2>
    <ul>
      <li>Chỉ nói điều có thật về sản phẩm: không hứa công dụng chữa bệnh, không gắn chứng nhận chưa có.</li>
      <li>Ảnh và video trên trang đều chụp tại nương, vườn và xưởng của hợp tác xã.</li>
      <li>Hàng hư do vận chuyển, giao sai hoặc lỗi sản xuất được đổi mới hoặc hoàn tiền (<a href="giao-hang-doi-tra.html">xem chính sách</a>).</li>
    </ul>

    <h2>Thông tin liên hệ</h2>
    <ul>
      <li><strong>Tên:</strong> Hợp tác xã Thế Hưng Organic (THOC)</li>
      <li><strong>Trụ sở:</strong> Thôn Liên Lạc, xã Vũ Lăng, tỉnh Lạng Sơn</li>
      <li><strong>Nơi sản xuất sắn dây:</strong> Thôn Nam Hương, xã Vũ Lăng, tỉnh Lạng Sơn</li>
      <li><strong>Zalo / điện thoại:</strong> <a href="https://zalo.me/0979502000">0979 502 000</a></li>
      <li><strong>Email:</strong> <a href="mailto:hello@thehungorganic.com">hello@thehungorganic.com</a></li>
    </ul>
    <p>Đối tác mua sỉ, đại lý, quán chè: xem <a href="mua-si-san-day.html">trang mua sỉ</a>. Khách nước ngoài: <a href="en/about.html">English</a>.</p>"""
    html = head(f, t, d, "home/og-share.jpg", "website", org) + nav(f, "en/about.html")
    html += phead([("index.html", "Trang chủ"), ("", "Về chúng tôi")], t, "Trồng ở Vũ Lăng, chế biến ở Vũ Lăng, gửi đi từ Vũ Lăng.")
    html += f'  <article class="article wrap">{body}\n  </article>\n</main>\n' + FOOT
    return f, html


SHIP_QA = [
    ("Giao hàng mất bao lâu?", "Giao toàn quốc qua đơn vị vận chuyển, thường 2–5 ngày tuỳ khu vực (nội thành nhanh hơn, vùng xa lâu hơn)."),
    ("Phí ship tính thế nào?", "Theo bảng giá của đơn vị vận chuyển, tuỳ khối lượng và nơi nhận, tối đa 70.000đ một đơn. Nhà mình báo phí ship trước, bạn đồng ý rồi mới gửi hàng."),
    ("Thanh toán thế nào?", "Gửi phiếu đặt hàng chưa phải trả tiền. Nhà mình nhắn hoặc gọi xác nhận đơn, báo phí ship và cách thanh toán trước khi giao."),
    ("Được đổi trả trong trường hợp nào?", "Vì là thực phẩm nên không nhận đổi trả hàng đã mở hoặc đã dùng. Hàng hư hỏng do vận chuyển, giao sai loại hoặc số lượng, hoặc lỗi sản xuất thì được đổi mới hoặc hoàn tiền."),
    ("Cần làm gì khi nhận hàng bị hư?", "Quay video lúc mở hàng và báo qua Zalo 0979 502 000 trong vòng 24 giờ kể từ khi nhận. Nhà mình xem video rồi gửi bù hoặc hoàn tiền phần bị hư."),
    ("Cam bị dập vài quả có được đổi không?", "Có. Cam là trái tươi, đi xa dễ dập. Bạn chụp hoặc quay lại số quả hư khi mở thùng, báo trong 24 giờ, nhà mình gửi bù ở lần giao sau hoặc hoàn tiền tương ứng."),
]


def p_ship():
    f = "giao-hang-doi-tra.html"
    t = "Giao hàng & đổi trả"
    d = "Giao toàn quốc 2–5 ngày, phí ship báo trước. Hàng hư do vận chuyển, giao sai hoặc lỗi sản xuất được đổi mới hoặc hoàn tiền."
    body = f"""
    <h2>Giao hàng</h2>
    <ul>
      <li><strong>Phạm vi:</strong> giao toàn quốc qua đơn vị vận chuyển. Cam Đường Canh hiện chỉ giao trong nước.</li>
      <li><strong>Thời gian:</strong> thường 2–5 ngày tuỳ khu vực.</li>
      <li><strong>Phí ship:</strong> theo bảng giá đơn vị vận chuyển, tối đa 70.000đ một đơn, báo trước khi bạn xác nhận đơn.</li>
      <li><strong>Cam Đường Canh:</strong> chỉ giao trong mùa thu hoạch (khoảng tháng 11 âm lịch đến tháng 1 năm sau). Đặt trước thì nhà mình hẹn ngày giao khi xác nhận đơn.</li>
    </ul>

    <h2>Thanh toán</h2>
    <p>Gửi phiếu đặt hàng chưa phải trả tiền. Nhà mình nhắn hoặc gọi xác nhận đơn, báo phí ship và cách thanh toán, bạn đồng ý rồi mới gửi hàng.</p>

    <h2>Đổi trả và hoàn tiền</h2>
    <p>Vì là thực phẩm, nhà mình <strong>không nhận đổi trả hàng đã mở hoặc đã dùng</strong>. Các trường hợp sau được <strong>đổi mới hoặc hoàn tiền</strong>:</p>
    <ul>
      <li>Hàng hư hỏng do vận chuyển (túi rách, ẩm, cam dập hỏng).</li>
      <li>Giao sai loại hoặc thiếu số lượng.</li>
      <li>Lỗi sản xuất (bột có mùi lạ, mốc, lẫn tạp chất).</li>
    </ul>
    <h3>Cách báo</h3>
    <ol class="howsteps">
      <li>Quay video lúc mở hàng (cả lúc bóc thùng hoặc túi).</li>
      <li>Báo qua Zalo <a href="https://zalo.me/0979502000">0979 502 000</a> trong vòng <strong>24 giờ</strong> kể từ khi nhận, gửi kèm video hoặc ảnh.</li>
      <li>Nhà mình xem rồi gửi bù hàng hoặc hoàn tiền phần bị lỗi, bạn không mất thêm phí ship cho phần gửi bù.</li>
    </ol>

    <h2>Hỏi nhanh</h2>
    {faq_html(SHIP_QA)}
    <p style="margin-top:24px">Câu hỏi khác? Nhắn Zalo <a href="https://zalo.me/0979502000">0979 502 000</a> hoặc email <a href="mailto:hello@thehungorganic.com">hello@thehungorganic.com</a>.</p>"""
    html = head(f, t, d, "home/og-share.jpg", "website", faq_schema(SHIP_QA)) + nav(f)
    html += phead([("index.html", "Trang chủ"), ("", "Giao hàng & đổi trả")], "Giao hàng &amp; đổi trả", "Rõ ràng trước khi bạn đặt: ship bao lâu, phí thế nào, hư thì xử lý ra sao.")
    html += f'  <article class="article wrap">{body}\n  </article>\n</main>\n' + FOOT
    return f, html


def p_review():
    # Khách thật tự viết đánh giá → FormSubmit gửi về hello@. Claude chép nguyên văn vào data/testimonials.json
    # khi chủ shop duyệt; KHÔNG tự hiện lên web, KHÔNG gắn AggregateRating cho tới khi có đủ đánh giá thật ở đây.
    f = "viet-danh-gia.html"
    t = "Viết đánh giá"
    d = "Đã mua Tinh Bột Sắn Dây hoặc Cam Đường Canh của Thế Hưng Organic? Để lại vài dòng nhận xét cho người mua sau."
    star = "".join(f'<input type="radio" name="so_sao" id="s{n}" value="{n}"{" required" if n == 5 else ""}><label for="s{n}" title="{n} sao">★</label>' for n in range(5, 0, -1))
    body = f"""
    <style>
      .rv label.t{{display:block;font-weight:600;margin:18px 0 6px}}
      .rv input[type=text],.rv input[type=tel],.rv select,.rv textarea{{width:100%;font:inherit;padding:12px 14px;border:1px solid #cfc8b8;border-radius:12px;background:#fff}}
      .rv textarea{{min-height:140px}}
      .rv .stars{{display:inline-flex;flex-direction:row-reverse;gap:4px}}
      .rv .stars input{{position:absolute;opacity:0;width:1px;height:1px}}
      .rv .stars label{{font-size:38px;line-height:1;color:#d6cfbf;cursor:pointer}}
      .rv .stars input:checked~label,.rv .stars label:hover,.rv .stars label:hover~label{{color:#e8a317}}
      .rv .stars input:focus-visible+label{{outline:2px solid var(--green-d);border-radius:4px}}
      .rv .ok{{display:none;padding:18px;border-radius:14px;background:#eef5ec;margin-top:20px}}
      .rv small{{color:var(--muted)}}
    </style>
    <p>Bạn đã mua Tinh Bột Sắn Dây hoặc Cam Đường Canh của nhà mình? Vài dòng thật lòng của bạn giúp người mua sau yên tâm hơn, và giúp nhà mình làm tốt hơn. Khen hay chê đều được.</p>
    <form class="rv" id="rv" novalidate>
      <label class="t" for="sp">Bạn đã mua gì?</label>
      <select id="sp" name="san_pham" required>
        <option value="">Chọn sản phẩm</option>
        <option>Tinh Bột Sắn Dây</option>
        <option>Cam Đường Canh</option>
        <option>Cả hai</option>
      </select>
      <span class="t" style="display:block;font-weight:600;margin:18px 0 6px" id="lb-sao">Chấm mấy sao?</span>
      <div class="stars" role="radiogroup" aria-labelledby="lb-sao">{star}</div>
      <label class="t" for="nx">Nhận xét của bạn</label>
      <textarea id="nx" name="nhan_xet" required maxlength="1500" placeholder="Ví dụ: bột mịn, pha không vón; cam ngọt, giao 2 ngày..."></textarea>
      <label class="t" for="ten">Tên hiển thị</label>
      <input type="text" id="ten" name="ten" maxlength="60" required placeholder="Ví dụ: Chị Lan, Hà Nội">
      <label class="t" for="sdt">Số điện thoại lúc đặt hàng <small>(không đăng lên web, chỉ để nhà mình đối chiếu đơn)</small></label>
      <input type="tel" id="sdt" name="so_dien_thoai" maxlength="20" inputmode="tel">
      <label style="display:flex;gap:10px;align-items:flex-start;margin-top:18px"><input type="checkbox" name="dong_y_dang" value="có" checked style="margin-top:5px"> <span>Đồng ý cho nhà mình đăng lời nhận xét này lên web, kèm tên hiển thị ở trên.</span></label>
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
      <p style="margin-top:22px"><button class="btn" type="submit">Gửi đánh giá</button></p>
      <p class="err" role="alert" style="color:#b3261e"></p>
      <div class="ok" role="status"><strong>Cảm ơn bạn!</strong> Nhà mình đã nhận được đánh giá. Nhà mình đọc từng đánh giá trước khi đăng lên web.</div>
    </form>
    <p style="margin-top:28px"><small>Nhà mình đăng nguyên văn, không sửa chữ, cả đánh giá chưa tốt. Đánh giá chứa thông tin cá nhân, quảng cáo hoặc không liên quan sẽ không được đăng.</small></p>
    <script>
    (function(){{
      var fm = document.getElementById("rv"), err = fm.querySelector(".err"), ok = fm.querySelector(".ok"), bt = fm.querySelector("button");
      fm.addEventListener("submit", function(e){{
        e.preventDefault(); err.textContent = "";
        if (!fm.san_pham.value || !fm.querySelector("input[name=so_sao]:checked") || fm.nhan_xet.value.trim().length < 5 || !fm.ten.value.trim()){{
          err.textContent = "Bạn chọn sản phẩm, số sao, viết nhận xét và tên hiển thị giúp nhà mình nhé."; return; }}
        var data = new FormData(fm); data.append("_subject", "Đánh giá mới trên web: " + fm.san_pham.value); data.append("_template", "table");
        bt.disabled = true; bt.textContent = "Đang gửi...";
        fetch("https://formsubmit.co/ajax/hello@thehungorganic.com", {{ method: "POST", body: data, headers: {{ Accept: "application/json" }} }})
          .then(function(r){{ if (!r.ok) throw 0; ok.style.display = "block"; bt.style.display = "none";
            if (window.thocTrack) thocTrack("gui-danh-gia"); }})
          .catch(function(){{ bt.disabled = false; bt.textContent = "Gửi đánh giá";
            err.innerHTML = 'Chưa gửi được. Bạn nhắn đánh giá qua <a href="https://zalo.me/0979502000">Zalo 0979 502 000</a> giúp nhà mình nhé.'; }});
      }});
    }})();
    </script>"""
    html = head(f, t, d, "home/og-share.jpg", "website") + nav(f)
    html += phead([("index.html", "Trang chủ"), ("", "Viết đánh giá")], "Viết đánh giá", "Đã mua hàng của nhà mình? Kể cho người mua sau nghe.")
    html += f'  <article class="article wrap">{body}\n  </article>\n</main>\n' + FOOT
    return f, html


TET_QA = [
    ("Khi nào giao quà Tết?", "Cam Đường Canh thu hoạch khoảng tháng 11 âm lịch đến tháng 1 năm sau. Khi xác nhận đơn, nhà mình hẹn ngày giao cụ thể với bạn, ưu tiên giao trước Tết. Đặt trước 26/01/2027 để chắc chắn kịp nhận trước Tết."),
    ("Giá gói quà bao nhiêu?", "Giá gói quà nhà mình báo khi nhắn lại, vì còn tuỳ số lượng và nơi giao. Giá lẻ để tham khảo: cam thùng 5kg " + C5 + ", thùng 10kg " + C10 + "; sắn dây túi 0,5kg " + P05 + ", túi 1kg " + P1 + "."),
    ("Đặt nhiều gửi nhiều địa chỉ được không?", "Được. Với quà biếu công ty, bạn gửi danh sách địa chỉ, nhà mình báo giá và phí ship riêng cho từng nơi."),
    ("Cam bị dập khi giao thì sao?", "Quay video lúc mở thùng, báo Zalo trong 24 giờ, nhà mình gửi bù hoặc hoàn tiền phần hư."),
]


def p_tet():
    f = "qua-tet-2027.html"
    t = "Quà Tết Đinh Mùi 2027: Cam Đường Canh và Tinh Bột Sắn Dây"
    d = "Hộp quà Tết từ vườn: Cam Đường Canh VietGAP chín cây kèm Tinh Bột Sắn Dây lọc tay, sấy lò. Đặt trước, giao toàn quốc, nhận quà biếu công ty."
    body = f"""
  <section class="tet" aria-labelledby="t-tet">
    <div class="wrap">
      <div class="box rise">
        <div class="img"><img src="assets/v2/tet-thung-1000.webp" srcset="assets/v2/tet-thung-560.webp 560w, assets/v2/tet-thung-1000.webp 1000w" sizes="(max-width:1000px) 100vw, 50vw" alt="Thùng Cam Đường Canh xếp sẵn để gửi đi" width="1000" height="1250"></div>
        <div class="txt">
          <h2 id="t-tet">Chọn gói quà</h2>
          <p>Mỗi gói gồm Cam Đường Canh hái đúng mùa và Tinh Bột Sắn Dây của hợp tác xã. Đặt trước để được giữ hàng, chưa cần thanh toán.</p>
          <p><strong>Hạn đặt để kịp nhận trước Tết: 26/01/2027.</strong> Sau ngày này các hãng vận chuyển nghỉ Tết, nhà mình vẫn nhận đơn nhưng không chắc giao kịp.</p>
          <div class="packs">
            <div class="pack"><div><b>Gói nhỏ</b><small>Cam 5kg + Sắn Dây 0,5kg</small></div><span class="p">Nhắn báo giá</span></div>
            <div class="pack"><div><b>Gói lớn</b><small>Cam 10kg + Sắn Dây 1kg</small></div><span class="p">Nhắn báo giá</span></div>
            <div class="pack"><div><b>Quà biếu công ty</b><small>Số lượng lớn, gửi nhiều địa chỉ</small></div><span class="p">Báo giá riêng</span></div>
          </div>
          <div class="row">
            <a class="btn light" href="dat-truoc.html?chon=qua-nho">Đặt gói nhỏ</a>
            <a class="btn light" href="dat-truoc.html?chon=qua-lon">Đặt gói lớn</a>
            <a class="btn glass" href="https://zalo.me/0979502000">Báo giá số lượng lớn</a>
          </div>
        </div>
      </div>
    </div>
  </section>
  <article class="article wrap">
    <h2>Vì sao chọn quà từ vườn</h2>
    <ul>
      <li><strong>Cam Đường Canh đạt VietGAP</strong> (giấy số 112/CN-TĐC-TT-20-0012), chỉ hái khi đã chín trên cây.</li>
      <li><strong>Tinh Bột Sắn Dây</strong> lọc tay nhiều lượt, sấy lò, không tẩy trắng, không phụ gia, để được lâu, người nhận dùng dần sau Tết.</li>
      <li>Hai món của cùng một hợp tác xã ở Vũ Lăng, Lạng Sơn, có nguồn gốc rõ ràng để kể cho người nhận.</li>
      <li>Khách mua cam mùa trước chấm <strong>4,85/5 sao trên 106 đánh giá</strong> ở Shopee (<a href="cam-duong-canh.html#danh-gia">đọc đánh giá</a>).</li>
    </ul>
    {figure("g-cam2-1200.webp", "Cam Đường Canh chín đỏ trên cành")}
    <h2>Mua lẻ từng món</h2>
    <p>Cam thùng 5kg <strong>{C5}</strong>, thùng 10kg <strong>{C10}</strong>. Sắn dây túi 0,5kg <strong>{P05}</strong>, túi 1kg <strong>{P1}</strong>. Chưa gồm phí ship.</p>
    <h2>Hỏi nhanh</h2>
    {faq_html(TET_QA)}
  </article>"""
    html = head(f, t, d, "home/og-cam.jpg", "website", faq_schema(TET_QA)) + nav(f)
    html += phead([("index.html", "Trang chủ"), ("", "Quà Tết 2027")], "Quà Tết Đinh Mùi 2027", "Cam Đường Canh VietGAP và Tinh Bột Sắn Dây từ cùng một hợp tác xã ở Lạng Sơn.")
    html += body + buy_cam() + "\n</main>\n" + FOOT
    return f, html


SI_QA = [
    ("Giá sỉ bao nhiêu?", "Giá túi 5kg, 10kg và giá theo số lượng nhà mình báo khi bạn nhắn, tuỳ số lượng mỗi lần lấy và nơi giao."),
    ("Có gửi mẫu thử không?", "Có. Bạn có thể đặt túi 0,5kg (" + P05 + ") để thử trước khi lấy số lượng lớn."),
    ("Bột có giấy tờ gì?", "Tinh Bột Sắn Dây hiện chưa có chứng nhận chất lượng chính thức (như VietGAP, ATTP). Vườn cam của hợp tác xã thì đã đạt VietGAP. Bạn có thể xem quy trình làm bột qua ảnh và video thật trên trang sản phẩm."),
    ("Có xuất khẩu không?", "Có nhận trao đổi với đối tác nước ngoài cho Tinh Bột Sắn Dây. Xem trang tiếng Anh hoặc email hello@thehungorganic.com."),
]


def p_si():
    f = "mua-si-san-day.html"
    t = "Mua sỉ Tinh Bột Sắn Dây cho quán chè, nhà hàng, đại lý"
    d = "Tinh Bột Sắn Dây túi 5kg, 10kg cho quán chè, nhà hàng, đại lý. Lọc tay, sấy lò, không tẩy trắng. Nhắn Zalo 0979 502 000 để báo giá."
    body = f"""
  <article class="article wrap">
    {figure("p3-say-800.webp", "Khay bột sắn dây trong lò sấy của hợp tác xã", 800, 1000)}
    <p>Quán chè, quán nước, nhà hàng hay đại lý cần sắn dây dùng hằng ngày có thể lấy <strong>túi 5kg và 10kg</strong>: cùng mẻ bột như túi lẻ, đóng túi lớn cho tiện dùng.</p>
    <h2>Bạn nhận được gì</h2>
    <ul>
      <li>Bột lọc tay nhiều lượt, <strong>sấy lò</strong> nên khô đều, không bám bụi.</li>
      <li><strong>Không tẩy trắng, không phụ gia</strong>, màu trắng ngà tự nhiên.</li>
      <li>Biết rõ nguồn gốc: nương, xưởng lọc và lò sấy đều ở xã Vũ Lăng, Lạng Sơn.</li>
      <li>Có hàng quanh năm vì bột đã sấy khô.</li>
    </ul>
    <h2>Cách đặt sỉ</h2>
    <ol class="howsteps">
      <li>Nhắn Zalo <a href="https://zalo.me/0979502000">0979 502 000</a> số lượng bạn cần mỗi lần và địa chỉ nhận.</li>
      <li>Nhà mình báo giá theo số lượng và phí ship.</li>
      <li>Muốn thử trước: đặt túi 0,5kg ({P05}) để kiểm tra chất bột.</li>
    </ol>
    <h2>Hỏi nhanh</h2>
    {faq_html(SI_QA)}
  </article>"""
    html = head(f, t, d, "home/og-san-day.jpg", "website", faq_schema(SI_QA)) + nav(f, "en/san-day.html#export")
    html += phead([("index.html", "Trang chủ"), ("san-day.html", "Sắn Dây"), ("", "Mua sỉ")], "Mua sỉ Tinh Bột Sắn Dây", "Túi 5kg, 10kg cho quán chè, nhà hàng, đại lý. Nhắn để nhận báo giá theo số lượng.")
    html += body + buy_sd("Đặt túi lớn hoặc túi thử", big=True) + "\n</main>\n" + FOOT
    return f, html


def p_camnang():
    f = "cam-nang.html"
    t = "Cẩm nang sắn dây và cam Đường Canh"
    d = "Cách pha sắn dây không vón cục, phân biệt bột thật giả, sắn dây khác bột năng, công thức chè, cách chọn cam Đường Canh ngon."
    cards = "".join(
        f'<a class="card rise" href="{fn}" style="text-decoration:none;color:inherit"><div class="img"><img src="assets/v2/{img}" alt="" width="1200" height="900" loading="lazy"></div><div class="b"><h3>{tt}</h3><p>{ds}</p></div></a>'
        for fn, tt, ds, img in ARTICLES)
    body = f"""
  <section>
    <div class="wrap">
      <div class="cards" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">{cards}</div>
    </div>
  </section>"""
    html = head(f, t, d, "home/og-cam-nang.jpg", "website") + nav(f)
    html += phead([("index.html", "Trang chủ"), ("", "Cẩm nang")], "Cẩm nang", "Mẹo dùng sắn dây, công thức món ngon và cách chọn cam, viết từ kinh nghiệm của nhà làm.")
    html += body + "\n</main>\n" + FOOT
    return f, html


# ---------------------------------------------------------------- TIẾNG ANH
def p_about_en():
    src = (DOCS / "en" / "index.html").read_text(encoding="utf-8")
    # dùng lại đầu trang + chân trang của trang tiếng Anh hiện có để giữ đúng điều hướng EN
    top = src[:src.index("</nav>") + len("</nav>")] + "\n\n"
    bot = src[src.index("</main>") + len("</main>"):]
    top = (top.replace("<title>", "<title>About us — ", 1) if "<title>" in top else top)
    import re
    top = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="https://thehungorganic.com/en/about.html">', top)
    top = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="The Hung Organic Cooperative (THOC) in Vu Lang, Lang Son, Vietnam: hand-filtered, oven-dried kudzu root starch and VietGAP-certified Canh mandarins.">', top)
    top = re.sub(r'<title>[^<]*</title>', '<title>About The Hung Organic Cooperative (THOC)</title>', top)
    body = """<main id="main" tabindex="-1">
  <header class="phead">
    <div class="wrap" style="max-width:780px">
      <p class="crumbs"><a href="index.html">Home</a> / About</p>
      <h1>About The Hung Organic Cooperative</h1>
      <p style="margin-top:12px;font-size:1.08rem;color:var(--muted)">Grown, processed and shipped from Vu Lang commune, Lang Son, Vietnam.</p>
    </div>
  </header>
  <article class="article wrap">
    <figure><img src="../assets/v2/vung-hoa-800.webp" alt="Kudzu fields below limestone mountains in Vu Lang" width="800" height="1000" loading="lazy"></figure>
    <p><strong>The Hung Organic Cooperative (THOC)</strong> is an agricultural cooperative in Vu Lang commune, in the limestone mountains of Bac Son, Lang Son province, northern Vietnam. Members grow and process two products: kudzu root starch and Canh mandarins.</p>
    <h2>Kudzu root starch</h2>
    <p>Kudzu is grown on fields at the foot of the limestone mountains. The roots are washed, crushed, then <strong>filtered and settled by hand several times</strong> until the starch is clean and white. Since 2026 the cooperative dries the starch in a multi-tray drying oven instead of in the sun. No bleaching, no additives. The cooperative produces approximately 10 to 20 tonnes of starch per month. Kudzu root starch does not yet hold a formal food-safety certification.</p>
    <h2>Canh mandarins (VietGAP)</h2>
    <p>The cooperative's orchard holds <strong>VietGAP certificate no. 112/CN-TĐC-TT-20-0012</strong> (TCVN 11892-1:2017), issued by NATEK JSC on 23 Dec 2025 and valid until 22 Dec 2028, under the cooperative's former name. Mandarins are fresh fruit and are currently sold <strong>within Vietnam only</strong>.</p>
    <h2>Wholesale and export</h2>
    <p>We welcome enquiries from importers and wholesale buyers for kudzu root starch. See <a href="wholesale.html">specifications and sample requests</a> or email <a href="mailto:hello@thehungorganic.com">hello@thehungorganic.com</a>.</p>
    <h2>Contact</h2>
    <ul>
      <li>The Hung Organic Cooperative (THOC), Lien Lac village, Vu Lang commune, Lang Son, Vietnam</li>
      <li>Email: <a href="mailto:hello@thehungorganic.com">hello@thehungorganic.com</a></li>
      <li>WhatsApp: <a href="https://wa.me/84363589920">+84 363 589 920</a> · Zalo: 0979 502 000</li>
    </ul>
  </article>
</main>"""
    return "en/about.html", top + body + bot


# Thông số xuất khẩu Tinh Bột Sắn Dây — số liệu do chủ shop cung cấp 2026-10-27 (HSD "2/3 năm" → ghi mức thấp 24 tháng).
# Dùng chung cho trang en/wholesale.html và bảng thông số in được en/spec-sheet.html (+ PDF).
EXPORT_SPEC = [
    ("Product", "Kudzu root starch (Vietnamese: <em>tinh bột sắn dây</em>), from kudzu roots (<em>Pueraria</em>)"),
    ("Ingredients", "100% kudzu root starch. No additives, no bleaching agents"),
    ("Process", "Roots washed and crushed; starch filtered and settled by hand several times; dried in a multi-tray drying oven"),
    ("Appearance", "Dry, white starch in natural pieces"),
    ("Packaging", "0.5 kg and 1 kg retail bags; 5 kg and 10 kg bulk bags. Other sizes: please ask"),
    ("Shelf life", "24 months from the production date, unopened"),
    ("Storage", "Cool, dry place away from direct sunlight; reseal after opening"),
    ("Production capacity", "Approx. 10–20 tonnes per month"),
    ("Minimum export order", "100 kg"),
    ("Origin", "Vu Lang commune, Lang Son province, Vietnam"),
    ("Producer", "The Hung Organic Cooperative (THOC)"),
    ("Laboratory test report", "Being prepared; ask us for the current status"),
    ("Certification", "No formal food-safety certification yet"),
    ("Price, lead time, shipping terms", "Quoted per order: tell us the destination country, volume and packaging"),
]
EXPORT_QA = [
    ("Can you send a sample?", "Yes. We can send a small sample so you can check the starch before ordering. Tell us your country and we will confirm the courier and cost with you first."),
    ("What is the minimum order for export?", "100 kg. Smaller quantities are possible for samples and first trial orders; please ask."),
    ("How much can you supply?", "The cooperative produces approximately 10 to 20 tonnes of kudzu root starch per month."),
    ("Do you have a laboratory test report or certificates?", "A laboratory test report is being prepared and we will share it with buyers on request. Kudzu root starch does not yet hold a formal food-safety certification such as HACCP. We will update this page as documents are issued."),
    ("Do you export the Canh mandarins too?", "No. Mandarins are fresh fruit and are currently sold within Vietnam only. For export we offer kudzu root starch."),
]
SPEC_PDF = "assets/thoc-kudzu-root-starch-spec-sheet.pdf"


def spec_rows():
    return "\n".join(f'        <tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in EXPORT_SPEC)


def en_shell(f, title, desc):
    # đầu trang + chân trang lấy từ trang chủ tiếng Anh, giống p_about_en
    import re
    src = (DOCS / "en" / "index.html").read_text(encoding="utf-8")
    top = src[:src.index("</nav>") + len("</nav>")] + "\n\n"
    bot = src[src.index("</main>") + len("</main>"):]
    top = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{SITE}{f}">', top)
    top = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', top)
    top = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', top)
    return top, bot


def p_wholesale_en():
    f = "en/wholesale.html"
    top, bot = en_shell(f, "Kudzu Root Starch for Wholesale &amp; Export — The Hung Organic",
                        "Kudzu root starch from Lang Son, Vietnam for importers and wholesale buyers: 100% kudzu starch, 24-month shelf life, approx. 10-20 tonnes per month, minimum export order 100 kg. Request a sample.")
    faq = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in EXPORT_QA]}, ensure_ascii=False)
    top = top.replace("</head>", f'<script type="application/ld+json">{faq}</script>\n</head>', 1)
    pics = "".join(f'<li><img src="../assets/story/{n}-640.webp" alt="{a}" width="640" height="800" loading="lazy"><span>{c}</span></li>' for n, a, c in [
        ("sd1", "Kudzu field below limestone hills in Vu Lang", "Grown below the limestone hills"),
        ("sd4", "Hand-filtering kudzu starch in a basin", "Filtered and settled by hand"),
        ("sd5", "Loading trays into a multi-level drying oven", "Dried in a multi-tray oven"),
        ("sd6", "Freshly dried kudzu starch in bags", "Bagged straight from the oven"),
    ])
    qa = "\n".join(f'          <details><summary>{q}<span class="pm" aria-hidden="true"></span></summary><p>{a}</p></details>' for q, a in EXPORT_QA)
    body = f"""<main id="main" tabindex="-1">
  <header class="phead">
    <div class="wrap">
      <p class="crumbs"><a href="index.html">Home</a> / Wholesale &amp; export</p>
      <h1>Kudzu root starch for importers and wholesale buyers</h1>
      <p class="lead">100% kudzu root starch from the limestone hills of Lang Son, Vietnam. <b>Approx. 10–20 tonnes per month</b>, minimum export order <b>100 kg</b>, shelf life <b>24 months</b>.</p>
      <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:24px">
        <a class="btn" href="#sample">Request a sample</a>
        <a class="btn ghost" href="../{SPEC_PDF}" download>Download spec sheet (PDF)</a>
      </div>
    </div>
  </header>

  <section style="padding-top:0">
    <div class="wrap">
      <ul class="wpics">{pics}</ul>
    </div>
  </section>

  <section class="info" id="specs" aria-labelledby="t-spec">
    <div class="wrap">
      <div class="head"><h2 id="t-spec">Product specifications</h2><p>Figures supplied by the cooperative. <a class="tlink" href="spec-sheet.html">Printable version</a></p></div>
      <table class="spec">
{spec_rows()}
      </table>
    </div>
  </section>

  <section id="sample" aria-labelledby="t-smp">
    <div class="wrap" style="max-width:820px">
      <div class="head"><h2 id="t-smp">Request a sample or a quote</h2><p>We reply by email within 2 working days. You can also write to <a class="tlink" href="mailto:hello@thehungorganic.com">hello@thehungorganic.com</a> or <a class="tlink" href="https://wa.me/84363589920">WhatsApp</a>.</p></div>
      <form id="wform" novalidate>
        <div class="fields">
          <div class="field"><label for="w-name">Your name</label><input id="w-name" name="name" required autocomplete="name"></div>
          <div class="field"><label for="w-co">Company <small>(optional)</small></label><input id="w-co" name="company" autocomplete="organization"></div>
          <div class="field"><label for="w-email">Email</label><input id="w-email" name="email" type="email" required autocomplete="email"></div>
          <div class="field"><label for="w-country">Destination country</label><input id="w-country" name="country" required autocomplete="country-name"></div>
          <div class="field"><label for="w-want">I would like</label><select id="w-want" name="request"><option>A sample</option><option>A price quote</option><option>A sample and a quote</option></select></div>
          <div class="field"><label for="w-vol">Expected volume <small>(optional)</small></label><input id="w-vol" name="volume" placeholder="e.g. 500 kg per month"></div>
          <div class="field full"><label for="w-msg">Message <small>(optional)</small></label><textarea id="w-msg" name="message" placeholder="Packaging you need, intended use, timeline…"></textarea></div>
        </div>
        <p style="margin-top:18px"><button class="btn" type="submit">Send request</button></p>
        <p id="wstatus" role="status" aria-live="polite" style="margin-top:12px;color:var(--muted)"></p>
      </form>
    </div>
  </section>

  <section class="faq" id="faq" aria-labelledby="t-faq">
    <div class="wrap">
      <div class="side"><h2 id="t-faq">Questions buyers ask</h2><p>Kudzu root starch is the product we offer for export. See <a class="tlink" href="san-day.html#process">how it is made</a>.</p></div>
      <div class="acc">
{qa}
      </div>
    </div>
  </section>
</main>
<script>
(function(){{
  var f = document.getElementById("wform"), st = document.getElementById("wstatus");
  f.addEventListener("submit", function(e){{
    e.preventDefault();
    var bad = null;
    [].slice.call(f.querySelectorAll("[required]")).forEach(function(i){{
      var ok = i.value.trim() && (i.type !== "email" || /.+@.+\\..+/.test(i.value));
      i.setAttribute("aria-invalid", ok ? "false" : "true"); if (!ok && !bad) bad = i;
    }});
    if (bad){{ st.textContent = "Please fill in your name, a valid email and the destination country."; bad.focus(); return; }}
    var d = {{}}; new FormData(f).forEach(function(v, k){{ d[k] = v; }});
    d._subject = "Export enquiry: " + d.request + " (" + d.country + ")"; d._template = "table"; d._replyto = d.email;
    var btn = f.querySelector("button"); btn.disabled = true; st.textContent = "Sending…";
    var mail = "mailto:hello@thehungorganic.com?subject=" + encodeURIComponent(d._subject) + "&body=" + encodeURIComponent(Object.keys(d).filter(function(k){{ return k[0] !== "_"; }}).map(function(k){{ return k + ": " + d[k]; }}).join("\\n"));
    fetch("https://formsubmit.co/ajax/hello@thehungorganic.com", {{ method: "POST", headers: {{ "Content-Type": "application/json", "Accept": "application/json" }}, body: JSON.stringify(d) }})
      .then(function(r){{ return r.json(); }})
      .then(function(j){{ if (String(j.success) !== "true") throw 0; f.reset(); st.innerHTML = "Thank you. Your request has been sent; we will reply by email within 2 working days."; }})
      .catch(function(){{ st.innerHTML = 'We could not send the form. Please <a class="tlink" href="' + mail + '">email us directly</a> (your details are filled in).'; }})
      .then(function(){{ btn.disabled = false; }});
  }});
}})();
</script>"""
    return f, top + body + bot


def p_spec_sheet_en():
    # bản in 1 trang A4; PDF xuất bằng Chrome headless (xem cuối main)
    f = "en/spec-sheet.html"
    pics = "".join(f'<img src="../assets/story/sheet-{n}.jpg" alt="">' for n in ("sd1", "sd4", "sd5", "sd6"))
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kudzu Root Starch: Specification Sheet — The Hung Organic Cooperative</title>
<link rel="canonical" href="{SITE}{f}"><meta name="robots" content="noindex">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600&family=Fraunces:opsz,wght@9..144,600&display=swap&subset=vietnamese" rel="stylesheet">
<style>
@page{{size:A4;margin:12mm}}
*{{box-sizing:border-box}}
body{{margin:0;background:#faf8f3;color:#1c2a20;font:400 11pt/1.45 "Be Vietnam Pro",Arial,sans-serif}}
.sheet{{max-width:186mm;margin:0 auto;padding:10mm 0;background:#faf8f3}}
header{{display:flex;align-items:center;gap:14px;border-bottom:2px solid #245c33;padding-bottom:10px}}
header img{{width:54px;height:54px;border-radius:50%}}
header b{{display:block;font:600 13pt/1.2 Fraunces,Cambria,serif}}
header span{{font-size:9.5pt;color:#55615a}}
h1{{font:600 22pt/1.1 Fraunces,Cambria,serif;margin:16px 0 4px;color:#173f23}}
.sub{{color:#55615a;margin:0 0 12px}}
.pics{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:0 0 14px}}
.pics img{{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:6px}}
table{{width:100%;border-collapse:collapse;font-size:10pt}}
th,td{{text-align:left;vertical-align:top;padding:6px 8px;border-bottom:1px solid #e3ded2}}
th{{width:34%;font-weight:600;color:#173f23}}
tr:nth-child(odd) td,tr:nth-child(odd) th{{background:#f1ede3}}
footer{{margin-top:14px;padding-top:10px;border-top:2px solid #245c33;font-size:9.5pt;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}}
footer b{{color:#173f23}}
.note{{font-size:8.5pt;color:#55615a;margin-top:8px}}
@media screen and (max-width:700px){{.sheet{{padding:16px}} .pics{{grid-template-columns:repeat(2,1fr)}} th{{width:40%}}}}
@media print{{body,.sheet{{background:#fff}} .sheet{{padding:0}}}}
</style></head>
<body><div class="sheet">
<header><img src="../assets/logo-thoc-mark.png" alt="THOC logo"><div><b>The Hung Organic Cooperative (THOC)</b><span>Lien Lac village, Vu Lang commune, Lang Son, Vietnam</span></div></header>
<h1>Kudzu Root Starch</h1>
<p class="sub">Specification sheet for importers and wholesale buyers · Updated October 2026</p>
<div class="pics">{pics}</div>
<table>
{spec_rows()}
</table>
<footer>
<div><b>Contact</b><br>hello@thehungorganic.com<br>WhatsApp +84 363 589 920</div>
<div><b>Request a sample</b><br>thehungorganic.com/en/wholesale.html</div>
</footer>
<p class="note">Information supplied by the cooperative. Kudzu root starch is a food ingredient and is not intended to diagnose, treat or cure any condition.</p>
</div></body></html>
"""
    return f, html


def main():
    pages = [
        p_about(), p_ship(), p_review(), p_tet(), p_si(), p_camnang(), p_about_en(), p_wholesale_en(), p_spec_sheet_en(),
        ("phan-biet-bot-san-day-that-gia.html", art("phan-biet-bot-san-day-that-gia.html", A_PHANBIET, buy_sd())),
        ("bot-san-day-khac-bot-nang.html", art("bot-san-day-khac-bot-nang.html", A_BOTNANG, buy_sd())),
        ("cach-nau-che-san-day.html", art("cach-nau-che-san-day.html", A_CHE, buy_sd())),
        ("uong-san-day-dung-cach.html", art("uong-san-day-dung-cach.html", A_UONG, buy_sd())),
        ("cach-chon-cam-duong-canh.html", art("cach-chon-cam-duong-canh.html", A_CAM, buy_cam())),
    ]
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    for f, html in pages:
        if only and only not in f:
            continue
        (DOCS / f).write_text(html, encoding="utf-8")
        print("OK", f)


if __name__ == "__main__":
    main()
