// Bao bì Tinh Bột Sắn Dây THOC — bản in sạch (soạn 2026-10-25).
// Lấy hình (lá, củ, núi) từ thiết kế gốc qua scripts/tao_bao_bi_anh.py, toàn bộ CHỮ gõ lại cho đúng dấu,
// bỏ chữ không chứng minh được ("ORGANIC", "tốt cho sức khỏe"), thêm đủ thông tin bắt buộc trên nhãn.
// Chạy: node scripts/tao_bao_bi.js   → content/nhan_bao_bi/bao-bi-moi/{pdf,png}/
// Chữ màu ĐỎ trong khung nét đứt = chỗ còn thiếu giấy tờ thật (số tự công bố, mã vạch) — điền rồi chạy lại.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'content/nhan_bao_bi/bao-bi-moi');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PROFILE = path.join(process.env.TEMP || OUT, 'thoc-bao-bi-chrome');
const url = (p) => 'file:///' + p.replace(/\\/g, '/');
const IMG = (n) => url(path.join(OUT, 'anh', n + '.png'));
const LOGO = url(path.join(ROOT, 'docs/assets/logo-thoc.jpg'));
const LOGO_TRON = url(path.join(ROOT, 'content/kenh_assets/logo-tron/logo-tron-day-du-1080.png'));

// Điền khi có giấy thật. Để null = in ô đỏ nhắc điền.
const SO_TCB = null;      // số tự công bố sản phẩm
const MA_VACH = null;     // đã có mã vạch GS1 chưa

const qrSrc = fs.readFileSync(path.join(ROOT, 'content/nhan_bao_bi/nhan-say-day-500g.svg'), 'utf8');
const QR = qrSrc.match(/<path d="(M2,2H3[^"]+)"/)[1];
const qr = `<svg class="qr" viewBox="0 0 37 37"><rect width="37" height="37" fill="#fff"/><path d="${QR}" fill="#000"/></svg>`;

const ICON = {
  la: '<path d="M12 21v-9M12 14C12 9.5 9 7 4 7c0 4.5 3 7 8 7zM12 11.5c0-4.5 3-7.5 8-7.5 0 4.5-3 7.5-8 7.5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
  khong: '<circle cx="12" cy="12" r="7.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M6.8 17.2 17.2 6.8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
  giot: '<path d="M12 3.5c3 4 5.5 7 5.5 10a5.5 5.5 0 0 1-11 0c0-3 2.5-6 5.5-10z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M5 19 19 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
  nui: '<path d="M2.5 19.5 9 8.5l4 6 2.5-3.5 6 8.5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><circle cx="17" cy="6" r="2" fill="currentColor"/>',
  coc: '<path d="M5 9h11v5a5 5 0 0 1-5 5h-1a5 5 0 0 1-5-5zM16 10.5h1.5a2.5 2.5 0 0 1 0 5H16M9 3.5c-1 1.2 1 2 0 3.3M12.5 3.5c-1 1.2 1 2 0 3.3" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
  bat: '<path d="M3.5 11h17a8.5 7 0 0 1-17 0zM9 20h6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 7.5c.8-1.5 2-1.5 2.8 0M13.2 7.5c.8-1.5 2-1.5 2.8 0" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
  banh: '<path d="M4 15h16v4H4zM6 15V11h12v4M9 11V8M12 11V7M15 11V8" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
  sua: '<path d="M7 4h10l-1.3 16H8.3zM7.6 10h8.8" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
  tay: '<path d="M7 13V6.5a1.5 1.5 0 0 1 3 0V12M10 11V5a1.5 1.5 0 0 1 3 0v6M13 11V6a1.5 1.5 0 0 1 3 0v7c0 4-2.5 7-6 7s-5-2-6.5-5L3 13.5a1.4 1.4 0 0 1 2.3-1.6L7 14" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
};
const ic = (k) => `<svg viewBox="0 0 24 24">${ICON[k]}</svg>`;

