// Tạo nhãn OCOP từ nhãn 500g gốc: giữ logo + QR, viết lại phần chữ, thêm ô logo OCOP.
const fs = require('fs');
const dir = process.argv[2];
const src = fs.readFileSync(dir + '/nhan-say-day-500g.svg', 'utf8');

const logo = src.slice(src.indexOf('  <!-- Logo bản nền'), src.indexOf('  <!-- Tên sản phẩm'));
const qr = src.slice(src.indexOf('  <!-- QR thật'), src.lastIndexOf('</svg>'));
const bg = src.slice(src.indexOf('  <rect'), src.indexOf('  <!-- Logo bản nền'));

const PH = '#a3361f'; // màu đỏ gạch cho chỗ cần điền — đổi về #3a2f18 khi điền thật
const t = (y, s, extra = '') =>
  `  <text x="52" y="${y}" font-family="Arial, sans-serif" font-size="2.3" fill="#3a2f18"${extra}>${s}</text>`;

function body(weight) {
  return `  <!-- Tên sản phẩm + thương hiệu -->
  <text x="52" y="13" font-family="Cambria, Georgia, serif" font-weight="500" font-size="6.4" letter-spacing="0.3" fill="#2e4630">TINH BỘT SẮN DÂY</text>
  <text x="52" y="19" font-family="Cambria, Georgia, serif" font-style="italic" font-size="3.2" letter-spacing="0.3" fill="#5b4a2a">Nông Sản Nhà Làm &#183; Lạng Sơn &#183; Zalo 0979 502 000</text>
  <line x1="52" y1="22" x2="136" y2="22" stroke="#2e4630" stroke-width="0.25" opacity="0.55"/>

  <!-- Ô LOGO OCOP: thay bằng file logo OCOP chính thức + đúng số sao trên giấy chứng nhận (không tự vẽ logo) -->
  <g>
    <circle cx="149" cy="11.5" r="8.3" fill="none" stroke="${PH}" stroke-width="0.35" stroke-dasharray="1,0.8"/>
    <text x="149" y="10.3" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="2.6" fill="${PH}">OCOP</text>
    <text x="149" y="13.6" text-anchor="middle" font-family="Arial, sans-serif" font-size="2.6" fill="${PH}">&#9733;&#9733;&#9733;</text>
    <text x="149" y="16.4" text-anchor="middle" font-family="Arial, sans-serif" font-size="1.5" fill="${PH}">[DÁN LOGO THẬT]</text>
  </g>

  <!-- Thông tin bắt buộc (giữ trong khổ x=52..138 để không đụng mã QR) -->
${t(26.2, `<tspan font-weight="700">Khối lượng tịnh: ${weight}</tspan> &#183; 100% tinh bột sắn dây, không phụ gia`)}
${t(29.4, 'Bảo quản nơi khô ráo, thoáng mát. Không thay thuốc chữa bệnh.')}
${t(32.6, `NSX, HSD, số lô: xem tem mặt sau &#183; Số tự công bố: <tspan fill="${PH}">[SỐ TCB]</tspan>`)}
${t(35.8, `Chịu trách nhiệm: <tspan fill="${PH}">[TÊN CÔNG TY]</tspan>`)}
${t(39.0, `Địa chỉ: <tspan fill="${PH}">[ĐỊA CHỈ CÔNG TY THEO GPKD]</tspan>`)}
${t(42.2, 'Sản xuất tại: Thôn Nam Hương, xã Vũ Lăng, tỉnh Lạng Sơn')}

`;
}

function label(weight, w, h) {
  const s = w / 160;
  const inner = bg + logo + body(weight) + qr +
    `  <text x="149" y="43.4" text-anchor="middle" font-family="Arial, sans-serif" font-size="1.7" fill="#3a2f18">Quét xem nguồn gốc</text>\n`;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}mm" height="${h}mm" viewBox="0 0 ${w} ${h}">
  <!-- Hướng 1 - Mộc & Thật, BẢN OCOP (soạn 2026-10-10). Chữ màu đỏ gạch = chỗ cần điền trước khi in -->
  <!-- Sản phẩm: Tinh Bột Sắn Dây - ${weight} -->
<g transform="scale(${s})">
${inner}</g>
</svg>
`;
}

// QR gốc nằm ở y=25..41; dời lên 1 chút để có chỗ cho dòng "Quét xem nguồn gốc"
const fix = (svg) => svg.replace('<svg x="141" y="25"', '<svg x="141" y="24.5"').replace(/<text[^>]*>Quét mã<\/text>\n?/, '');

fs.writeFileSync(dir + '/nhan-say-day-1kg-ocop.svg', fix(label('1kg', 160, 45)));
fs.writeFileSync(dir + '/nhan-say-day-500g-ocop.svg', fix(label('500g', 160, 45)));
// Gói dùng thử: túi nhỏ hơn (~13cm ngang) nên thu nhỏ đúng tỷ lệ còn 130 x 36.6mm
fs.writeFileSync(dir + '/nhan-say-day-250g-ocop.svg', fix(label('250g', 130, 36.5625)));

// Tem phụ mặt sau 50 x 32mm: mã vạch + QR truy xuất + NSX/HSD/lô đóng dấu tay
const tem = `<svg xmlns="http://www.w3.org/2000/svg" width="50mm" height="32mm" viewBox="0 0 50 32">
  <!-- Tem phụ mặt sau, dùng chung cho 250g / 500g / 1kg (soạn 2026-10-10) -->
  <rect x="0" y="0" width="50" height="32" rx="1.5" fill="#f4ead7"/>
  <rect x="0.6" y="0.6" width="48.8" height="30.8" rx="1.2" fill="none" stroke="#3e2e10" stroke-width="0.25" opacity="0.5"/>

  <!-- Ô MÃ VẠCH: thay bằng mã vạch thật (GS1 Việt Nam cấp cho công ty) -->
  <rect x="3" y="3" width="26" height="15" fill="none" stroke="${PH}" stroke-width="0.3" stroke-dasharray="1,0.8"/>
  <text x="16" y="10" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="2.4" fill="${PH}">MÃ VẠCH</text>
  <text x="16" y="13" text-anchor="middle" font-family="Arial, sans-serif" font-size="1.6" fill="${PH}">893 xxxx xxxxx</text>

  <!-- Ô QR TRUY XUẤT: thay bằng QR của hệ thống truy xuất nguồn gốc tỉnh/công ty dùng -->
  <rect x="32" y="3" width="15" height="15" fill="none" stroke="${PH}" stroke-width="0.3" stroke-dasharray="1,0.8"/>
  <text x="39.5" y="10" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="2" fill="${PH}">QR</text>
  <text x="39.5" y="12.6" text-anchor="middle" font-family="Arial, sans-serif" font-size="1.4" fill="${PH}">truy xuất</text>
  <text x="39.5" y="20.2" text-anchor="middle" font-family="Arial, sans-serif" font-size="1.6" fill="#3a2f18">Truy xuất nguồn gốc</text>

  <!-- Đóng dấu tay theo từng mẻ -->
  <line x1="3" y1="21.8" x2="47" y2="21.8" stroke="#3e2e10" stroke-width="0.2" opacity="0.5"/>
  <text x="3" y="25" font-family="Arial, sans-serif" font-size="2.2" fill="#3a2f18">NSX: ___/___/______     Lô: ________</text>
  <text x="3" y="28.6" font-family="Arial, sans-serif" font-size="2.2" fill="#3a2f18">HSD: 12 tháng kể từ ngày sản xuất</text>
</svg>
`;
fs.writeFileSync(dir + '/tem-phu-mat-sau.svg', tem);
console.log('ok');
