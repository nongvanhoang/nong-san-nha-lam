// Dựng phần "câu chuyện sản xuất khi cuộn" (ảnh ghim + đổi theo từng bước) cho 6 trang VI/EN.
// Sửa chữ/ảnh ở đây rồi chạy lại: node scripts/tao_cau_chuyen_cuon.mjs  (ảnh nằm ở docs/assets/story/).
import fs from 'node:fs';
import path from 'node:path';

const DOCS = path.join(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1')), '..', 'docs');

const SD = [
  { img: 'sd1', vi: ['Trồng giữa núi đá', 'Dây leo phủ kín giàn trên nương Vũ Lăng, củ lớn dần dưới lớp đất đỏ.', 'Nương sắn dây xanh dưới núi đá vôi'],
    en: ['Grown among limestone hills', 'Vines climb the trellis while the roots grow underground.', 'Kudzu field below limestone hills'] },
  { img: 'sd2', vi: ['Đào cả gốc củ', 'Củ to chắc, đưa về xưởng ngay trong ngày.', 'Củ sắn dây vừa đào đặt lên cân'],
    en: ['Whole roots dug up', 'Brought to the workshop the same day.', 'Freshly dug kudzu root on a scale'] },
  { img: 'sd3', vi: ['Rửa sạch, nghiền', 'Rửa hết đất cát, nghiền nát, ép lấy nước bột.', 'Rửa củ sắn dây bằng vòi nước'],
    en: ['Washed and ground', 'Pressed for the starch milk.', 'Washing kudzu roots with a hose'] },
  { img: 'sd4', vi: ['Lọc và lắng nhiều lượt', 'Khuấy, để lắng, thay nước, lọc lại đến khi bột trắng trong.', 'Lọc bột sắn dây bằng tay trong chậu'],
    en: ['Filtered and settled', 'Many times, until pure and white.', 'Hand-filtering kudzu starch in a basin'] },
  { img: 'sd5', vi: ['Sấy lò nhiều tầng', 'Nhiệt độ cài sẵn, khô đều, không phụ thuộc nắng mưa.', 'Xếp khay bột vào lò sấy nhiều tầng'],
    en: ['Kiln-dried', 'A preset temperature dries it evenly, rain or shine.', 'Loading trays into a multi-level drying kiln'] },
  { img: 'sd6', vi: ['Ra lò là đóng túi', 'Đóng ngay khi bột vừa khô, giữ trọn màu trắng tự nhiên.', 'Tinh bột sắn dây vừa khô được đóng túi'],
    en: ['Bagged from the kiln', 'Keeping its natural white color.', 'Freshly dried kudzu starch in bags'] },
];
const CAM = [
  { img: 'cam1', vi: ['Ra nụ đầu mùa', 'Cây bắt đầu ra những nụ hoa nhỏ xíu.', 'Nụ hoa cam đầu mùa'],
    en: ['First buds', 'The trees put out tiny flower buds.', 'Early-season orange buds'] },
  { img: 'cam2', vi: ['Hoa nở trắng vườn', 'Hoa cam nở, thơm dịu mỗi sáng.', 'Hoa cam nở trắng'],
    en: ['Blossom', 'White blossoms, gently fragrant every morning.', 'White orange blossom'] },
  { img: 'cam3', vi: ['Đậu quả non', 'Hoa rụng, quả non lớn dần qua nhiều tháng.', 'Quả cam non trên cành'],
    en: ['Young fruit', 'Petals fall and the fruit grows for months.', 'Young green fruit on the branch'] },
  { img: 'cam4', vi: ['Chín tự nhiên trên cây', 'Không thúc chín, đợi đủ ngày quả mới vàng và ngọt.', 'Cam chín vàng trên cây'],
    en: ['Ripened on the tree', "No ripening agents: we wait until it's ready.", 'Ripe mandarins on the tree'] },
  { img: 'cam5', vi: ['Hái tay đúng mùa', 'Khoảng tháng 11 âm lịch đến tháng 1, hái từng quả.', 'Hái cam bằng tay trong vườn dưới chân núi'],
    en: ['Hand-picked in season', 'Around November to January (lunar calendar), fruit by fruit.', 'Hand-picking mandarins below the hills'] },
  { img: 'cam6', vi: ['Phân loại, đóng thùng', 'Xếp cẩn thận trong ngày, gửi đi khắp cả nước.', 'Thùng Cam Đường Canh đầy quả vừa hái'],
    en: ['Sorted and boxed', 'Packed with care the same day, shipped across Vietnam.', 'A box of freshly picked mandarins'] },
];

const pad = n => String(n).padStart(2, '0');
function chapter({ cls, id, lang, pre, kick, title, lead, steps, tag, more }) {
  const beats = steps.map((s, i) => {
    const [h, p, alt] = s[lang], src = `${pre}assets/story/${s.img}`;
    return `          <li class="beat"><figure><img src="${src}-1080.webp" srcset="${src}-640.webp 640w, ${src}-1080.webp 1080w" sizes="(max-width:900px) 100vw, 560px" alt="${alt}" width="1080" height="1350" loading="lazy"></figure><div class="txt"><span class="n">${pad(i + 1)}</span><h4>${h}</h4><p>${p}</p></div></li>\n`;
  }).join('');
  const link = more ? `\n      <p class="ch-more"><a class="btn ${more[2] || ''}" href="${more[0]}">${more[1]} →</a></p>` : '';
  return `  <div class="ch ${cls}" aria-labelledby="${id}">
    <div class="wrap">
      <div class="ch-head"><span class="k rise">${kick}</span><${tag} id="${id}" class="rise">${title}</${tag}><p class="rise">${lead}</p></div>
      <div class="sc">
        <div class="stage"></div>
        <ol class="beats">
${beats}        </ol>
      </div>${link}
    </div>
  </div>
`;
}
const head = (h, p) => `    <div class="wrap">
      <div class="head">
        <h2 id="t-qt" class="rise">${h}</h2>
        <p class="rise">${p}</p>
      </div>
    </div>
`;

const pages = [
  { file: 'index.html', start: '  <section class="story" id="quy-trinh"', end: '  <section class="revs"',
    html: `  <section class="story" id="quy-trinh" aria-labelledby="t-qt">
${head('Cách chúng tôi làm', 'Cuộn chậm để đi cùng hợp tác xã: từ nương ra túi bột, từ nụ hoa tới thùng cam. Ảnh chụp thật tại vườn và xưởng.')}${chapter({ cls: 'ch-sd', id: 't-ch1', lang: 'vi', pre: '', kick: 'Chương 1 · Làm quanh năm', title: 'Tinh Bột Sắn Dây', lead: 'Sáu bước từ nương đá vôi Vũ Lăng tới túi bột trắng trong bếp nhà bạn.', steps: SD, tag: 'h3', more: ['san-day.html', 'Xem Tinh Bột Sắn Dây', 'light'] })}${chapter({ cls: 'ch-cam', id: 't-ch2', lang: 'vi', pre: '', kick: 'Chương 2 · Tháng 11 tới tháng 1 âm lịch', title: 'Cam Đường Canh', lead: 'Một năm chờ trên cây, chỉ hái khi quả đã đủ ngày.', steps: CAM, tag: 'h3', more: ['cam-duong-canh.html', 'Xem Cam Đường Canh'] })}  </section>

` },
  { file: 'san-day.html', start: '  <section id="quy-trinh"', end: '  <section class="info" id="video"',
    html: `  <section class="story solo" id="quy-trinh" aria-labelledby="t-qt">
${chapter({ cls: 'ch-sd', id: 't-qt', lang: 'vi', pre: '', kick: 'Quy trình · 6 bước', title: '6 bước, làm thật, không đi tắt', lead: 'Toàn bộ ảnh chụp tại nương và xưởng của hợp tác xã ở xã Vũ Lăng. Cuộn chậm để xem từng bước.', steps: SD, tag: 'h2', more: ['dat-truoc.html?chon=sd1', 'Đặt Tinh Bột Sắn Dây', 'light'] })}  </section>

` },
  { file: 'cam-duong-canh.html', start: '  <section class="info" aria-labelledby="t-mc">', end: '  <section aria-labelledby="t-co">',
    html: `  <section class="story solo" id="quy-trinh" aria-labelledby="t-mc">
${chapter({ cls: 'ch-cam', id: 't-mc', lang: 'vi', pre: '', kick: 'Một mùa cam · 6 bước', title: 'Từ nụ hoa đến thùng cam trên tay bạn', lead: 'Ảnh chụp thật trong vườn: cây được để ra hoa, đậu quả và chín theo đúng mùa. Cuộn chậm để xem từng bước.', steps: CAM, tag: 'h2', more: ['dat-truoc.html?chon=cam10', 'Đặt trước Cam Đường Canh'] })}  </section>

` },
  { file: 'en/index.html', start: '  <section id="process"', end: '  <section class="revs" id="reviews"',
    html: `  <section class="story" id="process" aria-labelledby="t-qt">
${head('How we make it', 'Scroll slowly to follow the cooperative from field to bag, and from blossom to box. Every photo was taken in our own fields and workshop.')}${chapter({ cls: 'ch-sd', id: 't-ch1', lang: 'en', pre: '../', kick: 'Chapter 1 · Made year-round', title: 'Kudzu Root Starch', lead: 'Six steps from the limestone hills of Vu Lang to the bag in your kitchen.', steps: SD, tag: 'h3', more: ['san-day.html', 'See Kudzu Root Starch', 'light'] })}${chapter({ cls: 'ch-cam', id: 't-ch2', lang: 'en', pre: '../', kick: 'Chapter 2 · Harvest Nov–Jan (lunar calendar)', title: 'Canh Mandarin Oranges', lead: 'A full year on the tree, picked only when the fruit is ready. Sold within Vietnam only.', steps: CAM, tag: 'h3', more: ['cam-duong-canh.html', 'See Canh Mandarins'] })}  </section>

` },
  { file: 'en/san-day.html', start: '  <section aria-labelledby="t-qt">', end: '  <section class="revs" id="export"',
    html: `  <section class="story solo" id="process" aria-labelledby="t-qt">
${chapter({ cls: 'ch-sd', id: 't-qt', lang: 'en', pre: '../', kick: 'Process · 6 steps', title: 'Six steps, done properly', lead: "Every photo was taken in the cooperative's own fields and workshop in Vu Lang commune. Scroll slowly to see each step.", steps: SD, tag: 'h2' })}  </section>

` },
  { file: 'en/cam-duong-canh.html', start: '  <section class="info" aria-labelledby="t-mc">', end: '  <section class="land"',
    html: `  <section class="story solo" id="process" aria-labelledby="t-mc">
${chapter({ cls: 'ch-cam', id: 't-mc', lang: 'en', pre: '../', kick: 'One season · 6 steps', title: 'From blossom to the box in your hands', lead: 'Real photos from the orchard: the trees flower, set fruit and ripen in their own time. Scroll slowly to see each step.', steps: CAM, tag: 'h2' })}  </section>

` },
];

for (const p of pages) {
  const f = path.join(DOCS, p.file);
  let s = fs.readFileSync(f, 'utf8');
  // lần chạy lại: phần đã dựng bắt đầu bằng <section class="story ...
  let a = s.indexOf('  <section class="story');
  if (a < 0) a = s.indexOf(p.start);
  const b = s.indexOf(p.end, a + 1);
  if (a < 0 || b < 0) throw new Error(`${p.file}: không tìm thấy chỗ chèn`);
  s = s.slice(0, a) + p.html + s.slice(b);
  const pre = p.file.startsWith('en/') ? '../' : '';
  const tag = `<script src="${pre}assets/story.js"></script>`;
  if (!s.includes(tag)) s = s.replace(`<script src="${pre}assets/track.js"></script>`, `<script src="${pre}assets/track.js"></script>\n${tag}`);
  fs.writeFileSync(f, s);
  console.log('ok', p.file);
}
