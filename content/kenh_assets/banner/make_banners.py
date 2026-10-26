#!/usr/bin/env python3
"""Dựng bộ banner THOC (ảnh thật + chữ + logo) bằng HTML rồi chụp bằng Chrome headless.

Chạy: C:/Users/Admin/AppData/Local/Python/bin/python.exe content/kenh_assets/banner/make_banners.py
Ra:   content/kenh_assets/banner/*.png (+ og-share.jpg chép sang docs/assets/home/ cho ảnh chia sẻ link)

Lưu ý máy này: Chrome của người dùng hay đang mở -> phải dùng --user-data-dir riêng, và đường dẫn
--screenshot phải là đường dẫn ĐẦY ĐỦ (tương đối sẽ ghi sai chỗ mà lệnh vẫn báo thành công).
Chỉ dùng số liệu thật: giá trong data/products.json, đánh giá trong data/testimonials.json.
"""
import json, os, subprocess, sys, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
A = ROOT / "docs" / "assets"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

rv = json.load(open(ROOT / "data" / "testimonials.json", encoding="utf-8"))["shopee_summary"]
RATING = f"{rv['avg']:.2f}".replace(".", ",")
REVIEWS = rv["total"]

def u(p):  # file URL cho ảnh
    return (A / p).resolve().as_uri()

