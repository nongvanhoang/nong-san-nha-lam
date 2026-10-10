const CHANNEL_LABELS = {
  facebook: "Facebook",
  zalo: "Zalo",
  shopee: "Shopee",
  lazada: "Lazada",
  tiktok: "TikTok Shop",
  offline: "Trực tiếp / offline",
};

const fmtVnd = (n) => Number(n).toLocaleString("vi-VN") + "đ";
const todayStr = () => new Date().toISOString().slice(0, 10);

let META = null;

async function api(path, options) {
  const res = await fetch(path, options);
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || "Có lỗi xảy ra");
  }
  return data;
}

// ---------- Tabs ----------
function setupTabs() {
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById("tab-" + btn.dataset.tab).classList.add("active");
      if (btn.dataset.tab === "tong-quan") loadOverview();
      if (btn.dataset.tab === "bao-cao") loadReport();
      if (btn.dataset.tab === "chi-phi") {
        loadMonthSummary();
        loadExpensesTable();
      }
      if (btn.dataset.tab === "gia-san-pham") loadProductsEditor();
      if (btn.dataset.tab === "ban-hang") {
        loadTodayPost();
        loadB2BLeads();
      }
      if (btn.dataset.tab === "media" && !MEDIA_ITEMS.length) loadMedia();
    });
  });
}

// ---------- Meta (channels/statuses/products) ----------
async function loadMeta() {
  META = await api("/api/meta");

  const productSelects = [document.getElementById("order-product"), document.getElementById("batch-product")];
  productSelects.forEach((sel) => {
    sel.innerHTML = META.product_names.map((p) => `<option value="${p}">${p}</option>`).join("");
  });

  const channelSel = document.getElementById("order-channel");
  channelSel.innerHTML = META.channels
    .map((c) => `<option value="${c}">${CHANNEL_LABELS[c] || c}</option>`)
    .join("");

  const statusSel = document.getElementById("order-status");
  statusSel.innerHTML = META.statuses
    .map((s) => `<option value="${s}">${META.status_labels[s] || s}</option>`)
    .join("");

  const expenseCategorySel = document.getElementById("expense-category");
  expenseCategorySel.innerHTML = META.expense_categories
    .map((c) => `<option value="${c}">${META.expense_category_labels[c] || c}</option>`)
    .join("");
}

