#!/usr/bin/env python3
"""Hook nhẹ cho Claude Code, mượn ý tưởng từ ECC (github.com/affaan-m/ECC, MIT) nhưng viết lại
chỉ bằng thư viện chuẩn để chạy được trên Windows (bản gốc của ECC cần bash/node + tiến trình nền,
không sống được trên Windows thường).

Một file dùng chung cho mọi dự án — mỗi tính năng tự bật khi thấy đúng file/thư mục của dự án đó:
  session-start : cảnh báo html/ lệch gốc (RankerToolAI), liệt kê việc treo trong VIEC_CAN_LAM.md
  post-edit     : sửa trang section/slug/index.html -> chạy seo_audit.py cho trang đó, chỉ báo khi FAIL;
                  kèm nhắc /compact khi ngữ cảnh phiên đã lớn (ý tưởng strategic-compact của ECC)
  pre-commit    : trước git commit -> hỏi lại nếu có file .html bị mất mã GTM, hoặc file bí mật bị stage

Hook không bao giờ làm hỏng phiên: mọi lỗi nội bộ đều bị nuốt và thoát 0.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()
COMPACT_TOKENS = int(os.environ.get("ECC_COMPACT_TOKENS", "160000"))
COMPACT_INTERVAL = int(os.environ.get("ECC_COMPACT_INTERVAL", "60000"))
GTM_RE = re.compile(r"googletagmanager|GTM-[A-Z0-9]{4,}")
SECRET_NAME_RE = re.compile(r"(^|/)(\.env(\..+)?|client_secret[^/]*\.json|[^/]*token[^/]*\.json|[^/]*\.pem|[^/]*\.key)$", re.I)


def run(cmd, cwd=ROOT, timeout=60):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout, env=env)
    return r.stdout + r.stderr


def emit(event, context=None, user_msg=None, extra=None):
    out = {}
    spec = {"hookEventName": event}
    if context:
        spec["additionalContext"] = context
    if extra:
        spec.update(extra)
    if len(spec) > 1:
        out["hookSpecificOutput"] = spec
    if user_msg:
        out["systemMessage"] = user_msg
    if out:
        print(json.dumps(out, ensure_ascii=False))


# ---------- session-start ----------

def html_drift():
    html = ROOT / "html"
    if not (html / ".git").exists():
        return None
    try:
        root_ct = int(run(["git", "log", "-1", "--format=%ct"]).strip())
        html_ct = int(run(["git", "log", "-1", "--format=%ct"], cwd=html).strip())
    except ValueError:
        return None
    if root_ct - html_ct <= 86400:
        return None
    days = (root_ct - html_ct) // 86400
    ahead = run(["git", "rev-list", "--count", f"--since={html_ct}", "HEAD"]).strip()
    return (f"⚠ html/ (thư mục thực sự được deploy) chậm hơn repo gốc {days} ngày ({ahead} commit). "
            "Trang vừa sửa ở gốc có thể CHƯA live — xem Category 0b trong rankertoolai-monitor.md.")


def pending_tasks():
    f = ROOT / "VIEC_CAN_LAM.md"
    if not f.exists():
        return None
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    open_items = [l for l in lines if l.lstrip().startswith("- [ ]")]
    if not open_items:
        return None
    titles = []
    for l in open_items[:5]:
        m = re.search(r"\*\*(.+?)\*\*", l)
        titles.append("  • " + (m.group(1) if m else l.strip()[6:80]))
    more = f"\n  … và {len(open_items) - 5} việc nữa" if len(open_items) > 5 else ""
    return f"📋 VIEC_CAN_LAM.md còn {len(open_items)} việc chưa xong:\n" + "\n".join(titles) + more


def session_start(_data):
    notes = [n for n in (html_drift(), pending_tasks()) if n]
    if notes:
        text = "\n".join(notes)
        emit("SessionStart", context=text, user_msg=text)


# ---------- post-edit ----------

def audit_page(file_path):
    """Chạy audit_page() của seo_audit.py lên ĐÚNG file vừa sửa. seo_audit.py tự đọc từ thư mục
    deploy (html/ ở RankerToolAI, public/ ở RankerNest) nên gọi nó qua CLI sẽ chấm bản cũ nếu vừa
    sửa bản ở gốc — ở đây trỏ tạm biến thư mục gốc của nó vào nơi chứa file vừa sửa."""
    if not file_path or not file_path.lower().endswith("index.html"):
        return None
    audit = ROOT / "seo_audit.py"
    if not audit.exists():
        return None
    page = Path(file_path).resolve()
    try:
        page.relative_to(ROOT)
    except ValueError:
        return None
    section, slug, base = page.parent.parent.name, page.parent.name, page.parent.parent.parent
    import importlib.util
    spec = importlib.util.spec_from_file_location("seo_audit", audit)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if section not in getattr(mod, "SECTIONS", []):
        return None
    for var in ("HTML_DIR", "ROOT_DIR"):
        if hasattr(mod, var):
            setattr(mod, var, base)
    result = mod.audit_page(section, slug)
    issues = result.get("issues") or ([result["error"]] if result.get("error") else [])
    if not issues:
        return None
    rel = page.relative_to(ROOT).as_posix()
    return (f"seo_audit báo {rel} FAIL sau lần sửa này — sửa luôn nếu do thay đổi vừa rồi gây ra:\n"
            + "\n".join("  - " + i for i in issues))


def context_tokens(transcript_path):
    if not transcript_path or not os.path.exists(transcript_path):
        return 0
    with open(transcript_path, "rb") as fh:
        fh.seek(0, 2)
        size = fh.tell()
        fh.seek(max(0, size - 512_000))
        chunk = fh.read().decode("utf-8", errors="replace")
    for line in reversed(chunk.splitlines()):
        if '"usage"' not in line:
            continue
        try:
            usage = json.loads(line).get("message", {}).get("usage")
        except (json.JSONDecodeError, AttributeError):
            continue
        if isinstance(usage, dict):
            return sum(int(usage.get(k) or 0) for k in
                       ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
    return 0


def compact_hint(data):
    tokens = context_tokens(data.get("transcript_path"))
    if tokens < COMPACT_TOKENS:
        return None
    state = Path(tempfile.gettempdir()) / f"ecc_compact_{data.get('session_id', 'x')}.json"
    last = 0
    try:
        last = json.loads(state.read_text()).get("warned_at", 0)
    except (OSError, ValueError):
        pass
    if last and tokens < last + COMPACT_INTERVAL:
        return None
    state.write_text(json.dumps({"warned_at": tokens, "ts": time.time()}))
    return (f"Ngữ cảnh phiên đã khoảng {tokens // 1000}k token. Nếu vừa xong một giai đoạn: ghi việc còn lại ra file, "
            "chạy /rut-kinh-nghiem để lưu bài học, rồi /compact. Đừng compact khi đang sửa dở giữa chừng.")


def post_edit(data):
    fp = (data.get("tool_input") or {}).get("file_path")
    audit = audit_page(fp)
    hint = compact_hint(data)
    ctx = "\n\n".join(x for x in (audit, hint) if x)
    if ctx:
        emit("PostToolUse", context=ctx, user_msg=hint)


# ---------- pre-commit ----------

def repo_dir_for(cmd):
    m = re.search(r"git\s+-C\s+[\"']?([^\"'\s]+)", cmd) or re.search(r"\bcd\s+[\"']?([^\"'\s;&|]+)", cmd)
    if not m:
        return ROOT
    p = Path(m.group(1))
    return (p if p.is_absolute() else ROOT / p).resolve()


def pre_commit(data):
    cmd = (data.get("tool_input") or {}).get("command") or ""
    if not re.search(r"\bgit\b[^\n]*\bcommit\b", cmd):
        return
    repo = repo_dir_for(cmd)
    problems = []

    # GTM bị xoá ròng trong file .html (staged + chưa stage, so với HEAD)
    diff = run(["git", "diff", "HEAD", "-U0", "--", "*.html"], cwd=repo, timeout=60)
    net, cur = {}, None
    for line in diff.splitlines():
        if line.startswith("+++ "):
            cur = line[6:] if line.startswith("+++ b/") else None
        elif cur and GTM_RE.search(line):
            if line.startswith("-") and not line.startswith("---"):
                net[cur] = net.get(cur, 0) + 1
            elif line.startswith("+"):
                net[cur] = net.get(cur, 0) - 1
    lost = [f for f, n in net.items() if n > 0]
    if lost:
        shown = "\n".join("  - " + f for f in lost[:10]) + (f"\n  … +{len(lost) - 10} file" if len(lost) > 10 else "")
        problems.append(f"{len(lost)} file .html bị MẤT mã GTM so với HEAD (thường do script generate_*/inject_* ghi đè):\n{shown}")

    # File bí mật đang được stage
    staged = run(["git", "diff", "--cached", "--name-only"], cwd=repo).splitlines()
    secrets = [f for f in staged if SECRET_NAME_RE.search(f.strip())]
    if secrets:
        problems.append("File trông như chứa khoá bí mật đang được stage: " + ", ".join(secrets[:10]))

    if problems:
        reason = "Kiểm tra trước commit (ecc_hooks.py):\n" + "\n".join(problems)
        emit("PreToolUse", extra={"permissionDecision": "ask", "permissionDecisionReason": reason})


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    # Windows mặc định cp1252 -> in tiếng Việt sẽ lỗi và bị nuốt im lặng
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        data = {}
    handler = {"session-start": session_start, "post-edit": post_edit, "pre-commit": pre_commit}.get(mode)
    if handler:
        try:
            handler(data)
        except Exception:  # hook không bao giờ được làm hỏng phiên làm việc
            if os.environ.get("ECC_HOOK_DEBUG"):
                import traceback
                traceback.print_exc()
    sys.exit(0)


if __name__ == "__main__":
    main()
