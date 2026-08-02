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
      if (btn.dataset.tab === "bao-cao") loadReport();
      if (btn.dataset.tab === "gia-san-pham") loadProductsEditor();
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
}

// ---------- Ghi đơn hàng ----------
function setupOrderForm() {
  document.getElementById("order-date").value = todayStr();
  const form = document.getElementById("form-order");
  const msg = document.getElementById("order-msg");

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

// ---------- Khởi động ----------
async function init() {
  setupTabs();
  setupOrderForm();
  setupBatchForm();
  setupReportControls();
  await loadMeta();
  loadOrdersTable();
  loadBatchesTable();
}

init();