// ---------- Tổng quan hôm nay ----------
async function loadOverview() {
  const data = await api("/api/today-overview");

  // Bài cần đăng hôm nay (bản rút gọn, trỏ sang tab "Bán hàng hôm nay" để đăng thật)
  const postEl = document.getElementById("overview-post-content");
  if (!data.today_post.chu_de) {
    postEl.innerHTML = `<p class="hint">Hôm nay không có bài nào đến lịch.</p>`;
  } else {
    const channelCount = Object.keys(data.today_post.channels).length;
    postEl.innerHTML = `
      <p><strong>${escapeHtml(data.today_post.chu_de)}</strong> (${channelCount} kênh)</p>
      <button type="button" class="small" id="overview-goto-post-btn">Xem & đăng →</button>
    `;
    const btn = document.getElementById("overview-goto-post-btn");
    if (btn) btn.addEventListener("click", () => document.querySelector('.tab-btn[data-tab="ban-hang"]').click());
  }

  // Hôm nay nên gọi/nhắn B2B
  const callsEl = document.getElementById("overview-calls-content");
  if (!data.today_calls.length) {
    callsEl.innerHTML = `<p class="hint">Không còn lead nào ở nhóm ưu tiên chưa liên hệ — xem toàn bộ ở tab "Bán hàng hôm nay".</p>`;
  } else {
    callsEl.innerHTML =
      data.today_calls
        .map((l) => {
          const phone = (l.SDT || "").split("/")[0].trim().replace(/[^0-9+]/g, "");
          const contactBits = [];
          if (phone) contactBits.push(`<a href="tel:${phone}">📞 ${escapeHtml(l.SDT)}</a>`);
          if (l.Email) contactBits.push(`<a href="mailto:${escapeHtml(l.Email)}">✉️ ${escapeHtml(l.Email)}</a>`);
          if (!contactBits.length) contactBits.push(`<span class="hint">— chỉ có Facebook/địa chỉ —</span>`);
          return `<p><strong>${escapeHtml(l.Ten)}</strong> (${escapeHtml(l.Nhom.split(" - ")[0])}) — ${contactBits.join(" · ")}</p>`;
        })
        .join("") + `<p class="hint">Cập nhật kết quả cuộc gọi ở tab "Bán hàng hôm nay" để lần sau không hiện lại.</p>`;
  }

  // Hạn chót sắp tới
  const deadlinesEl = document.getElementById("overview-deadlines-content");
  if (!data.deadlines.length) {
    deadlinesEl.innerHTML = `<p class="hint">Không có hạn chót nào đang theo dõi trong VIEC_CAN_LAM.md.</p>`;
  } else {
    deadlinesEl.innerHTML = data.deadlines
      .map((d) => {
        const urgent = d.days_left <= 7;
        const overdue = d.days_left < 0;
        const badge = overdue
          ? `<span class="warning-badge danger">TRỄ ${-d.days_left} ngày</span>`
          : `<span class="warning-badge${urgent ? " danger" : ""}">còn ${d.days_left} ngày</span>`;
        return `<p>${badge} ${escapeHtml(d.title)}</p>`;
      })
      .join("");
  }

  // Cảnh báo tồn kho
  const invEl = document.getElementById("overview-inventory-content");
  if (!data.inventory_warnings.length) {
    invEl.innerHTML = `<p class="hint">Không có cảnh báo tồn kho nào.</p>`;
  } else {
    invEl.innerHTML = data.inventory_warnings
      .map((i) => {
        const danger = i.warning.includes("VƯỢT");
        return `<p><span class="warning-badge${danger ? " danger" : ""}">${escapeHtml(i.warning)}</span> ${escapeHtml(i.product)} — còn ${i.remaining}</p>`;
      })
      .join("");
  }

  // Tài chính tháng này (bản rút gọn)
  const monthEl = document.getElementById("overview-month-content");
  const m = data.month;
  monthEl.innerHTML = `
    <p>Doanh thu: <strong>${fmtVnd(m.revenue)}</strong> · Chi phí: <strong>${fmtVnd(m.expenses)}</strong> · Lãi/lỗ: <strong>${fmtVnd(m.profit)}</strong></p>
    <button type="button" class="small" id="overview-goto-finance-btn">Xem chi tiết →</button>
  `;
  const financeBtn = document.getElementById("overview-goto-finance-btn");
  if (financeBtn) financeBtn.addEventListener("click", () => document.querySelector('.tab-btn[data-tab="chi-phi"]').click());

  // Khách quen lâu chưa quay lại
  const followupsEl = document.getElementById("overview-followups-content");
  if (!data.followups.length) {
    followupsEl.innerHTML = `<p class="hint">Không có khách quen nào đang chờ nhắn lại (hoặc chưa có đủ dữ liệu đơn hàng).</p>`;
  } else {
    followupsEl.innerHTML = data.followups
      .map(
        (c) =>
          `<p>${escapeHtml(c.customer)} — ${c.days_since_last_order} ngày chưa mua lại (${c.order_count} đơn trước đó, mua ${escapeHtml(c.products.join(", "))})</p>`
      )
      .join("") + `<p class="hint">Mẫu nhắn lại: content/templates/nhan_tin_truc_tiep.md (Mẫu 2).</p>`;
  }
}

