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

FONT_BOLD = "C:/Windows/Fonts/cambriab.ttf"  # đổi từ Arial sang Cambria — đúng bộ nhận diện thương hiệu
FONT_REG = "C:/Windows/Fonts/cambriab.ttf"
LOGO = ROOT / "docs" / "assets" / "icon-512.png"

END_CARD_SECONDS = 3.0
TRANSITION_SECONDS = 0.35  # crossfade mượt giữa các clip quy trình (không áp dụng vào thẻ kết thúc)
ZOOM_START = 1.12  # phóng nhẹ rồi zoom in dần trong mỗi đoạn clip, bớt cảm giác đứng yên
TEXT_FADE_SECONDS = 0.25  # chữ đè fade in/out thay vì bật/tắt cứng


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
    thống nhất để nối (concat) an toàn ở bước sau. Zoom nhẹ cố định (ZOOM_START)
    để khung hình chặt/có chủ đích hơn, bớt khoảng trống rìa ảnh — đã thử zoom
    ĐỘNG (phóng to dần theo thời gian) nhưng bản ffmpeg trên máy này không hỗ
    trợ eval=frame cho crop filter nên dùng bản tĩnh, chắc chắn chạy được."""
    ow, oh = round(WIDTH * ZOOM_START), round(HEIGHT * ZOOM_START)
    ow += ow % 2
    oh += oh % 2
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start), "-t", str(duration), "-i", str(src),
        "-vf", (
            f"scale={ow}:{oh}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},setsar=1,fps={FPS}"
        ),
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
            f"line_spacing=14:x=(w-text_w)/2:y=680:alpha='min(1,t/0.4)'[vout]"
        )
        cmd += ["-filter_complex", filter_complex, "-map", "[vout]"]
    else:
        cmd += [
            "-vf",
            f"drawtext=fontfile='{esc_filter_path(FONT_BOLD)}':"
            f"textfile='{esc_filter_path(lines_txt)}':fontcolor=white:fontsize=44:"
            f"line_spacing=14:x=(w-text_w)/2:y=(h-text_h)/2:alpha='min(1,t/0.4)'",
        ]
    cmd += ["-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_path)]
    run(cmd)


def crossfade_sequence(segment_paths, durations, transition, out_path):
    """Nối các đoạn clip bằng crossfade (mờ dần chồng nhau) thay vì cắt cứng,
    cho cảm giác mượt/chuyên nghiệp hơn. Trả về offset TUYỆT ĐỐI (giây) của
    từng clip trên video đã ghép — dùng để canh giờ chữ caption cho đúng,
    vì thời lượng tổng bị rút ngắn đi (transition*(n-1)) so với cộng dồn thô."""
    n = len(segment_paths)
    if n == 1:
        shutil.copy(segment_paths[0], out_path)
        return [0.0]

    cmd = ["ffmpeg", "-y"]
    for p in segment_paths:
        cmd += ["-i", str(p)]

    filter_parts = []
    cur = "0:v"
    offsets = [0.0]
    cumulative_raw = durations[0]
    for i in range(1, n):
        offset = cumulative_raw - i * transition
        offsets.append(offset)
        nxt = f"x{i}"
        filter_parts.append(
            f"[{cur}][{i}:v]xfade=transition=fade:duration={transition}:offset={offset:.3f}[{nxt}]"
        )
        cur = nxt
        cumulative_raw += durations[i]

    cmd += ["-filter_complex", ";".join(filter_parts), "-map", f"[{cur}]"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_path)]
    run(cmd)
    return offsets


def build_video(config):
    slug = config["slug"]
    clips = config["clips"]
    captions = config.get("captions", [])
    end_card_lines = config.get("end_card_text", "Nhắn Zalo để đặt hàng").split("\n")

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / f"{slug}.mp4"

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        # 1) Cắt từng đoạn clip thật.
        segment_paths = []
        durations = []
        for i, clip in enumerate(clips):
            src = MEDIA_ROOT / clip["file"]
            if not src.exists():
                print(f"ERROR: không tìm thấy clip thật: {src}")
                sys.exit(1)
            duration = clip["duration"]
            seg_path = tmp / f"seg{i}.mp4"
            trim_clip(src, clip.get("start", 0), duration, seg_path)
            segment_paths.append(seg_path)
            durations.append(duration)

        # 2) Nối các clip quy trình bằng crossfade (mượt hơn cắt cứng), rồi
        #    lấy offset tuyệt đối thật của từng clip để canh chữ caption cho
        #    đúng lúc — KHÔNG dùng cộng dồn thô nữa vì crossfade rút ngắn
        #    thời lượng tổng.
        transitioned = tmp / "transitioned.mp4"
        caption_offsets = crossfade_sequence(segment_paths, durations, TRANSITION_SECONDS, transitioned)

        # 3) Thẻ kết thúc — nối vào bằng cắt cứng (không crossfade), giữ cảm
        #    giác "chốt lại" rõ ràng khi chuyển sang màn hình thương hiệu.
        end_card_path = tmp / "endcard.mp4"
        build_end_card(end_card_lines, end_card_path, tmp)

        concat_list = tmp / "concat.txt"
        concat_list.write_text(
            "\n".join(f"file '{to_posix(p)}'" for p in [transitioned, end_card_path]),
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
            # Tính trước mọi mốc bắt đầu, rồi CẮT BỚT mốc kết thúc của mỗi chữ
            # tại đúng lúc chữ tiếp theo xuất hiện — nếu không, 2 chữ liền
            # nhau sẽ đè lên nhau trong đúng khoảng crossfade (chữ cũ chưa
            # kịp tắt thì chữ mới đã hiện).
            starts_abs = [
                caption_offsets[cap.get("clip_index", i)] + cap.get("start", 0)
                for i, cap in enumerate(captions)
            ]
            natural_ends = [starts_abs[i] + cap.get("duration", 3) for i, cap in enumerate(captions)]
            sorted_starts = sorted(starts_abs)
            ends_abs = []
            for i in range(len(captions)):
                end = natural_ends[i]
                for s in sorted_starts:
                    if starts_abs[i] < s < end:
                        end = s
                        break
                ends_abs.append(end)

            filter_lines = ["[0:v]null[v0]"]
            cur = "v0"
            n_captions = len(captions)
            for i, cap in enumerate(captions):
                start_abs = starts_abs[i]
                end_abs = ends_abs[i]
                txt_file = tmp / f"cap{i}.txt"
                txt_file.write_text(cap["text"], encoding="utf-8")
                # đoạn cuối cùng phải xuất ra đúng nhãn [vout] để -map [vout] tìm thấy
                box_out = f"b{i}"
                text_out = "vout" if i == n_captions - 1 else f"v{i+1}"
                filter_lines.append(
                    f"[{cur}]drawbox=x=0:y={HEIGHT-260}:w={WIDTH}:h=260:"
                    f"color=black@0.55:t=fill:enable='between(t,{start_abs},{end_abs})'[{box_out}]"
                )
                fade_alpha = (
                    f"if(lt(t,{start_abs}+{TEXT_FADE_SECONDS}),(t-{start_abs})/{TEXT_FADE_SECONDS},"
                    f"if(gt(t,{end_abs}-{TEXT_FADE_SECONDS}),({end_abs}-t)/{TEXT_FADE_SECONDS},1))"
                )
                filter_lines.append(
                    f"[{box_out}]drawtext=fontfile='{esc_filter_path(FONT_BOLD)}':"
                    f"textfile='{esc_filter_path(txt_file)}':fontcolor=white:fontsize=48:"
                    f"line_spacing=8:x=(w-text_w)/2:y={HEIGHT-190}:"
                    f"alpha='{fade_alpha}':"
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
