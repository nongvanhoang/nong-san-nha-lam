#!/usr/bin/env python3
"""App quản lý local cho Nông Sản Nhà Làm — ghi đơn hàng, ghi mẻ sản xuất,
xem báo cáo, sửa giá sản phẩm. Chỉ dùng thư viện chuẩn Python (không cần pip
install gì thêm). Chạy xong mở trình duyệt vào địa chỉ được in ra.

Chạy: python scripts/webapp.py
"""
import json
import socket
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from nsn_core import (
    CHANNELS,
    ORDERS_CSV,
    PRODUCTION_CSV,
    STATUS_LABELS,
    STATUSES,
    add_batch,
    add_order,
    compute_report,
    load_products,
    load_rows,
    update_variant_price,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PORT = 8943
STATIC_DIR = Path(__file__).resolve().parent / "webapp_static"

STATIC_FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/app.js": ("app.js", "application/javascript; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
}


def get_lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # bớt spam log request bình thường ra console

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, message, status=400):
        self._send_json({"error": message}, status=status)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path in STATIC_FILES:
            filename, content_type = STATIC_FILES[path]
            file_path = STATIC_DIR / filename
            if not file_path.exists():
                self._send_error_json("Không tìm thấy file giao diện", status=404)
                return
            body = file_path.read_text(encoding="utf-8").encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/api/report":
            days = int(query.get("days", ["7"])[0])
            self._send_json(compute_report(days))
            return

        if path == "/api/products":
            self._send_json(load_products())
            return

        if path == "/api/meta":
            products = load_products()
            product_names = [p["name"] for p in products["products"]]
            self._send_json({
                "channels": CHANNELS,
                "statuses": STATUSES,
                "status_labels": STATUS_LABELS,
                "product_names": product_names,
            })
            return

        if path == "/api/orders":
            limit = int(query.get("limit", ["20"])[0])
            rows = load_rows(ORDERS_CSV)
            self._send_json(list(reversed(rows))[:limit])
            return

        if path == "/api/batches":
            limit = int(query.get("limit", ["20"])[0])
            rows = load_rows(PRODUCTION_CSV)
            self._send_json(list(reversed(rows))[:limit])
            return

        self._send_error_json("Không tìm thấy đường dẫn này", status=404)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            data = self._read_json_body()
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_error_json("Dữ liệu gửi lên không đúng định dạng")
            return

        try:
            if path == "/api/orders":
                row = add_order(
                    date_str=data.get("date") or None,
                    customer=data.get("customer", ""),
                    product=data.get("product", ""),
                    qty=data.get("qty"),
                    unit=data.get("unit") or "kg",
                    unit_price=data.get("unit_price"),
                    channel=data.get("channel", ""),
                    status=data.get("status") or "moi",
                    note=data.get("note", ""),
                )
                self._send_json({"ok": True, "row": row})
                return

            if path == "/api/batches":
                row = add_batch(
                    date_str=data.get("date") or None,
                    product=data.get("product", ""),
                    quantity=data.get("quantity"),
                    unit=data.get("unit") or "kg",
                    batch_id=data.get("batch_id") or None,
                    note=data.get("note", ""),
                )
                self._send_json({"ok": True, "row": row})
                return

            if path == "/api/products/price":
                updated = update_variant_price(
                    product_id=data.get("product_id", ""),
                    package=data.get("package", ""),
                    new_price=data.get("price"),
                )
                self._send_json({"ok": True, "products": updated})
                return

            self._send_error_json("Không tìm thấy đường dẫn này", status=404)
        except (ValueError, TypeError) as exc:
            self._send_error_json(str(exc))
        except Exception as exc:  # noqa: BLE001 - trả lỗi chung, không để app crash
            print(f"Lỗi server: {exc}", file=sys.stderr)
            self._send_error_json("Có lỗi xảy ra ở server, kiểm tra lại dữ liệu nhập", status=500)


def main():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    lan_ip = get_lan_ip()
    local_url = f"http://127.0.0.1:{PORT}/"
    lan_url = f"http://{lan_ip}:{PORT}/"

    print("=== App quản lý Nông Sản Nhà Làm đang chạy ===")
    print(f"  Trên máy này:        {local_url}")
    print(f"  Từ điện thoại (cùng wifi nhà): {lan_url}")
    print("\nGiữ cửa sổ này mở khi đang dùng app. Nhấn Ctrl+C để tắt.\n")

    try:
        webbrowser.open(local_url)
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã tắt app.")


if __name__ == "__main__":
    main()