// ---------- Ghi đơn hàng ----------
function setupOrderForm() {
  document.getElementById("order-date").value = todayStr();
  const form = document.getElementById("form-order");
  const msg = document.getElementById("order-msg");
  const customerInput = document.getElementById("order-customer");
  const knownHint = document.getElementById("order-customer-known");

  customerInput.addEventListener("blur", async () => {
    const name = customerInput.value.trim();
    if (!name) {
      knownHint.style.display = "none";
      return;
    }
    try {
      const c = await api(`/api/customers/lookup?name=${encodeURIComponent(name)}`);
      if (c && c.phone) {
        document.getElementById("order-phone").value = c.phone;
        document.getElementById("order-address").value = c.address || "";
        knownHint.textContent = `Khách quen — đã tự điền SĐT/địa chỉ lần trước (${c.updated_at || ""})`;
        knownHint.style.display = "block";
      } else {
        knownHint.style.display = "none";
      }
    } catch {
      knownHint.style.display = "none";
    }
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    msg.textContent = "";
    msg.className = "msg";
    const fd = new FormData(form);
    const payload = {
      date: fd.get("date"),
      customer: fd.get("customer"),
      product: fd.get("product"),
      qty: parseFloat(fd.get("qty")),
      unit: fd.get("unit"),
      unit_price: parseFloat(fd.get("unit_price")),
      channel: fd.get("channel"),
      status: fd.get("status"),
      phone: fd.get("phone"),
      address: fd.get("address"),
      note: fd.get("note"),
    };
    try {
      const result = await api("/api/orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const total = result.row.qty * result.row.unit_price_vnd;
      msg.textContent = `Đã ghi: ${result.row.customer} - ${result.row.product} = ${fmtVnd(total)}`;
      msg.classList.add("ok");
      form.reset();
      document.getElementById("order-date").value = todayStr();
      knownHint.style.display = "none";
      loadOrdersTable();
    } catch (err) {
      msg.textContent = "Lỗi: " + err.message;
      msg.classList.add("err");
    }
  });
}

async function loadOrdersTable() {
  const rows = await api("/api/orders?limit=20");
  const tbody = document.querySelector("#orders-table tbody");
  tbody.innerHTML = rows
    .map((r) => {
      const total = parseFloat(r.qty) * parseFloat(r.unit_price_vnd);
      const statusLabel = (META && META.status_labels[r.status]) || r.status;
      return `<tr>
        <td>${r.date}</td>
        <td>${r.customer}</td>
        <td>${r.product}</td>
        <td>${r.qty}${r.unit}</td>
        <td>${fmtVnd(total)}</td>
        <td>${CHANNEL_LABELS[r.channel] || r.channel}</td>
        <td>${statusLabel}</td>
      </tr>`;
    })
    .join("");
}

// ---------- Ghi mẻ sản xuất ----------
function setupBatchForm() {
  document.getElementById("batch-date").value = todayStr();
  const form = document.getElementById("form-batch");
  const msg = document.getElementById("batch-msg");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    msg.textContent = "";
    msg.className = "msg";
    const fd = new FormData(form);
    const payload = {
      date: fd.get("date"),
      product: fd.get("product"),
      quantity: parseFloat(fd.get("quantity")),
      unit: fd.get("unit"),
      batch_id: fd.get("batch_id") || null,
      note: fd.get("note"),
    };
    try {
      const result = await api("/api/batches", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      msg.textContent = `Đã ghi mẻ ${result.row.batch_id}: ${result.row.product} - ${result.row.quantity}${result.row.unit}`;
      msg.classList.add("ok");
      form.reset();
      document.getElementById("batch-date").value = todayStr();
      loadBatchesTable();
    } catch (err) {
      msg.textContent = "Lỗi: " + err.message;
      msg.classList.add("err");
    }
  });
}

async function loadBatchesTable() {
  const rows = await api("/api/batches?limit=20");
  const tbody = document.querySelector("#batches-table tbody");
  tbody.innerHTML = rows
    .map(
      (r) => `<tr>
        <td>${r.date}</td>
        <td>${r.batch_id}</td>
        <td>${r.product}</td>
        <td>${r.quantity}${r.unit}</td>
        <td>${r.note || ""}</td>
      </tr>`
    )
    .join("");
}

// ---------- Chi phí / Lãi lỗ ----------
function setupExpenseForm() {
  document.getElementById("expense-date").value = todayStr();
  const form = document.getElementById("form-expense");
  const msg = document.getElementById("expense-msg");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    msg.textContent = "";
    msg.className = "msg";
    const fd = new FormData(form);
    const payload = {
      date: fd.get("date"),
      category: fd.get("category"),
      amount: parseFloat(fd.get("amount")),
      note: fd.get("note"),
    };
    try {
      const result = await api("/api/expenses", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const label = (META && META.expense_category_labels[result.row.category]) || result.row.category;
      msg.textContent = `Đã ghi: ${label} - ${fmtVnd(result.row.amount_vnd)}`;
      msg.classList.add("ok");
      form.reset();
      document.getElementById("expense-date").value = todayStr();
      loadExpensesTable();
      loadMonthSummary();
    } catch (err) {
      msg.textContent = "Lỗi: " + err.message;
      msg.classList.add("err");
    }
  });
}