const CSS = `
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact;font-family:"Be Vietnam Pro",Arial,sans-serif;color:#1d3b1f}
.page{position:relative;overflow:hidden;width:var(--w);height:var(--h);container-type:size;background:var(--bg)}
.abs{position:absolute}
img{display:block}
.g{color:#1f5124}.br{background:#7a2c12}
.script{font-family:"Dancing Script",cursive;font-weight:700;line-height:1}
.ph{color:#c0281b;border:.25cqw dashed #c0281b;padding:0 .8cqw;border-radius:.6cqw;font-weight:700}
svg{display:block}
`;

const brush = (fill) => `<svg class="abs" style="inset:0" viewBox="0 0 400 40" preserveAspectRatio="none"><path fill="${fill}" d="M6 7 30 4l40 2 60-3 70 2 70-2 60 3 52-1 14 4-6 6 7 5-5 7 6 6-10 4-48-2-70 3-64-2-70 3-58-2-40 2-28-3-8-5 6-6-7-6 5-6z"/></svg>`;

// ---------- MẶT TRƯỚC (túi đứng + bao dệt) ----------
function front({ weight, sack }) {
  const bg = sack ? '#ffffff' : '#f5f1e2';
  const logo = sack
    ? `<img class="abs" src="${LOGO_TRON}" style="left:37cqw;top:3cqw;width:26cqw">`
    : `<img class="abs" src="${LOGO}" style="left:30.5cqw;top:6cqw;width:39cqw;mix-blend-mode:multiply">`;
  const feats = [['khong', 'KHÔNG CHẤT<br>BẢO QUẢN'], ['giot', 'KHÔNG<br>PHỤ GIA'], ['la', 'KHÔNG<br>TẨY TRẮNG']];
  const info = sack ? `
  <div class="abs" style="left:6cqw;right:6cqw;bottom:3.2cqw;color:#fff;font-size:1.75cqw;line-height:1.5;font-weight:500">
    <b>Chịu trách nhiệm:</b> Hợp tác xã Thế Hưng Organic · Thôn Liên Lạc, xã Vũ Lăng, tỉnh Lạng Sơn<br>
    <b>Sản xuất tại:</b> Thôn Nam Hương, xã Vũ Lăng, tỉnh Lạng Sơn · <b>Xuất xứ:</b> Việt Nam · <b>Thành phần:</b> 100% tinh bột sắn dây<br>
    <b>Bảo quản:</b> nơi khô ráo, thoáng mát, tránh ánh nắng · <b>Số tự công bố:</b> ${SO_TCB || '<span class="ph" style="border-color:#ffb3a8;color:#ffd0c8">[SỐ TCB]</span>'}<br>
    <b>NSX · HSD · Số lô:</b> xem dấu in trên bao · Zalo 0979 502 000 · nongsannhalam.com
  </div>` : '';
  return `<div class="page" style="--bg:${bg}">
  ${sack ? '' : `<img class="abs" src="${IMG('la-goc-trai')}" style="left:-2cqw;top:-2cqw;width:27cqw">`}
  ${sack ? '' : `<img class="abs" src="${IMG('la-goc-phai')}" style="right:-2cqw;top:-2cqw;width:22cqw">`}
  ${logo}

  <!-- dải đeo góc phải -->
  <div class="abs" style="right:${sack ? 6 : 7}cqw;top:0;width:15cqw;height:27cqw;background:#1f5124;clip-path:polygon(0 0,100% 0,100% 100%,50% 88%,0 100%);color:#fff;text-align:center;padding-top:4cqw">
    <div style="width:6cqw;height:6cqw;margin:0 auto;color:#fff">${ic('la')}</div>
    <div style="font-weight:900;font-size:5cqw;line-height:1.05;margin-top:.6cqw">100%</div>
    <div style="font-weight:700;font-size:1.8cqw;line-height:1.45;margin-top:.4cqw">TINH BỘT<br>SẮN DÂY<br>NGUYÊN CHẤT</div>
  </div>

  <!-- tên sản phẩm -->
  <div class="abs g" style="left:0;right:0;top:${sack ? 28 : 33.5}cqw;text-align:center;font-weight:900;line-height:1.12;letter-spacing:-.02em">
    <div style="font-size:9.5cqw">TINH BỘT</div>
    <div style="font-size:16.5cqw;margin-top:5cqw">SẮN DÂY</div>
  </div>
  <div class="abs" style="left:9cqw;right:9cqw;top:${sack ? 62 : 67.5}cqw;height:7.4cqw">
    ${brush('#7a2c12')}
    <div class="abs" style="inset:0;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:3.3cqw;white-space:nowrap">LỌC TAY · SẤY LÒ · KHÔNG TẨY TRẮNG</div>
  </div>
  <div class="abs g" style="left:0;right:0;top:${sack ? 69.6 : 76.3}cqw;text-align:center;font-weight:700;font-size:3.3cqw">Từ vùng đồi Bắc Sơn – Lạng Sơn</div>

  <!-- hình -->
  ${sack ? '' : `<img class="abs" src="${IMG('nui-doi')}" style="left:24cqw;top:80cqw;width:80cqw">`}
  <img class="abs" src="${IMG('cu-va-bot')}" style="left:${sack ? 30 : 31}cqw;top:${sack ? 75 : 83}cqw;width:${sack ? 58 : 60}cqw">

  <!-- 3 cam kết -->
  <div class="abs" style="left:5cqw;top:${sack ? 74.5 : 82.5}cqw;width:22cqw;display:grid;gap:${sack ? 0.6 : 1.6}cqw;text-align:center">
    ${feats.map(([k, t]) => `<div><div class="g" style="width:${sack ? 7 : 8.5}cqw;height:${sack ? 7 : 8.5}cqw;margin:0 auto;border:.5cqw solid #1f5124;border-radius:50%;padding:${sack ? 1.2 : 1.5}cqw;background:${bg}">${ic(k)}</div><div class="g" style="font-weight:800;font-size:2cqw;line-height:1.38;margin-top:.7cqw">${t}</div></div>`).join('')}
  </div>

  <!-- sóng xanh dưới -->
  <svg class="abs" style="left:0;bottom:0;width:100cqw;height:${sack ? 37 : 23}cqw" viewBox="0 0 100 25" preserveAspectRatio="none">
    <path d="M0 6C22 0 38 2 56 8S88 13 100 5V25H0z" fill="#1f5124"/>
    <path d="M0 6C22 0 38 2 56 8S88 13 100 5" fill="none" stroke="#7fb24a" stroke-width=".6"/>
  </svg>
  <div class="abs script" style="left:6cqw;bottom:${sack ? 20 : 5}cqw;color:#fff;font-size:${sack ? 5.6 : 6.4}cqw;line-height:1.05">Tinh hoa<br>núi rừng Bắc Sơn</div>
  <div class="abs" style="right:6cqw;bottom:${sack ? 19 : 4}cqw;background:#f5f1e2;border:.5cqw solid #c9b98f;border-radius:2.4cqw;padding:1.4cqw 3cqw;text-align:center;color:#1d3b1f">
    <div style="font-weight:600;font-size:2.2cqw">Khối lượng tịnh</div>
    <div style="font-weight:900;font-size:${weight.length > 4 ? 7.6 : 8.6}cqw;line-height:1">${weight}</div>
  </div>
  ${info}
</div>`;
}

