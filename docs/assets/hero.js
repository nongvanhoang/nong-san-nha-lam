(function(){
  "use strict";

  var CFG = window.HERO_CONFIG || {};
  var VIDEO_URL = CFG.videoUrl;
  var VIDEO_BYTES = CFG.videoBytes;
  var POSTER_URL = CFG.posterUrl;
  var hasHero = !!VIDEO_URL;

  /* ---------------- Word/character split (seeded, load-once) ---------------- */
  function rng(seed){ let s = seed >>> 0; return function(){ s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }

  function splitWords(el, entrance, seed){
    const text = el.textContent;
    el.setAttribute('aria-label', text);
    el.textContent = '';
    const words = text.split(' ');
    const rand = rng(seed);
    words.forEach(function(word, i){
      if (i > 0) el.appendChild(document.createTextNode(' '));
      const span = document.createElement('span');
      span.className = 'w ' + entrance;
      span.textContent = word;
      const th = (i / words.length) * 0.7 + rand() * 0.08;
      span.style.setProperty('--th', th.toFixed(3));
      span.setAttribute('aria-hidden', 'true');
      el.appendChild(span);
    });
  }

  const splitTargets = document.querySelectorAll('.split-target');
  let seedCounter = 7;
  splitTargets.forEach(function(el){
    const entrance = el.getAttribute('data-entrance') || 'rise';
    if (entrance === 'blur'){
      const text = el.textContent;
      el.innerHTML = '';
      el.setAttribute('aria-label', text);
      const soft = document.createElement('span');
      soft.className = 'soft-copy';
      soft.textContent = text;
      soft.setAttribute('aria-hidden', 'true');
      const sharp = document.createElement('span');
      sharp.className = 'sharp-copy';
      sharp.textContent = text;
      sharp.setAttribute('aria-hidden', 'true');
      el.appendChild(soft);
      el.appendChild(sharp);
    } else {
      splitWords(el, entrance, seedCounter++);
    }
  });

  if (!hasHero){
    /* Page has no scroll hero (e.g. the home page) — still run below-fold choreography. */
    initRevealAndPause();
    return;
  }

  /* ---------------- Band ranges & the drive loop ---------------- */
  const bandEls = Array.prototype.slice.call(document.querySelectorAll('[data-band]'));
  const bands = bandEls.map(function(el){
    const range = el.getAttribute('data-range').split(',').map(Number);
    return { el: el, a: range[0], b: range[1], op: -1, k: -1 };
  });

  function smoothstep(p, e0, e1){
    const t = Math.min(1, Math.max(0, (p - e0) / (e1 - e0)));
    return t * t * (3 - 2 * t);
  }

  const settleBtns = document.getElementById('settleBtns');
  let lastKB = -1;
  const pageLoadStart = performance.now();
  function loadRamp(){
    const t = Math.min(1, (performance.now() - pageLoadStart) / 900);
    return t * t * (3 - 2 * t);
  }

  function updateCaptions(p){
    bands.forEach(function(band, idx){
      const a = band.a, b = band.b;
      const f = Math.min(0.02, (b - a) / 3);
      let opacity;
      if (idx === 0){
        opacity = 1 - smoothstep(p, b - f, b);
      } else if (idx === bands.length - 1){
        opacity = smoothstep(p, a, a + f);
      } else {
        opacity = smoothstep(p, a, a + f) * (1 - smoothstep(p, b - f, b));
      }
      const ramp = Math.min(0.025, (b - a) * 0.35);
      let k = Math.min(1, Math.max(0, (p - a) / ramp));
      if (idx === 0) k = Math.max(k, loadRamp());
      const rOp = Math.round(opacity * 1000) / 1000;
      const rK = Math.round(k * 1000) / 1000;
      if (rOp !== band.op){
        band.el.style.opacity = rOp;
        band.op = rOp;
      }
      if (rK !== band.k){
        band.el.style.setProperty('--k', rK);
        band.k = rK;
      }
    });

    const settleBand = bands[bands.length - 1];
    if (settleBand){
      const p2 = settleBand.k;
      const ks = Math.min(1, Math.max(0, (p2 - 0.5) * 3));
      const kb = Math.min(1, Math.max(0, (p2 - 0.68) * 4));
      const rKs = Math.round(ks * 1000) / 1000;
      const rKb = Math.round(kb * 1000) / 1000;
      const subEl = settleBand.el.querySelector('p');
      if (subEl){
        const cur = subEl.style.getPropertyValue('--ks-cache');
        if (cur !== String(rKs)){
          subEl.style.opacity = rKs;
          subEl.style.setProperty('--ks-cache', rKs);
        }
      }
      const markEl = settleBand.el.querySelector('.brand-mark');
      if (markEl){
        const cur = markEl.style.getPropertyValue('--kc-cache');
        if (cur !== String(rKs)){
          markEl.style.opacity = rKs;
          markEl.style.setProperty('--kc-cache', rKs);
        }
      }
      if (settleBtns && rKb !== lastKB){
        settleBtns.style.opacity = rKb;
        lastKB = rKb;
      }
    }

    const cue = document.getElementById('scrollCue');
    if (cue){
      const cueOp = 1 - smoothstep(p, 0, 0.08);
      cue.style.opacity = cueOp;
    }
  }

  /* ---------------- Hero progress ---------------- */
  const heroStage = document.getElementById('heroStage');
  const heroPin = document.querySelector('.hero-pin');
  const video = document.getElementById('heroVideo');
  let heroOnScreen = false;
  const io = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){ heroOnScreen = entry.isIntersecting; if (heroOnScreen) armLoop(); });
  }, { threshold: 0 });
  io.observe(heroPin);

  function heroProgress(){
    const rect = heroPin.getBoundingClientRect();
    const total = heroPin.offsetHeight - window.innerHeight;
    if (total <= 0) return 0;
    const scrolled = -rect.top;
    return Math.min(1, Math.max(0, scrolled / total));
  }

  /* ---------------- Gated seeks ---------------- */
  let seekBusy = false;
  let pendingTime = null;
  function requestSeek(t){
    if (!video.duration) return;
    if (seekBusy){ pendingTime = t; return; }
    seekBusy = true;
    video.currentTime = t;
  }
  video.addEventListener('seeked', function(){
    seekBusy = false;
    if (pendingTime !== null){
      const t = pendingTime; pendingTime = null; requestSeek(t);
    }
  });
  video.addEventListener('error', function(){ seekBusy = false; pendingTime = null; });

  /* ---------------- Lerp loop ---------------- */
  let target = 0, shown = 0, rafId = null, lastTick = 0;
  function tick(now){
    const dt = Math.min(100, now - (lastTick || now));
    lastTick = now;
    const k = 0.16;
    shown += (target - shown) * (1 - Math.pow(1 - k, dt / 16.667));
    const stillLoading = (now - pageLoadStart) < 950;
    if (Math.abs(target - shown) < 0.0005 && !stillLoading){
      shown = target; rafId = null; lastTick = 0;
    } else {
      rafId = requestAnimationFrame(tick);
    }
    if (video.duration) requestSeek(shown * video.duration);
    updateCaptions(shown);
  }
  function onScroll(){
    target = heroProgress();
    if (rafId === null && heroOnScreen) rafId = requestAnimationFrame(tick);
  }
  function armLoop(){
    if (rafId === null) rafId = requestAnimationFrame(tick);
  }

  /* ---------------- Streamed Blob loader with loading ring ---------------- */
  const ring = document.getElementById('ldRing');
  const posterLayer = document.getElementById('heroPoster');

  let started = false;
  function startBlobFetch(){
    if (started) return;
    started = true;
    loadHeroBlob().catch(failVideo);
  }
  let heroInited = false;
  function initHeroOnce(){
    if (heroInited) return;
    heroInited = true;
    posterLayer.style.backgroundImage = "url('" + POSTER_URL + "')";
    const posterImg = new Image();
    posterImg.onload = startBlobFetch;
    posterImg.onerror = startBlobFetch;
    posterImg.src = POSTER_URL;
    setTimeout(startBlobFetch, 4000);
  }

  async function loadHeroBlob(){
    const ctrl = new AbortController();
    let watchdog = setTimeout(function(){ ctrl.abort(); }, 20000);
    const res = await fetch(VIDEO_URL, { signal: ctrl.signal });
    const total = Number(res.headers.get('Content-Length')) || VIDEO_BYTES;
    const reader = res.body.getReader();
    const chunks = [];
    let got = 0, lastRing = 0;
    for (;;){
      const { done, value } = await reader.read();
      if (done) break;
      clearTimeout(watchdog);
      watchdog = setTimeout(function(){ ctrl.abort(); }, 20000);
      chunks.push(value);
      got += value.length;
      const frac = Math.min(1, got / total);
      const now = performance.now();
      if (now - lastRing > 100 || frac === 1){
        lastRing = now;
        ring.style.setProperty('--ld', Math.round(126 * (1 - frac)));
      }
    }
    clearTimeout(watchdog);
    ring.style.setProperty('--ld', 0);
    video.src = URL.createObjectURL(new Blob(chunks));
    video.load();
    video.addEventListener('canplay', function(){
      requestSeek(heroProgress() * video.duration);
      heroStage.classList.add('video-ready');
    }, { once: true });
  }

  function failVideo(){
    heroStage.classList.add('video-failed');
  }
  video.addEventListener('error', failVideo);

  /* ---------------- The five static-hero gates ---------------- */
  const GATES = [
    '(max-width: 720px)',
    '(orientation: portrait) and (max-width: 1024px)',
    '(orientation: portrait) and (pointer: coarse)',
    '(orientation: landscape) and (pointer: coarse) and (max-height: 560px)',
    '(prefers-reduced-motion: reduce)'
  ];
  let scrubOn = false;
  function pinToFinalStates(){
    bands.forEach(function(band){
      band.el.style.opacity = (band === bands[bands.length - 1]) ? 1 : 0;
      band.el.style.setProperty('--k', 1);
    });
    if (settleBtns) settleBtns.style.opacity = 1;
    const subEl = bands[bands.length - 1].el.querySelector('p');
    if (subEl) subEl.style.opacity = 1;
    const markEl = bands[bands.length - 1].el.querySelector('.brand-mark');
    if (markEl) markEl.style.opacity = 1;
  }
  function unpinFinalStates(){
    bands.forEach(function(band){ band.op = -1; band.k = -1; });
    lastKB = -1;
  }
  function enableScrub(){
    scrubOn = true;
    document.body.classList.remove('static-mode');
    initHeroOnce();
    addEventListener('scroll', onScroll, { passive: true });
    unpinFinalStates();
    updateCaptions(heroProgress());
    onScroll();
  }
  function disableScrub(){
    scrubOn = false;
    document.body.classList.add('static-mode');
    removeEventListener('scroll', onScroll);
    if (rafId !== null){ cancelAnimationFrame(rafId); rafId = null; }
  }
  function applyHeroMode(){
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (GATES.some(function(q){ return matchMedia(q).matches; })){
      disableScrub();
      if (reduced) pinToFinalStates();
    } else {
      enableScrub();
    }
  }
  const MQLS = GATES.map(function(q){ return matchMedia(q); });
  MQLS.forEach(function(m){ m.addEventListener('change', applyHeroMode); });
  applyHeroMode();

  initRevealAndPause();

  function initRevealAndPause(){
    const revealEls = document.querySelectorAll('.reveal, .reveal-stagger');
    const revealIO = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if (entry.isIntersecting){
          entry.target.classList.add('in');
          revealIO.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(function(el){ revealIO.observe(el); });

    document.addEventListener('visibilitychange', function(){
      document.body.classList.toggle('paused', document.hidden);
    });
  }
})();
