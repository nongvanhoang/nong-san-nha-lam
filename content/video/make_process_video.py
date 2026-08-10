#!/usr/bin/env python3
"""
Ghép clip THẬT (đã có sẵn trong "Hình Ảnh, Video/") thành 1 video dọc ngắn
(1080x1920) kiểu "quy trình thật" — không phải video quảng cáo bóng bẩy.
Không có giọng AI, không dựng cảnh giả — chỉ clip thật + chữ thật đè lên,
đúng nguyên tắc "không bịa" áp dụng cho cả hệ thống.

Input: 1 file JSON mô tả clip nào, đoạn nào (giây bắt đầu/độ dài), chữ gì
hiện lúc nào — xem configs/README.md để biết đúng cấu trúc file.

Dùng:
  python make_process_video.py --config configs/ten-video.json

Cần ffmpeg trên PATH (đã xác nhận có sẵn trên máy này).

Output:
  output/<slug>.mp4
  output/<slug>_caption.txt   (rỗng, agent tự điền caption khi soạn bài)
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).parent
ROOT = HERE.parent.parent  # NongSanNhaLam/
MEDIA_ROOT = ROOT / "Hình Ảnh, Video"
OUTPUT_DIR = HERE / "output"
WIDTH, HEIGHT, FPS = 1080, 1920, 30

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_REG = "C:/Windows/Fonts/arial.ttf"
LOGO = ROOT / "docs" / "assets" / "icon-512.png"

END_CARD_SECONDS = 3.0


def esc_filter_path(p):
    """Escape cho dùng BÊN TRONG filtergraph (-vf/-filter_complex, textfile=/fontfile=)."""
    return str(p).replace("\\", "/").replace(":", "\\:")


def to_posix(p):
    """Chuyển path sang dạng ffmpeg đọc được cho concat demuxer / -i thường —
    KHÔNG escape dấu hai chấm (khác esc_filter_path, dùng nhầm sẽ hỏng path ổ đĩa Windows)."""
    return str(p).replace("\\", "/")


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        print("ffmpeg failed:", result.stderr[-3000:], file=sys.stderr)
        sys.exit(1)


def trim_clip(src, start, duration, out_path):
    """Cắt 1 đoạn từ clip thật, resize/crop phủ kín khung 1080x1920, mã hoá
    thống nhất để nối (concat) an toàn ở bước sau."""
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start), "-t", str(duration), "-i", str(src),
        "-vf", f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
               f"crop={WIDTH}:{HEIGHT},setsar=1,fps={FPS}",
        "-an",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        str(out_path),
    ]
    run(cmd)


def build_end_card(text_lines, out_path, tmp):
    """Thẻ kết thúc: nền màu thương hiệu + logo thật + thông tin liên hệ thật."""
    lines_txt = tmp / "endcard.txt"
    lines_txt.write_text("\n".join(text_lines), encoding="utf-8")

    cmd = ["ffmpeg", "-y"]
    cmd += ["-f", "lavfi", "-i", f"color=c=0x2F5233:s={WIDTH}x{HEIGHT}:d={END_CARD_SECONDS}:r={FPS}"]
    if LOGO.exists():
        cmd += ["-loop", "1", "-t", str(END_CARD_SECONDS), "-i", str(LOGO)]
        filter_complex = (
            f"[1:v]scale=320:-1[logo];"
            f"[0:v][logo]overlay=(W-w)/2:260[bg];"
            f"[bg]drawtext=fontfile='{esc_filter_path(FONT_BOLD)}':"
            f"textfile='{esc_filter_path(lines_txt)}':fontcolor=white:fontsize=44:"
            f"line_spacing=14:x=(w-text_w)/2:y=680[vout]"
        )
        cmd += ["-filter_complex", filter_complex, "-map", "[vout]"]
    else:
        cmd += [
            "-vf",
            f"drawtext=fontfile='{esc_filter_path(FONT_BOLD)}':"
            f"textfile='{esc_filter_path(lines_txt)}':fontcolor=white:fontsize=44:"
            f"line_spacing=14:x=(w-text_w)/2:y=(h-text_h)/2",
        ]
    cmd += ["-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_path)]
    run(cmd)


def build_video(config):
    slug = config["slug"]
    clips = config["clips"]
    captions = config.get("captions", [])
    end_card_lines = config.get("end_card_text", "Nhắn Zalo để đặt hàng").split("\n")

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / f"{slug}.mp4"

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        # 1) Cắt từng đoạn clip thật, tính offset thời gian tuyệt đối trên
        #    timeline sau khi nối (để chữ hiện đúng lúc, dù caption trong
        #    config viết theo thời gian riêng của từng clip).
        segment_paths = []
        cumulative = 0.0
        caption_offsets = []
        for i, clip in enumerate(clips):
            src = MEDIA_ROOT / clip["file"]
            if not src.exists():
                print(f"ERROR: không tìm thấy clip thật: {src}")
                sys.exit(1)
            duration = clip["duration"]
            seg_path = tmp / f"seg{i}.mp4"
            trim_clip(src, clip.get("start", 0), duration, seg_path)
            segment_paths.append(seg_path)
            caption_offsets.append(cumulative)
            cumulative += duration

        # 2) Thẻ kết thúc
        end_card_path = tmp / "endcard.mp4"
        build_end_card(end_card_lines, end_card_path, tmp)
        segment_paths.append(end_card_path)

        # 3) Nối các đoạn (concat demuxer — an toàn vì mọi đoạn đã mã hoá
        #    cùng codec/resolution/fps ở bước cắt).
        concat_list = tmp / "concat.txt"
        concat_list.write_text(
            "\n".join(f"file '{to_posix(p)}'" for p in segment_paths),
            encoding="utf-8",
        )
        concatenated = tmp / "concatenated.mp4"
        run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
            "-c", "copy", str(concatenated),
        ])

        # 4) Đè chữ caption đúng lúc (dùng textfile để chữ có dấu tiếng Việt
        #    không bị lỗi escape trong ffmpeg filter).
        if captions:
            filter_lines = ["[0:v]null[v0]"]
            cur = "v0"
            n_captions = len(captions)
            for i, cap in enumerate(captions):
                clip_i = cap.get("clip_index", i)
                start_abs = caption_offsets[clip_i] + cap.get("start", 0)
                end_abs = start_abs + cap.get("duration", 3)
                txt_file = tmp / f"cap{i}.txt"
                txt_file.write_text(cap["text"], encoding="utf-8")
                # đoạn cuối cùng phải xuất ra đúng nhãn [vout] để -map [vout] tìm thấy
                box_out = f"b{i}"
                text_out = "vout" if i == n_captions - 1 else f"v{i+1}"
                filter_lines.append(
                    f"[{cur}]drawbox=x=0:y={HEIGHT-260}:w={WIDTH}:h=260:"
                    f"color=black@0.55:t=fill:enable='between(t,{start_abs},{end_abs})'[{box_out}]"
                )
                filter_lines.append(
                    f"[{box_out}]drawtext=fontfile='{esc_filter_path(FONT_BOLD)}':"
                    f"textfile='{esc_filter_path(txt_file)}':fontcolor=white:fontsize=48:"
                    f"line_spacing=8:x=(w-text_w)/2:y={HEIGHT-190}:"
                    f"enable='between(t,{start_abs},{end_abs})'[{text_out}]"
                )
                cur = text_out

            filter_script = tmp / "captions.txt"
            filter_script.write_text(";\n".join(filter_lines), encoding="utf-8")

            run([
                "ffmpeg", "-y", "-i", str(concatenated),
                "-filter_complex_script", str(filter_script),
                "-map", "[vout]",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                str(out_path),
            ])
        else:
            shutil.copy(concatenated, out_path)

    caption_path = out_path.with_name(out_path.stem + "_caption.txt")
    if not caption_path.exists():
        caption_path.write_text("", encoding="utf-8")
    print(f"Đã tạo: {out_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", required=True, help="đường dẫn file JSON mô tả video")
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        print("ERROR: không tìm thấy ffmpeg trên PATH.")
        sys.exit(1)

    with open(args.config, encoding="utf-8") as f:
        config = json.load(f)

    build_video(config)


if __name__ == "__main__":
    main()