// ---------- MẶT SAU (túi đứng) ----------
function back({ weight }) {
  const four = [['la', '100%<br>SẮN DÂY'], ['giot', 'KHÔNG<br>PHỤ GIA'], ['khong', 'KHÔNG<br>TẨY TRẮNG'], ['nui', 'NGUỒN GỐC<br>BẮC SƠN']];
  const uses = [['coc', 'Pha uống', 'Hoà bột với nước lạnh trước, rồi rót nước sôi, khuấy đến khi trong'], ['bat', 'Nấu chè', 'Tạo độ sánh cho chè đậu xanh, chè hạt sen'], ['banh', 'Làm bánh', 'Trộn cùng bột gạo, bột năng cho bánh dẻo trong'], ['sua', 'Đồ uống', 'Pha cùng sữa, nước cốt chanh, nước ép']];
  return `<div class="page" style="--bg:#f5f1e2">
  <img class="abs" src="${IMG('la-goc-trai')}" style="left:-3cqw;top:-3cqw;width:24cqw">
  <div class="abs script g" style="right:7cqw;top:6cqw;font-size:6.6cqw;transform:rotate(-8deg);transform-origin:right top;text-align:right;line-height:1.15">Từ núi rừng Bắc Sơn<br>đến căn bếp mọi nhà</div>

  <img class="abs" src="${IMG('nui-doi')}" style="left:0;top:24cqw;width:100cqw">
  <svg class="abs" style="left:0;top:38cqw;width:100cqw;height:10cqw" viewBox="0 0 100 10" preserveAspectRatio="none">
    <path d="M0 5C25 -1 45 2 62 7S88 9 100 4V10H0z" fill="#f5f1e2"/>
    <path d="M0 5C25 -1 45 2 62 7S88 9 100 4" fill="none" stroke="#5f9a3a" stroke-width=".7"/>
  </svg>
  <img class="abs" src="${IMG('dong-cu')}" style="right:-1cqw;top:40cqw;width:38cqw">

  <div class="abs g" style="left:7cqw;top:43cqw;font-weight:900;font-size:7cqw;line-height:1.45">TINH BỘT<br>SẮN DÂY</div>
  <p class="abs" style="left:7cqw;top:63.5cqw;width:58cqw;font-size:2.4cqw;line-height:1.5;color:#2b3a2c;font-weight:500">
    Củ sắn dây vùng đồi Bắc Sơn, Lạng Sơn, xay nhỏ, lọc nước nhiều lần bằng tay rồi sấy khô trong lò.
    Không tẩy trắng, không phụ gia — chỉ có tinh bột sắn dây nguyên chất.</p>

  <div class="abs" style="left:6cqw;right:6cqw;top:80cqw;display:grid;grid-template-columns:repeat(4,1fr);text-align:center">
    ${four.map(([k, t], i) => `<div style="${i ? 'border-left:.3cqw solid #b9c4a9;' : ''}padding:0 1cqw"><div class="g" style="width:9cqw;height:9cqw;margin:0 auto;border:.5cqw solid #1f5124;border-radius:50%;padding:1.7cqw">${ic(k)}</div><div class="g" style="font-weight:800;font-size:2.05cqw;line-height:1.4;margin-top:.8cqw">${t}</div></div>`).join('')}
  </div>

  <div class="abs" style="left:6cqw;right:6cqw;top:95.8cqw;display:grid;grid-template-columns:2.15fr 1fr;gap:2cqw">
    <div style="border:.4cqw solid #1f5124;border-radius:2cqw;overflow:hidden;background:#fbf9f1">
      <div style="background:#1f5124;color:#fff;font-weight:800;font-size:2.7cqw;padding:1cqw 2.2cqw">HƯỚNG DẪN SỬ DỤNG</div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);padding:1.2cqw .6cqw">
        ${uses.map(([k, h, t], i) => `<div style="${i ? 'border-left:.25cqw solid #c9cfbd;' : ''}padding:0 1cqw;text-align:center"><div class="g" style="width:5.5cqw;height:5.5cqw;margin:0 auto">${ic(k)}</div><div class="g" style="font-weight:800;font-size:2cqw;margin-top:.6cqw">${h}</div><div style="font-size:1.55cqw;line-height:1.3;margin-top:.3cqw;color:#2b3a2c">${t}</div></div>`).join('')}
      </div>
    </div>
    <div style="border:.4cqw solid #1f5124;border-radius:2cqw;overflow:hidden;background:#fbf9f1;font-size:1.85cqw;line-height:1.4">
      <div style="background:#1f5124;color:#fff;font-weight:800;font-size:2.4cqw;padding:1cqw 1.8cqw">THÀNH PHẦN</div>
      <div style="padding:.9cqw 1.8cqw;font-weight:600">100% tinh bột sắn dây nguyên chất</div>
      <div style="background:#1f5124;color:#fff;font-weight:800;font-size:2.4cqw;padding:1cqw 1.8cqw">BẢO QUẢN</div>
      <div style="padding:.9cqw 1.8cqw">Nơi khô ráo, thoáng mát, tránh ánh nắng. Đậy kín sau khi dùng.</div>
    </div>
  </div>

  <!-- thông tin bắt buộc -->
  <div class="abs" style="left:6cqw;right:6cqw;bottom:3cqw;height:22.6cqw;background:#fff;border:.3cqw solid #c9b98f;border-radius:2cqw;padding:1.8cqw 2.2cqw;display:grid;grid-template-columns:1fr auto auto;gap:2.2cqw;align-items:center">
    <div style="font-size:1.72cqw;line-height:1.5;color:#22301f">
      <b>Khối lượng tịnh: ${weight}</b> · Xuất xứ: Việt Nam<br>
      <b>Chịu trách nhiệm:</b> Hợp tác xã Thế Hưng Organic<br>
      Địa chỉ: Thôn Liên Lạc, xã Vũ Lăng, tỉnh Lạng Sơn<br>
      Sản xuất tại: Thôn Nam Hương, xã Vũ Lăng, tỉnh Lạng Sơn<br>
      Số tự công bố: ${SO_TCB || '<span class="ph">[SỐ TCB]</span>'} · Zalo 0979 502 000 · nongsannhalam.com
      <div style="margin-top:1cqw;border:.25cqw solid #8a7c55;border-radius:1cqw;padding:.6cqw 1.2cqw;font-weight:700;display:flex;gap:4cqw">
        <span>NSX:</span><span>HSD:</span><span>Số lô:</span>
      </div>
    </div>
    <div style="width:15.5cqw;height:15.5cqw;${MA_VACH ? '' : 'border:.3cqw dashed #c0281b;'}display:flex;align-items:center;justify-content:center;text-align:center;font-size:1.6cqw;color:#c0281b;font-weight:700">${MA_VACH ? '' : 'MÃ VẠCH<br>(GS1)'}</div>
    <div style="text-align:center;font-size:1.4cqw;font-weight:600">${qr.replace('class="qr"', 'style="width:14cqw;height:14cqw"')}<div style="margin-top:.5cqw">Quét xem nguồn gốc</div></div>
  </div>
</div>`;
}