async function loadExpensesTable() {
  const rows = await api("/api/expenses?limit=20");
  const tbody = document.querySelector("#expenses-table tbody");
  tbody.innerHTML = rows
    .map((r) => {
      const label = (META && META.expense_category_labels[r.category]) || r.category;
      return `<tr>
        <td>${r.date}</td>
        <td>${label}</td>
        <td>${fmtVnd(r.amount_vnd)}</td>
        <td>${r.note || ""}</td>
      </tr>`;
    })
    .join("");
}

async function loadMonthSummary() {
  const el = document.getElementById("month-summary-content");
  const m = await api("/api/month-summary");

  const pctHtml = (actual, target) => {
    if (!target) return "";
    const pct = ((actual / target) * 100).toFixed(0);
    return ` — đã đạt ${pct}% mục tiêu (${fmtVnd(target)})`;
  };

  el.innerHTML = `
    <p class="hint">Từ ${m.since} đến hôm nay (tháng ${m.month})</p>
    <div class="report-section">
      <h3>Doanh thu</h3>
      <div class="stat-total">${fmtVnd(m.revenue)}</div>
      <p class="hint">${pctHtml(m.revenue, m.target_revenue) || "Chưa đặt mục tiêu tháng — sửa data/muc_tieu.json"}</p>
    </div>
    <div class="report-section">
      <h3>Chi phí</h3>
      <div class="stat-total">${fmtVnd(m.expenses)}</div>
    </div>
    <div class="report-section">
      <h3>Lãi/lỗ</h3>
      <div class="stat-total">${fmtVnd(m.profit)}</div>
      <p class="hint">${pctHtml(m.profit, m.target_profit)}</p>
    </div>
  `;
}

// ---------- Báo cáo ----------
function setupReportControls() {
  document.getElementById("report-days").addEventListener("change", loadReport);
}

