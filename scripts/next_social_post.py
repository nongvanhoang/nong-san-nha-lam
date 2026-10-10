#!/usr/bin/env python3
"""In ra nội dung bài đăng TIẾP THEO trong hàng đợi xoay vòng (data/social_queue.json),
trích đúng đoạn theo từng kênh từ content/posts_ready.md, rồi tự tăng con trỏ hàng đợi
(data/social_queue_state.json) lên 1 để lần chạy sau ra mục kế tiếp.

Dùng cho lịch nhắc đăng bài đều đặn (mỗi 3 ngày 1 bài) - chạy độc lập, không cần Claude
đọc/hiểu file .md mỗi lần, chỉ cần in ra và gửi nguyên văn cho người dùng.

Chạy: python scripts/next_social_post.py
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
QUEUE_PATH = BASE_DIR / "data" / "social_queue.json"
STATE_PATH = BASE_DIR / "data" / "social_queue_state.json"
POSTS_PATH = BASE_DIR / "content" / "posts_ready.md"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def load_json(path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.replace(path)


def parse_posts_blocks(text):
    """Trả về list (heading_line, body) cho mỗi mục '## ...' trong posts_ready.md."""
    parts = re.split(r"\n(?=## )", text)
    blocks = []
    for part in parts:
        if not part.startswith("## "):
            continue
        lines = part.splitlines()
        heading = lines[0][3:].strip()
        body = "\n".join(lines[1:]).strip()
        body = re.sub(r"\n---\s*$", "", body).strip()
        blocks.append((heading, body))
    return blocks


def find_block(blocks, channel: str, topic_keyword: str):
    for heading, body in blocks:
        if not heading.lower().startswith(channel.lower()):
            continue
        if topic_keyword.lower() in heading.lower():
            return heading, body
    return None, None


def main():
    queue = load_json(QUEUE_PATH)["items"]
    state = load_json(STATE_PATH)
    idx = state["next_index"]

    if idx >= len(queue):
        print("Hàng đợi đã hết (đã nhắc đủ hết các mục trong data/social_queue.json).")
        print("Cần thêm mục mới vào hàng đợi (nhờ Claude soạn thêm nội dung + thêm vào file).")
        return

    item = queue[idx]
    topic = item["topic_keyword"]
    blocks = parse_posts_blocks(POSTS_PATH.read_text(encoding="utf-8"))

    print(f"=== Bài tiếp theo ({idx + 1}/{len(queue)}): {topic} ===\n")

    missing = []
    for channel in item["channels"]:
        heading, body = find_block(blocks, channel, topic)
        if body is None:
            missing.append(channel)
            continue
        print(f"--- {heading} ---")
        print(body)
        print()

    if missing:
        print(f"[Cảnh báo] Không tìm thấy nội dung cho kênh: {', '.join(missing)} "
              f"— kiểm tra lại tiêu đề trong content/posts_ready.md có khớp từ khoá '{topic}' không.")

    state["next_index"] = idx + 1
    state["last_sent_date"] = date.today().isoformat()
    save_json(STATE_PATH, state)


if __name__ == "__main__":
    main()