const DESIGNS = [
  // tên file, khổ (mm) rộng × cao, nội dung
  ['tui-500g-mat-truoc', 160, 240, () => front({ weight: '500g' })],
  ['tui-500g-mat-sau', 160, 240, () => back({ weight: '500g' })],
  ['tui-1kg-mat-truoc', 200, 300, () => front({ weight: '1kg' })],
  ['tui-1kg-mat-sau', 200, 300, () => back({ weight: '1kg' })],
  ['bao-5kg', 350, 525, () => front({ weight: '5kg', sack: true })],
  ['bao-10kg', 400, 600, () => front({ weight: '10kg', sack: true })],
];

for (const d of ['html', 'pdf', 'png']) fs.mkdirSync(path.join(OUT, d), { recursive: true });
const only = process.argv[2];
// Máy yếu (4GB RAM): Chrome thỉnh thoảng tự thoát giữa chừng → thử lại tối đa 3 lần
const run = (args) => { for (let i = 1; ; i++) { try { return execFileSync(CHROME, args, { stdio: 'ignore' }); } catch (e) { if (i >= 3) throw e; } } };
for (const [name, w, h, make] of DESIGNS) {
  if (only && !name.includes(only)) continue;
  const html = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>${name}</title>
<link rel="stylesheet" href="../font/fonts.css"><style>@page{size:${w}mm ${h}mm;margin:0}${CSS}</style></head>
<body style="--w:${w}mm;--h:${h}mm">${make()}</body></html>`;
  const file = path.join(OUT, 'html', name + '.html');
  fs.writeFileSync(file, html);
  const common = ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', `--user-data-dir=${PROFILE}`, '--virtual-time-budget=15000'];
  run([...common, '--no-pdf-header-footer', `--print-to-pdf=${path.join(OUT, 'pdf', name + '.pdf')}`, url(file)]);
  const pxW = Math.round(w * 3.7795), pxH = Math.round(h * 3.7795);
  run([...common, `--window-size=${pxW},${pxH}`, `--force-device-scale-factor=${(1100 / pxW).toFixed(4)}`, `--screenshot=${path.join(OUT, 'png', name + '.png')}`, url(file)]);
  console.log(name, `${w}x${h}mm`);
}