async function loadReport() {
  const days = document.getElementById("report-days").value;
  const report = await api(`/api/report?days=${days}`);
  const el = document.getElementById("report-content");

  const revenueRows = report.revenue_by_product.length
    ? report.revenue_by_product
        .map((r) => `<tr><td>${r.product}</td><td>${r.qty}</td><td>${fmtVnd(r.revenue)}</td></tr>`)
        .join("")
    : `<tr><td colspan="3">Chưa có đơn hàng trong khoảng thời gian này</td></tr>`;

  const channelRows = report.revenue_by_channel.length
    ? report.revenue_by_channel
        .map((r) => `<tr><td>${CHANNEL_LABELS[r.channel] || r.channel}</td><td>${fmtVnd(r.revenue)}</td></tr>`)
        .join("")
    : `<tr><td colspan="2">—</td></tr>`;

  const expenseRows = report.expenses_by_category.length
    ? report.expenses_by_category.map((r) => `<tr><td>${r.label}</td><td>${fmtVnd(r.amount)}</td></tr>`).join("")
    : `<tr><td colspan="2">Chưa ghi chi phí trong khoảng thời gian này</td></tr>`;

  const productionRows = report.production.length
    ? report.production.map((r) => `<tr><td>${r.product}</td><td>${r.qty}</td></tr>`).join("")
    : `<tr><td colspan="2">Chưa có mẻ sản xuất trong khoảng thời gian này</td></tr>`;

  const inventoryRows = report.inventory.length
    ? report.inventory
        .map((r) => {
          let badge = "";
          if (r.warning) {
            const danger = r.warning.includes("VƯỢT");
            badge = `<span class="warning-badge ${danger ? "danger" : ""}">${r.warning}</span>`;
          }
          return `<tr><td>${r.product}${badge}</td><td>${r.produced}</td><td>${r.sold}</td><td>${r.remaining}</td></tr>`;
        })
        .join("")
    : `<tr><td colspan="4">Chưa có dữ liệu sản xuất/đơn hàng</td></tr>`;

  el.innerHTML = `
    <p class="hint">Từ ${report.since} đến hôm nay (${report.days} ngày)</p>

    <div class="report-section">
      <h3>Tổng doanh thu</h3>
      <div class="stat-total">${fmtVnd(report.total_revenue)}</div>
      <p class="hint">${report.order_count} đơn hàng</p>
    </div>

    <div class="report-section">
      <h3>Doanh thu theo sản phẩm</h3>
      <div class="table-wrap"><table>
        <thead><tr><th>Sản phẩm</th><th>SL bán</th><th>Doanh thu</th></tr></thead>
        <tbody>${revenueRows}</tbody>
      </table></div>
    </div>

    <div class="report-section">
      <h3>Doanh thu theo kênh</h3>
      <div class="table-wrap"><table>
        <thead><tr><th>Kênh</th><th>Doanh thu</th></tr></thead>
        <tbody>${channelRows}</tbody>
      </table></div>
    </div>

    <div class="report-section">
      <h3>Chi phí</h3>
      <div class="table-wrap"><table>
        <thead><tr><th>Hạng mục</th><th>Số tiền</th></tr></thead>
        <tbody>${expenseRows}</tbody>
      </table></div>
    </div>

    <div class="report-section">
      <h3>Lãi/lỗ trong kỳ</h3>
      <div class="stat-total">${fmtVnd(report.profit)}</div>
    </div>

    <div class="report-section">
      <h3>Sản lượng sản xuất/thu hoạch</h3>
      <div class="table-wrap"><table>
        <thead><tr><th>Sản phẩm</th><th>Sản lượng</th></tr></thead>
        <tbody>${productionRows}</tbody>
      </table></div>
    </div>

    <div class="report-section">
      <h3>Tồn kho ước tính (toàn thời gian)</h3>
      <div class="table-wrap"><table>
        <thead><tr><th>Sản phẩm</th><th>Đã làm</th><th>Đã bán</th><th>Còn lại</th></tr></thead>
        <tbody>${inventoryRows}</tbody>
      </table></div>
      <p class="hint">Số này chỉ đúng nếu luôn ghi số lượng cùng đơn vị (nên luôn quy ra kg).</p>
    </div>
  `;
}

// ---------- Giá sản phẩm ----------
async function loadProductsEditor() {
  const data = await api("/api/products");
  const el = document.getElementById("products-editor");

  el.innerHTML = data.products
    .map((p) => {
      const variantRows = p.variants
        .map(
          (v, i) => `
        <div class="variant-row">
          <span class="package-name">${v.package}</span>
          <input type="number" step="1000" data-product="${p.id}" data-package="${v.package}" value="${v.price_vnd}">
          <span>đ</span>
          <button type="button" class="small save-price-btn" data-product="${p.id}" data-package="${v.package}">Lưu</button>
        </div>`
        )
        .join("");
      return `<div class="product-block">
        <h3>${p.name}</h3>
        ${variantRows}
      </div>`;
    })
    .join("");

  el.querySelectorAll(".save-price-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const productId = btn.dataset.product;
      const pkg = btn.dataset.package;
      const input = el.querySelector(`input[data-product="${productId}"][data-package="${pkg}"]`);
      const price = parseFloat(input.value);
      btn.textContent = "...";
      try {
        await api("/api/products/price", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ product_id: productId, package: pkg, price }),
        });
        btn.textContent = "Đã lưu ✓";
        setTimeout(() => (btn.textContent = "Lưu"), 1500);
      } catch (err) {
        btn.textContent = "Lỗi";
        alert("Lỗi: " + err.message);
      }
    });
  });
}