BASE = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%(w)dpx;height:%(h)dpx;overflow:hidden;background:#14100c}
body{font-family:'Segoe UI',Arial,sans-serif;color:#fff;position:relative}
.bg{position:absolute;inset:0;background:center/cover no-repeat}
.shade{position:absolute;inset:0}
.serif{font-family:Cambria,Georgia,serif}
.logo{border-radius:50%%;background:#fff;box-shadow:0 6px 24px rgba(0,0,0,.45)}
.gold{color:#e6c878}
.pill{display:inline-block;border-radius:999px;background:rgba(20,16,12,.72);border:2px solid rgba(201,162,39,.6)}
.btn{display:inline-block;background:#c9a227;color:#14100c;font-weight:800;border-radius:8px;letter-spacing:.04em}
.star{color:#f5b301}
"""

BANNERS = {
 # 1) Ảnh bìa Facebook/Zalo — nội dung chính nằm giữa (điện thoại cắt 2 bên)
 "bia-facebook-1640x624": (1640, 624, """
<div class="bg" style="background-image:url('%(vung)s')"></div>
<div class="shade" style="background:linear-gradient(90deg,rgba(10,8,6,.15) 0%%,rgba(10,8,6,.78) 30%%,rgba(10,8,6,.78) 70%%,rgba(10,8,6,.15) 100%%)"></div>
<div style="position:absolute;left:250px;right:250px;top:0;bottom:0;display:flex;align-items:center;gap:44px">
  <img class="logo" src="%(logo)s" style="width:210px;height:210px">
  <div>
    <div style="font-size:24px;letter-spacing:.28em;text-transform:uppercase" class="gold">Hợp tác xã · Vũ Lăng, Lạng Sơn</div>
    <div class="serif" style="font-size:86px;line-height:1.05;margin:10px 0 14px">Thế Hưng Organic</div>
    <div style="font-size:31px;color:#efe6d3">Tinh Bột Sắn Dây · Cam Đường Canh VietGAP</div>
    <div style="font-size:27px;margin-top:22px;color:#efe6d3"><span class="star">★★★★★</span> %(rating)s/5 · %(reviews)s đánh giá Shopee &nbsp;|&nbsp; thehungorganic.com</div>
  </div>
</div>"""),
 # 2) Banner gian hàng Shopee
 "banner-shopee-1200x600": (1200, 600, """
<div class="bg" style="background-image:url('%(bot)s');left:600px"></div>
<div class="shade" style="left:0;right:600px;background:#1d1712"></div>
<div class="shade" style="background:linear-gradient(90deg,#1d1712 49%%,rgba(29,23,18,0) 62%%)"></div>
<div style="position:absolute;left:60px;top:60px;width:600px">
  <img class="logo" src="%(logo)s" style="width:96px;height:96px">
  <div class="serif" style="font-size:66px;line-height:1.08;margin:22px 0 14px">Tinh Bột Sắn Dây<br><span class="gold">trắng tự nhiên</span></div>
  <div style="font-size:24px;color:#efe6d3;line-height:1.5">Lọc nhiều lượt · Sấy lò kiểm soát nhiệt<br>Không tẩy trắng · Không phụ gia</div>
  <div class="pill" style="margin-top:26px;padding:12px 24px;font-size:26px">Túi 0,5kg <b class="gold">%(p05)s</b> · 1kg <b class="gold">%(p1)s</b></div>
  <div style="margin-top:22px;font-size:20px;color:#cfc4ac">Hợp tác xã Thế Hưng Organic · Lạng Sơn</div>
</div>"""),
 # 3) Quảng cáo vuông (Facebook/Instagram/Zalo) — Sắn dây
 "qc-vuong-san-day-1080": (1080, 1080, """
<div class="bg" style="background-image:url('%(nuong)s')"></div>
<div class="shade" style="background:linear-gradient(180deg,rgba(10,8,6,.35) 0%%,rgba(10,8,6,.15) 30%%,rgba(10,8,6,.88) 62%%,rgba(10,8,6,.96) 100%%)"></div>
<img class="logo" src="%(logo)s" style="position:absolute;left:60px;top:56px;width:120px;height:120px">
<div style="position:absolute;left:64px;right:64px;bottom:64px">
  <div style="font-size:26px;letter-spacing:.24em;text-transform:uppercase" class="gold">Từ nương núi đá Bắc Sơn</div>
  <div class="serif" style="font-size:84px;line-height:1.05;margin:14px 0 18px">Tinh Bột Sắn Dây<br>trắng tự nhiên</div>
  <div style="font-size:31px;color:#efe6d3">Không tẩy trắng · Không phụ gia · Sấy lò</div>
  <div style="display:flex;align-items:center;justify-content:space-between;margin-top:34px">
    <div class="pill" style="padding:14px 28px;font-size:32px">Chỉ từ <b class="gold">%(p05)s</b></div>
    <div class="btn" style="padding:20px 34px;font-size:30px">Đặt: thehungorganic.com</div>
  </div>
</div>"""),
 # 4) Story / Reels dọc — Cam đặt trước
 "story-cam-dat-truoc-1080x1920": (1080, 1920, """
<div class="bg" style="background-image:url('%(cam)s')"></div>
<div class="shade" style="background:linear-gradient(180deg,rgba(10,8,6,.8) 0%%,rgba(10,8,6,.35) 22%%,rgba(10,8,6,.05) 32%%,rgba(10,8,6,.1) 48%%,rgba(10,8,6,.92) 70%%,rgba(10,8,6,.97) 100%%)"></div>
<div style="position:absolute;top:120px;left:0;right:0;text-align:center">
  <img class="logo" src="%(logo)s" style="width:150px;height:150px">
  <div style="font-size:30px;letter-spacing:.24em;text-transform:uppercase;margin-top:22px" class="gold">Hợp tác xã Thế Hưng Organic</div>
</div>
<div style="position:absolute;left:70px;right:70px;bottom:150px;text-align:center">
  <div class="serif" style="font-size:96px;line-height:1.05">Cam Đường Canh<br><span class="gold">mùa mới</span></div>
  <div style="font-size:36px;color:#efe6d3;margin:26px 0 30px">Chín tự nhiên trên cây · Chứng nhận VietGAP</div>
  <div style="font-size:38px"><span class="star">★★★★★</span> %(rating)s/5 · %(reviews)s đánh giá Shopee</div>
  <div class="pill" style="margin-top:40px;padding:18px 34px;font-size:36px">Thùng 5kg <b class="gold">%(c5)s</b> · 10kg <b class="gold">%(c10)s</b></div>
  <div class="btn" style="margin-top:44px;padding:28px 48px;font-size:40px">Đặt trước — chưa cần thanh toán</div>
  <div style="font-size:32px;color:#cfc4ac;margin-top:30px">thehungorganic.com · Zalo 0979 502 000</div>
</div>"""),
 # 5) Ảnh hiện khi chia sẻ link website (Facebook/Zalo/Messenger)
 "og-share-1200x630": (1200, 630, """
<div class="bg" style="background-image:url('%(vung)s')"></div>
<div class="shade" style="background:linear-gradient(90deg,rgba(10,8,6,.88) 0%%,rgba(10,8,6,.7) 48%%,rgba(10,8,6,.1) 100%%)"></div>
<div style="position:absolute;left:70px;top:70px;width:720px">
  <img class="logo" src="%(logo)s" style="width:110px;height:110px">
  <div class="serif" style="font-size:72px;line-height:1.05;margin:24px 0 16px">Thế Hưng Organic</div>
  <div style="font-size:30px;color:#efe6d3;line-height:1.45">Tinh Bột Sắn Dây trắng tự nhiên<br>Cam Đường Canh VietGAP · Lạng Sơn</div>
  <div style="font-size:26px;margin-top:26px"><span class="star">★★★★★</span> %(rating)s/5 · %(reviews)s đánh giá Shopee</div>
</div>"""),
 # 6) Ảnh bìa YouTube — chữ nằm trong vùng an toàn 1546x423 ở giữa (TV hiện cả ảnh, điện thoại chỉ hiện dải giữa)
 "bia-youtube-2560x1440": (2560, 1440, """
<div class="bg" style="background-image:url('%(suong)s')"></div>
<div class="shade" style="background:linear-gradient(90deg,rgba(10,8,6,.25) 0%%,rgba(10,8,6,.8) 28%%,rgba(10,8,6,.8) 72%%,rgba(10,8,6,.25) 100%%)"></div>
<div style="position:absolute;left:507px;width:1546px;top:509px;height:423px;display:flex;align-items:center;gap:56px;padding:0 40px">
  <img class="logo" src="%(logo)s" style="width:300px;height:300px">
  <div>
    <div style="font-size:34px;letter-spacing:.28em;text-transform:uppercase" class="gold">Hợp tác xã · Vũ Lăng, Lạng Sơn</div>
    <div class="serif" style="font-size:118px;line-height:1.05;margin:12px 0 16px">Thế Hưng Organic</div>
    <div style="font-size:42px;color:#efe6d3">Tinh Bột Sắn Dây · Cam Đường Canh VietGAP</div>
  </div>
</div>"""),
 # 7) Ảnh bìa Zalo — Zalo cắt khác nhau theo máy, nên dồn hết nội dung vào giữa
 "bia-zalo-1280x720": (1280, 720, """
<div class="bg" style="background-image:url('%(vung)s')"></div>
<div class="shade" style="background:radial-gradient(ellipse at center,rgba(10,8,6,.8) 0%%,rgba(10,8,6,.62) 55%%,rgba(10,8,6,.3) 100%%)"></div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
  <img class="logo" src="%(logo)s" style="width:150px;height:150px">
  <div class="serif" style="font-size:72px;line-height:1.05;margin:20px 0 12px">Thế Hưng Organic</div>
  <div style="font-size:28px;color:#efe6d3">Tinh Bột Sắn Dây · Cam Đường Canh VietGAP</div>
  <div style="font-size:24px;margin-top:16px" class="gold">Zalo 0979 502 000 · thehungorganic.com</div>
</div>"""),
 # 8) Shopee — banner vòng xoay 1: Tinh Bột Sắn Dây
 "shopee-vong-xoay-1-2000x1000": (2000, 1000, """
<div class="bg" style="background-image:url('%(ngang)s')"></div>
<div class="shade" style="background:linear-gradient(90deg,rgba(10,8,6,.9) 0%%,rgba(10,8,6,.75) 45%%,rgba(10,8,6,.1) 85%%)"></div>
<div style="position:absolute;left:110px;top:0;bottom:0;width:1050px;display:flex;flex-direction:column;justify-content:center">
  <img class="logo" src="%(logo)s" style="width:140px;height:140px">
  <div style="font-size:34px;letter-spacing:.24em;text-transform:uppercase;margin-top:34px" class="gold">Từ nương núi đá Bắc Sơn</div>
  <div class="serif" style="font-size:120px;line-height:1.04;margin:14px 0 22px">Tinh Bột Sắn Dây<br><span class="gold">trắng tự nhiên</span></div>
  <div style="font-size:40px;color:#efe6d3">Lọc tay · Sấy lò · Không tẩy trắng · Không phụ gia</div>
  <div style="margin-top:44px"><span class="pill" style="padding:18px 38px;font-size:42px">Túi 0,5kg <b class="gold">%(p05)s</b> · 1kg <b class="gold">%(p1)s</b></span></div>
</div>"""),
 # 9) Shopee — banner vòng xoay 2: túi lớn cho quán / mua sỉ (giá chưa chốt -> nhắn báo giá)
 "shopee-vong-xoay-2-2000x1000": (2000, 1000, """
<div class="bg" style="background-image:url('%(nuong)s')"></div>
<div class="shade" style="background:linear-gradient(90deg,rgba(10,8,6,.1) 15%%,rgba(10,8,6,.78) 52%%,rgba(10,8,6,.92) 100%%)"></div>
<div style="position:absolute;right:110px;top:0;bottom:0;width:980px;display:flex;flex-direction:column;justify-content:center">
  <div style="font-size:34px;letter-spacing:.24em;text-transform:uppercase" class="gold">Cho quán chè · nhà hàng · đại lý</div>
  <div class="serif" style="font-size:112px;line-height:1.05;margin:16px 0 24px">Túi lớn<br><span class="gold">5kg · 10kg</span></div>
  <div style="font-size:40px;color:#efe6d3;line-height:1.45">Cùng mẻ bột nhà làm, đóng túi lớn<br>cho quán dùng hằng ngày</div>
  <div style="margin-top:46px;display:flex;gap:28px;align-items:center">
    <span class="btn" style="padding:24px 44px;font-size:40px">Nhắn shop báo giá</span>
    <span style="font-size:34px;color:#cfc4ac">Zalo 0979 502 000</span>
  </div>
</div>"""),
 # 10) Bài đăng dọc 4:5 (Instagram / Facebook) — Sắn dây
 "bai-doc-san-day-1080x1350": (1080, 1350, """
<div class="bg" style="background-image:url('%(doc)s')"></div>
<div class="shade" style="background:linear-gradient(180deg,rgba(10,8,6,.45) 0%%,rgba(10,8,6,.1) 28%%,rgba(10,8,6,.85) 58%%,rgba(10,8,6,.97) 100%%)"></div>
<img class="logo" src="%(logo)s" style="position:absolute;left:64px;top:60px;width:124px;height:124px">
<div style="position:absolute;left:68px;right:68px;bottom:72px">
  <div style="font-size:27px;letter-spacing:.24em;text-transform:uppercase" class="gold">Nhà làm · Bắc Sơn, Lạng Sơn</div>
  <div class="serif" style="font-size:92px;line-height:1.05;margin:16px 0 20px">Một ly sắn dây<br>đúng vị quê</div>
  <div style="font-size:32px;color:#efe6d3;line-height:1.45">Củ đào trên nương núi đá, lọc tay nhiều lượt,<br>sấy lò. Không tẩy trắng, không phụ gia.</div>
  <div style="display:flex;align-items:center;justify-content:space-between;margin-top:40px">
    <div class="pill" style="padding:14px 28px;font-size:32px">Chỉ từ <b class="gold">%(p05)s</b></div>
    <div class="btn" style="padding:20px 34px;font-size:30px">thehungorganic.com</div>
  </div>
</div>"""),
 # 11) Story dọc — Quà Tết (giá gói quà chưa chốt -> nhắn báo giá)
 "story-qua-tet-1080x1920": (1080, 1920, """
<div class="bg" style="background-image:url('%(camhero)s');background-position:72%% center"></div>
<div class="shade" style="background:linear-gradient(180deg,rgba(10,8,6,.82) 0%%,rgba(10,8,6,.3) 22%%,rgba(10,8,6,.15) 38%%,rgba(10,8,6,.9) 62%%,rgba(10,8,6,.97) 100%%)"></div>
<div style="position:absolute;top:120px;left:0;right:0;text-align:center">
  <img class="logo" src="%(logo)s" style="width:150px;height:150px">
  <div style="font-size:30px;letter-spacing:.24em;text-transform:uppercase;margin-top:22px" class="gold">Hợp tác xã Thế Hưng Organic</div>
</div>
<div style="position:absolute;left:70px;right:70px;bottom:150px;text-align:center">
  <div style="font-size:34px;letter-spacing:.2em;text-transform:uppercase" class="gold">Tết Đinh Mùi 2027</div>
  <div class="serif" style="font-size:104px;line-height:1.05;margin:18px 0 30px">Quà Tết<br><span class="gold">từ vườn nhà</span></div>
  <div style="font-size:36px;color:#efe6d3;line-height:1.5">Cam Đường Canh VietGAP + Tinh Bột Sắn Dây<br>Gói nhỏ · Gói lớn · Quà biếu công ty</div>
  <div class="btn" style="margin-top:50px;padding:28px 48px;font-size:40px">Nhắn báo giá &amp; đặt trước</div>
  <div style="font-size:32px;color:#cfc4ac;margin-top:30px">thehungorganic.com · Zalo 0979 502 000</div>
</div>"""),
 # 12) Ảnh chia sẻ link trang Sắn Dây
 "og-san-day-1200x630": (1200, 630, """
<div class="bg" style="background-image:url('%(ngang)s')"></div>
<div class="shade" style="background:linear-gradient(90deg,rgba(10,8,6,.9) 0%%,rgba(10,8,6,.72) 50%%,rgba(10,8,6,.1) 100%%)"></div>
<div style="position:absolute;left:70px;top:0;bottom:0;width:760px;display:flex;flex-direction:column;justify-content:center">
  <img class="logo" src="%(logo)s" style="width:96px;height:96px">
  <div style="font-size:22px;letter-spacing:.24em;text-transform:uppercase;margin-top:24px" class="gold">Từ nương núi đá Bắc Sơn</div>
  <div class="serif" style="font-size:70px;line-height:1.05;margin:12px 0 16px">Tinh Bột Sắn Dây<br><span class="gold">trắng tự nhiên</span></div>
  <div style="font-size:26px;color:#efe6d3">Lọc tay · Sấy lò · Không tẩy trắng</div>
  <div style="margin-top:26px"><span class="pill" style="padding:12px 26px;font-size:26px">Túi 0,5kg <b class="gold">%(p05)s</b> · 1kg <b class="gold">%(p1)s</b></span></div>
</div>"""),
 # 13) Ảnh chia sẻ link trang Cam
 "og-cam-1200x630": (1200, 630, """
<div class="bg" style="background-image:url('%(camhero)s')"></div>
<div class="shade" style="background:linear-gradient(90deg,rgba(10,8,6,.9) 0%%,rgba(10,8,6,.7) 50%%,rgba(10,8,6,.05) 100%%)"></div>
<div style="position:absolute;left:70px;top:0;bottom:0;width:760px;display:flex;flex-direction:column;justify-content:center">
  <img class="logo" src="%(logo)s" style="width:96px;height:96px">
  <div style="font-size:22px;letter-spacing:.24em;text-transform:uppercase;margin-top:24px" class="gold">Vườn đạt VietGAP · Lạng Sơn</div>
  <div class="serif" style="font-size:70px;line-height:1.05;margin:12px 0 16px">Cam Đường Canh<br><span class="gold">chín trên cây</span></div>
  <div style="font-size:26px"><span class="star">★★★★★</span> %(rating)s/5 · %(reviews)s đánh giá Shopee</div>
  <div style="margin-top:26px"><span class="pill" style="padding:12px 26px;font-size:26px">Thùng 5kg <b class="gold">%(c5)s</b> · 10kg <b class="gold">%(c10)s</b></span></div>
</div>"""),
 # 14) Ảnh chia sẻ link các bài cẩm nang
 "og-cam-nang-1200x630": (1200, 630, """
<div class="bg" style="background-image:url('%(doc)s');background-position:center 60%%"></div>
<div class="shade" style="background:linear-gradient(90deg,rgba(10,8,6,.9) 0%%,rgba(10,8,6,.72) 55%%,rgba(10,8,6,.15) 100%%)"></div>
<div style="position:absolute;left:70px;top:0;bottom:0;width:760px;display:flex;flex-direction:column;justify-content:center">
  <img class="logo" src="%(logo)s" style="width:96px;height:96px">
  <div style="font-size:22px;letter-spacing:.24em;text-transform:uppercase;margin-top:24px" class="gold">Cẩm nang nhà làm</div>
  <div class="serif" style="font-size:70px;line-height:1.05;margin:12px 0 16px">Sắn dây &amp; cam<br><span class="gold">dùng sao cho ngon</span></div>
  <div style="font-size:26px;color:#efe6d3">Cách pha, công thức chè, phân biệt thật giả</div>
</div>"""),
}

def vnd(n):
    return f"{n:,}".replace(",", ".") + "đ"

def main():
    prods = json.load(open(ROOT / "data" / "products.json", encoding="utf-8"))["products"]
    price = {v["package"]: v["price_vnd"] for p in prods for v in p["variants"]}
    logo = (ROOT / "content" / "kenh_assets" / "logo-tron" / "logo-tron-bieu-tuong-1080.png").resolve().as_uri()  # logo vừa khung tròn
    vals = dict(logo=logo, suong=u("v2/vung-suong-2000.webp"), sdhero=u("sp/sd-hero.jpg"), camhero=u("sp/cam-hero.jpg"), ngang=(HERE / "anh" / "nuong-nui-da-ngang.jpg").as_uri(), doc=(HERE / "anh" / "nuong-nui-da-doc.jpg").as_uri(), vung=u("home/vung-19.jpg"), nuong=u("home/hero-1920.jpg"),
                bot=u("home/sp-san-day.jpg"), cam=u("sp/cam-story.jpg"), rating=RATING, reviews=REVIEWS,
                p05=vnd(price["túi 0.5kg"]), p1=vnd(price["túi 1kg"]),
                c5=vnd(price["thùng 5kg"]), c10=vnd(price["thùng 10kg"]))
    prof = Path(tempfile.gettempdir()) / "thoc-banner-chrome"
    for name, (w, h, body) in BANNERS.items():
        if len(sys.argv) > 1 and sys.argv[1] not in name:
            continue
        html = f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE % dict(w=w, h=h)}</style></head><body>{body % vals}</body></html>"
        src = HERE / f"_{name}.html"
        src.write_text(html, encoding="utf-8")
        out = HERE / f"{name}.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                        f"--user-data-dir={prof}", f"--window-size={w},{h}", f"--screenshot={out}",
                        "--virtual-time-budget=3000", src.as_uri()], capture_output=True, timeout=300)
        src.unlink()
        print(("OK  " if out.exists() else "LỖI ") + out.name)

if __name__ == "__main__":
    main()
