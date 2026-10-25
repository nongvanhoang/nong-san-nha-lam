/* Dùng chung cho trang Sắn Dây / Cam: menu đổ bóng, hiện dần, ảnh xem lớn, nút phát video, giỏ hàng +/- sang phiếu đặt hàng. */
(function(){
  var nav = document.getElementById('nav');
  function onScroll(){ if (nav) nav.classList.toggle('scrolled', scrollY > 8); }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  var els = [].slice.call(document.querySelectorAll('.rise'));
  if ('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -6% 0px' });
    els.forEach(function(el, i){ if (!el.style.getPropertyValue('--i')) el.style.setProperty('--i', i % 3); io.observe(el); });
  } else els.forEach(function(el){ el.classList.add('in'); });

  // ảnh xem lớn
  var big = document.querySelector('.gallery .big img');
  [].slice.call(document.querySelectorAll('.thumbs button')).forEach(function(b, _, all){
    b.addEventListener('click', function(){
      all.forEach(function(x){ x.setAttribute('aria-pressed', 'false'); });
      b.setAttribute('aria-pressed', 'true');
      big.style.opacity = '.3';
      var img = new Image();
      img.onload = function(){ big.src = b.dataset.src; big.alt = b.dataset.alt || ''; big.style.opacity = '1'; };
      img.src = b.dataset.src;
    });
  });

  // video: nút phát riêng
  [].slice.call(document.querySelectorAll('.player')).forEach(function(pl){
    var v = pl.querySelector('video'), btn = pl.querySelector('.play');
    if (btn) btn.addEventListener('click', function(){ v.controls = true; v.play(); pl.classList.add('playing'); });
  });

  // giỏ hàng
  var bar = document.getElementById('bar');
  var rows = [].slice.call(document.querySelectorAll('.var[data-id]')), qty = {};
  if (!bar) return;
  var hero = document.querySelector('.pmain') || document.querySelector('.hero');
  var past = false;
  function update(){ bar.classList.toggle('show', bar.classList.contains('has-items') || (past && innerWidth <= 900)); }
  if (hero && 'IntersectionObserver' in window){ new IntersectionObserver(function(e){ past = !e[0].isIntersecting; update(); }, { threshold: 0.05 }).observe(hero); }
  if (!rows.length) return;
  var sum = bar.querySelector('.sum'), go = bar.querySelector('.go'), buyGo = document.getElementById('buyGo');
  var buyLabel = buyGo ? buyGo.textContent : '';
  function vnd(n){ return n.toLocaleString('vi-VN') + 'đ'; }
  function render(){
    var n = 0, t = 0, ask = false, parts = [];
    rows.forEach(function(r){ var id = r.dataset.id, q = qty[id] || 0; r.querySelector('output').textContent = q; r.classList.toggle('on', q > 0); if (q){ n += q; if (r.dataset.price) t += q * Number(r.dataset.price); else ask = true; parts.push(id + ':' + q); } });
    bar.classList.toggle('has-items', n > 0);
    var money = t ? vnd(t) + (ask ? ' + báo giá' : '') : 'báo giá sau';
    sum.innerHTML = n ? (n + ' món · <b>' + money + '</b> <span style="opacity:.75">(chưa gồm ship)</span>') : '';
    var href = 'dat-truoc.html' + (parts.length ? '?chon=' + parts.join(',') : (buyGo ? '?chon=' + buyGo.dataset.def : ''));
    go.href = href;
    if (buyGo){ buyGo.href = href; buyGo.textContent = n ? ('Đặt ' + n + ' món · ' + money) : buyLabel; }
    update();
  }
  rows.forEach(function(r){ r.querySelectorAll('button').forEach(function(b){ b.addEventListener('click', function(){
    var id = r.dataset.id; qty[id] = Math.max(0, Math.min(50, (qty[id] || 0) + Number(b.dataset.d))); render();
    var o = r.querySelector('output'); o.classList.remove('pop'); void o.offsetWidth; o.classList.add('pop');
  }); }); });
  render();
})();