// ---------- Bán hàng hôm nay: bài cần đăng ----------
function escapeHtml(s) {
  return (s || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

async function loadTodayPost() {
  const el = document.getElementById("today-post-content");
  el.innerHTML = "<p class=\"hint\">Đang tải...</p>";
  const data = await api("/api/today-post");

  if (!data.chu_de) {
    el.innerHTML = `<p class="hint">Hôm nay không có bài nào đến lịch trong LICH_DANG_BAI.md.</p>`;
    return;
  }

  const channelKeys = Object.keys(data.channels);
  if (!channelKeys.length) {
    el.innerHTML = `<p class="hint">Tìm thấy chủ đề "${escapeHtml(data.chu_de)}" trong lịch, nhưng chưa khớp được nội dung nào trong posts_ready.md — mở file lên tìm thủ công.</p>`;
    return;
  }

  const posted = new Set(data.posted || []);

  el.innerHTML = `
    <h3>${escapeHtml(data.chu_de)}</h3>
    ${channelKeys
      .map((ch, i) => {
        const isPosted = posted.has(ch);
        return `
      <div class="post-channel-block${isPosted ? " posted" : ""}">
        <div class="post-channel-head">
          <strong>${escapeHtml(ch)}</strong>
          <span>
            <button type="button" class="small copy-post-btn" data-idx="${i}">Copy</button>
            <button type="button" class="small mark-posted-btn" data-channel="${escapeHtml(ch)}" ${isPosted ? "disabled" : ""}>${isPosted ? "Đã đăng ✓" : "Đã đăng"}</button>
          </span>
        </div>
        <pre class="post-body" id="post-body-${i}">${escapeHtml(data.channels[ch])}</pre>
      </div>`;
      })
      .join("")}
    <p class="hint">"Đã đăng" chỉ để app tự nhớ trong ngày hôm nay — vẫn cần báo Claude để tick chính thức vào LICH_DANG_BAI.md.</p>
  `;

  el.querySelectorAll(".copy-post-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const text = document.getElementById("post-body-" + btn.dataset.idx).textContent;
      try {
        await navigator.clipboard.writeText(text);
        btn.textContent = "Đã copy ✓";
        setTimeout(() => (btn.textContent = "Copy"), 1500);
      } catch {
        alert("Không copy tự động được, hãy bôi đen và copy thủ công.");
      }
    });
  });

  el.querySelectorAll(".mark-posted-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        await api("/api/mark-posted", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ chu_de: data.chu_de, channel: btn.dataset.channel }),
        });
        btn.textContent = "Đã đăng ✓";
        btn.disabled = true;
        btn.closest(".post-channel-block").classList.add("posted");
      } catch (err) {
        alert("Lỗi: " + err.message);
      }
    });
  });
}

// ---------- Bán hàng hôm nay: danh sách khách B2B ----------
let B2B_LEADS = [];

// Thứ tự ưu tiên đúng theo Giai đoạn 0->4 trong KE_HOACH_KHAI_THAC_B2B.md — số nhỏ = làm trước.
// Nhóm không nằm trong danh sách (D, E, C, G...) coi như "chưa tới lượt", xếp cuối.
const NHOM_PRIORITY = { N: 0, B: 1, F: 1, H: 2, J: 2, K: 2, L: 3, M: 3, A: 4 };
function nhomTier(nhomFull) {
  const letter = (nhomFull || "").trim().charAt(0);
  return NHOM_PRIORITY[letter] ?? 9;
}

async function loadB2BLeads() {
  B2B_LEADS = await api("/api/b2b");
  B2B_LEADS.sort((a, b) => {
    const tierDiff = nhomTier(a.Nhom) - nhomTier(b.Nhom);
    if (tierDiff !== 0) return tierDiff;
    const aDone = a.Trang_thai && a.Trang_thai.trim() && a.Trang_thai.trim() !== "Chưa liên hệ";
    const bDone = b.Trang_thai && b.Trang_thai.trim() && b.Trang_thai.trim() !== "Chưa liên hệ";
    if (aDone !== bDone) return aDone ? 1 : -1; // chưa liên hệ lên trước
    return (parseInt(a.Uu_tien) || 9) - (parseInt(b.Uu_tien) || 9);
  });

  const nhomSel = document.getElementById("b2b-filter-nhom");
  if (nhomSel.options.length <= 1) {
    const nhoms = [...new Set(B2B_LEADS.map((l) => l.Nhom))].sort();
    nhomSel.innerHTML =
      `<option value="">Tất cả</option>` + nhoms.map((n) => `<option value="${escapeHtml(n)}">${escapeHtml(n)}</option>`).join("");
  }

  renderB2BTable();
}

