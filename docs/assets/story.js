/* Câu chuyện sản xuất khi cuộn: ảnh ghim lại, đổi theo từng bước, phóng nhẹ theo vị trí cuộn. */
(function(){
  var scs = [].slice.call(document.querySelectorAll('.sc'));
  if (!scs.length) return;
  var still = matchMedia('(prefers-reduced-motion: reduce)');
  function clamp(x){ return x < 0 ? 0 : x > 1 ? 1 : x; }
  function pad(n){ return (n < 10 ? '0' : '') + n; }

  var list = scs.map(function(sc){
    var stage = sc.querySelector('.stage'), beats = [].slice.call(sc.querySelectorAll('.beat'));
    var frame = document.createElement('div'); frame.className = 'frame';
    var imgs = beats.map(function(b){ var im = b.querySelector('img').cloneNode(); frame.appendChild(im); return im; });
    var meta = document.createElement('div'); meta.className = 'meta'; meta.setAttribute('aria-hidden', 'true');
    meta.innerHTML = '<span class="cnt"><b>01</b> / ' + pad(beats.length) + '</span><span class="lbl"></span><span class="pbar"><i></i></span>';
    stage.appendChild(frame); stage.appendChild(meta);
    return { sc: sc, frame: frame, imgs: imgs, beats: beats, cnt: meta.querySelector('b'), lbl: meta.querySelector('.lbl'), fill: meta.querySelector('i'), cur: -1 };
  });

  function show(s, a){
    if (a === s.cur) return;
    if (s.cur >= 0){ s.imgs[s.cur].classList.remove('on'); s.imgs[s.cur].style.transform = ''; s.beats[s.cur].classList.remove('on'); }
    s.imgs[a].classList.add('on'); s.beats[a].classList.add('on');
    s.cnt.textContent = pad(a + 1); s.lbl.textContent = s.beats[a].querySelector('h4').textContent;
    s.cur = a;
  }

  var ticking = false;
  function tick(){
    ticking = false;
    var vh = innerHeight, line = vh * (innerWidth <= 900 ? .74 : .55), calm = still.matches;
    list.forEach(function(s){
      var r = s.sc.getBoundingClientRect();
      if (r.bottom < -vh || r.top > 2 * vh) return;
      var a = 0;
      s.beats.forEach(function(b, i){ if (b.getBoundingClientRect().top < line) a = i; });
      show(s, a);
      s.fill.style.transform = 'scaleX(' + clamp((line - r.top) / r.height) + ')';
      if (calm) return;
      var br = s.beats[a].getBoundingClientRect();
      s.imgs[a].style.transform = 'scale(' + (1.12 - .12 * clamp((line - br.top) / br.height)).toFixed(4) + ')';
      // khung ảnh mở rộng dần khi chương vừa cuộn tới
      s.frame.style.setProperty('--e', clamp((r.top - vh * .1) / (vh * .6)).toFixed(3));
    });
  }
  function req(){ if (!ticking){ ticking = true; requestAnimationFrame(tick); } }
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', req);
  req();
})();

/* Video ngắn tự chạy (không tiếng) khi cuộn tới; bật giảm chuyển động thì hiện nút phát thay vì tự chạy. */
(function(){
  var vs = [].slice.call(document.querySelectorAll('video[data-loop]'));
  if (!vs.length) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)){
    vs.forEach(function(v){ v.controls = true; });
    return;
  }
  var io = new IntersectionObserver(function(es){
    es.forEach(function(e){ if (e.isIntersecting) e.target.play().catch(function(){}); else e.target.pause(); });
  }, { threshold: .35 });
  vs.forEach(function(v){ io.observe(v); });
})();
