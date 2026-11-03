/* Đếm lượt xem trang + lượt bấm Zalo / Gọi / Đặt hàng / Gửi phiếu bằng GoatCounter (miễn phí, không cookie).
   Chưa điền GC thì file này không làm gì cả. Điền tên tài khoản GoatCounter (vd "thoc" cho thoc.goatcounter.com). */
(function(){
  var GC = "thehungorganic";
  window.thocTrack = function(name){
    try { if (window.goatcounter && goatcounter.count) goatcounter.count({ path: name, title: name, event: true }); } catch(e){}
  };
  if (!GC) return;
  var s = document.createElement("script");
  s.async = true;
  s.src = "https://gc.zgo.at/count.js";
  s.setAttribute("data-goatcounter", "https://" + GC + ".goatcounter.com/count");
  document.head.appendChild(s);

  // Tự đếm các nút liên hệ / đặt hàng trên mọi trang
  document.addEventListener("click", function(e){
    var a = e.target.closest && e.target.closest("a");
    if (!a) return;
    var h = a.getAttribute("href") || "";
    var page = location.pathname.split("/").pop() || "index.html";
    if (h.indexOf("zalo.me") > -1) thocTrack("bam-zalo/" + page);
    else if (h.indexOf("wa.me") > -1) thocTrack("bam-whatsapp/" + page);
    else if (h.indexOf("mailto:") === 0) thocTrack("bam-email/" + page);
    else if (h.indexOf("tel:") === 0) thocTrack("bam-goi/" + page);
    else if (h.indexOf("dat-truoc.html") > -1) thocTrack("bam-dat-hang/" + page);
    else if (h.indexOf("shopee.vn") > -1) thocTrack("bam-shopee/" + page);
  }, true);

  // Đếm lượt bấm xem video + lượt xem gần hết (≥75%), mỗi video 1 lần/lượt tải trang.
  // Bỏ qua video nền tự chạy (aria-hidden) — chỉ đếm video khách tự bấm.
  function vname(v){
    var src = v.currentSrc || v.getAttribute("src") || "";
    return src.split("/").pop().replace(/\.mp4.*$/, "");
  }
  document.addEventListener("play", function(e){
    var v = e.target;
    if (!v || v.tagName !== "VIDEO" || v.getAttribute("aria-hidden") === "true" || v._thocPlay) return;
    v._thocPlay = true;
    thocTrack("xem-video/" + vname(v));
  }, true);
  document.addEventListener("timeupdate", function(e){
    var v = e.target;
    if (!v || v.tagName !== "VIDEO" || !v._thocPlay || v._thocDone || !v.duration) return;
    if (v.currentTime / v.duration >= 0.75) { v._thocDone = true; thocTrack("xem-het-video/" + vname(v)); }
  }, true);
})();