function renderB2BTable() {
  const nhomFilter = document.getElementById("b2b-filter-nhom").value;
  const ttFilter = document.getElementById("b2b-filter-trangthai").value;
  const search = document.getElementById("b2b-search").value.trim().toLowerCase();

  let rows = B2B_LEADS;
  if (nhomFilter) rows = rows.filter((l) => l.Nhom === nhomFilter);
  if (ttFilter === "chua") rows = rows.filter((l) => !l.Trang_thai || l.Trang_thai.trim() === "Chưa liên hệ" || l.Trang_thai.trim() === "");
  if (ttFilter === "da") rows = rows.filter((l) => l.Trang_thai && l.Trang_thai.trim() !== "Chưa liên hệ" && l.Trang_thai.trim() !== "");
  if (ttFilter === "quantam")
    rows = rows.filter((l) => l.Trang_thai && (l.Trang_thai.includes("Đã mở") || l.Trang_thai.includes("quan tâm")));
  if (search) rows = rows.filter((l) => l.Ten.toLowerCase().includes(search));

  document.getElementById("b2b-count").textContent = `Hiện ${rows.length} / ${B2B_LEADS.length} lead — xếp theo đúng thứ tự ưu tiên Giai đoạn 0→4, chưa liên hệ lên trước`;

  const tbody = document.querySelector("#b2b-table tbody");
  tbody.innerHTML = rows
    .slice(0, 200)
    .map((l) => {
      const phone = (l.SDT || "").split("/")[0].trim().replace(/[^0-9+]/g, "");
      const contactBits = [];
      if (phone) contactBits.push(`<a href="tel:${phone}">📞 ${escapeHtml(l.SDT)}</a>`);
      if (l.Email) contactBits.push(`<a href="mailto:${escapeHtml(l.Email)}">✉️ ${escapeHtml(l.Email)}</a>`);
      if (!contactBits.length) contactBits.push("<span class=\"hint\">— chỉ có Facebook/địa chỉ —</span>");
      return `<tr>
        <td>${escapeHtml(l.Nhom.split(" - ")[0])}</td>
        <td>${escapeHtml(l.Ten)}</td>
        <td>${escapeHtml(l.Khu_vuc)}</td>
        <td>${contactBits.join("<br>")}</td>
        <td>${escapeHtml(l.Trang_thai || "Chưa liên hệ")}</td>
        <td>
          <select class="b2b-update-select" data-ten="${escapeHtml(l.Ten)}">
            <option value="" selected disabled>Cập nhật...</option>
            <option value="Đã gửi">Đã gửi</option>
            <option value="Đã mở">Đã mở</option>
            <option value="Đã phản hồi - quan tâm">Đã phản hồi - quan tâm</option>
            <option value="Đã phản hồi - từ chối">Đã phản hồi - từ chối</option>
            <option value="__custom__">Khác (nhập tay)...</option>
          </select>
        </td>
      </tr>`;
    })
    .join("");

  if (rows.length > 200) {
    tbody.innerHTML += `<tr><td colspan="6" class="hint">...và ${rows.length - 200} lead nữa, thu hẹp bộ lọc để xem hết.</td></tr>`;
  }

  tbody.querySelectorAll(".b2b-update-select").forEach((sel) => {
    sel.addEventListener("change", async () => {
      const ten = sel.dataset.ten;
      const lead = B2B_LEADS.find((l) => l.Ten === ten);
      let trangThai = sel.value;
      let ghiChu = "";

      if (trangThai === "__custom__") {
        trangThai = prompt(`Trạng thái mới cho "${ten}" (vd: Đã gọi - hẹn gọi lại, Từ chối, Đồng ý):`, lead.Trang_thai || "");
        if (trangThai === null) {
          sel.value = "";
          return;
        }
        ghiChu = prompt("Ghi chú thêm (để trống nếu không có):", "");
        if (ghiChu === null) {
          sel.value = "";
          return;
        }
      }

      try {
        await api("/api/b2b/update", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ten, trang_thai: trangThai, ghi_chu_them: ghiChu }),
        });
        await loadB2BLeads();
      } catch (err) {
        alert("Lỗi: " + err.message);
        sel.value = "";
      }
    });
  });
}

function setupB2BFilters() {
  ["b2b-filter-nhom", "b2b-filter-trangthai"].forEach((id) => document.getElementById(id).addEventListener("change", renderB2BTable));
  document.getElementById("b2b-search").addEventListener("input", renderB2BTable);
}

// ---------- Thư viện Media ----------
let MEDIA_ITEMS = [];

function fmtBytes(n) {
  if (n > 1024 * 1024) return (n / 1024 / 1024).toFixed(1) + " MB";
  if (n > 1024) return (n / 1024).toFixed(0) + " KB";
  return n + " B";
}

async function loadMedia() {
  const grid = document.getElementById("media-grid");
  grid.innerHTML = `<p class="hint">Đang quét thư mục...</p>`;
  MEDIA_ITEMS = await api("/api/media");
  renderMediaGrid();
}

function renderMediaGrid() {
  const search = document.getElementById("media-search").value.trim().toLowerCase();
  const category = document.getElementById("media-filter-category").value;
  const kind = document.getElementById("media-filter-kind").value;
  const onlyUnused = document.getElementById("media-filter-unused").checked;

  let rows = MEDIA_ITEMS;
  if (search) rows = rows.filter((m) => m.name.toLowerCase().includes(search));
  if (category) rows = rows.filter((m) => m.category === category);
  if (kind) rows = rows.filter((m) => m.kind === kind);
  if (onlyUnused) rows = rows.filter((m) => !m.used_in.length);

  document.getElementById("media-count").textContent =
    `Hiện ${rows.length} / ${MEDIA_ITEMS.length} file` +
    (rows.length > 300 ? " (chỉ hiện 300 đầu, thu hẹp bộ lọc để xem hết)" : "");

  const grid = document.getElementById("media-grid");
  if (!rows.length) {
    grid.innerHTML = `<p class="hint">Không tìm thấy file nào khớp bộ lọc.</p>`;
    return;
  }

  grid.innerHTML = rows
    .slice(0, 300)
    .map((m, i) => {
      const src = "/media/" + m.rel_path.split("/").map(encodeURIComponent).join("/");
      const thumb =
        m.kind === "image"
          ? `<img class="media-thumb" src="${src}" loading="lazy" alt="${escapeHtml(m.name)}">`
          : `<video class="media-thumb" src="${src}" preload="metadata" muted></video>`;
      const usedBadge = m.used_in.length
        ? `<span class="media-badge used" title="${escapeHtml(m.used_in.join(" | "))}">Đã dùng</span>`
        : `<span class="media-badge unused">Chưa dùng</span>`;
      return `<button type="button" class="media-item" data-idx="${i}" data-path="${escapeHtml(m.rel_path)}" title="${escapeHtml(m.rel_path)}">
        ${usedBadge}
        ${thumb}
        <span class="media-name">${escapeHtml(m.name)} · ${fmtBytes(m.size)}</span>
      </button>`;
    })
    .join("");

  grid.querySelectorAll(".media-item").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const p = btn.dataset.path;
      try {
        await navigator.clipboard.writeText(p);
        btn.classList.add("copied");
        setTimeout(() => btn.classList.remove("copied"), 1000);
      } catch {
        alert("Đường dẫn: " + p + "\n(không copy tự động được, hãy tự chép)");
      }
    });
  });
}

function setupMediaFilters() {
  ["media-search", "media-filter-category", "media-filter-kind", "media-filter-unused"].forEach((id) => {
    const el = document.getElementById(id);
    el.addEventListener(el.tagName === "INPUT" && el.type === "text" ? "input" : "change", renderMediaGrid);
  });
  document.getElementById("media-refresh-btn").addEventListener("click", loadMedia);
}

// ---------- Khởi động ----------
async function init() {
  setupTabs();
  setupOrderForm();
  setupBatchForm();
  setupExpenseForm();
  setupReportControls();
  setupB2BFilters();
  setupMediaFilters();
  await loadMeta();
  loadOrdersTable();
  loadBatchesTable();
  loadOverview();
}

init();
