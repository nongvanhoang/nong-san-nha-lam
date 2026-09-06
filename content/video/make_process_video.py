#!/usr/bin/env python3
"""
Ghép clip THẬT (đã có sẵn trong "Hình Ảnh, Video/") thành 1 video dọc ngắn
(1080x1920) kiểu "quy trình thật" — HÌNH ẢNH luôn 100% clip thật, không dàn
dựng cảnh giả, đúng nguyên tắc "không bịa" áp dụng cho cả hệ thống.

Từ 2026-09-03, hỗ trợ thêm 2 lớp KHÔNG BẮT BUỘC (bật qua config JSON, không
khai báo thì video vẫn chạy y như trước — im lặng, chỉ chữ tiếng Việt):
  - Giọng đọc AI tiếng Việt qua Edge-TTS (Microsoft, miễn phí, không cần API
    key) — chỉ thêm LỜI ĐỌC, không thay thế/chỉnh sửa hình ảnh thật nào.
  - Phụ đề tiếng Anh chèn cứng, nằm ngay phía trên dòng chữ tiếng Việt — để
    đăng được cho khách quốc tế trên LinkedIn/Instagram/TikTok/YouTube.
Xem configs/README.md để biết cấu trúc field "narration" / "text_en".

Input: 1 file JSON mô tả clip nào, đoạn nào (giây bắt đầu/độ dài), chữ gì
hiện lúc nào — xem configs/README.md để biết đúng cấu trúc file.

Dùng:
  python make_process_video.py --config configs/ten-video.json

Cần ffmpeg + ffprobe trên PATH (đã xác nhận có sẵn trên máy này). Nếu config
có "narration", cần gói Python "edge-tts" (cài 1 lần: pip install edge-tts).

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

FONT_BOLD = "C:/Windows/Fonts/cambriab.ttf"  # chữ tiếng Việt (chính) — đúng bộ nhận diện thương hiệu
FONT_REG = "C:/Windows/Fonts/cambriab.ttf"
FONT_ITALIC = "C:/Windows/Fonts/cambriai.ttf"  # phụ đề tiếng Anh (phụ) — nghiêng để phân biệt với chữ chính
LOGO = ROOT / "docs" / "assets" / "icon-512.png"

END_CARD_SECONDS = 3.0
MAX_END_CARD_SECONDS = 20.0  # chặn trần — nếu lời đọc dài bất thường so với video, script sẽ báo thay vì tự kéo dài vô hạn
TRANSITION_SECONDS = 0.35  # crossfade mượt giữa các clip quy trình (không áp dụng vào thẻ kết thúc)
ZOOM_START = 1.12  # phóng nhẹ rồi zoom in dần trong mỗi đoạn clip, bớt cảm giác đứng yên
ZOOM_DETAIL = 1.22  # mức zoom mạnh hơn cho motion="zoom_detail" (cảnh chi tiết/cận cảnh cuối)
TEXT_FADE_SECONDS = 0.25  # chữ đè fade in/out thay vì bật/tắt cứng
MUSIC_VOLUME_DEFAULT = 0.16  # nhạc nền nhỏ, không lấn giọng đọc — chỉnh qua config["music"]["volume"] nếu cần
MUSIC_FADE_IN = 1.0
MUSIC_FADE_OUT = 1.5

EN_BAND_HEIGHT = 78  # dải phụ đề tiếng Anh, nằm ngay phía trên dải chữ tiếng Việt (cao 260px)
END_CARD_LINE_PITCH = 135  # khoảng cách dòng thực tế đo được trên máy này ở fontsize=44/line_spacing=14
                            # (lớn hơn nhiều so với 44+14 cộng thô — Cambria Bold có ascent/descent lớn),
                            # dùng để tính chỗ đặt khối chữ tiếng Anh bên dưới mà không đè lên khối tiếng Việt
DEFAULT_VOICE = "vi-VN-HoaiMyNeural"  # giọng nữ, thân thiện — hợp tông "nhà mình". Đổi sang vi-VN-NamMinhNeural (nam) trong config nếu muốn đổi giọng


def esc_filter_path(p):
    """Escape cho dùng BÊN TRONG filtergraph (-vf/-filter_complex, textfile=/fontfile=)."""
    return str(p).replace("\\", "/").replace(":", "\\:")


# LƯU Ý drawtext + "%": ffmpeg drawtext mặc định bật cú pháp mở rộng %{...}
# (vd %{pts}) — một dấu % trơn (như trong "100%") làm CẢ DÒNG CHỮ biến mất
# im lặng (ffmpeg vẫn exit code 0, chỉ in warning "Stray %" ra stderr, rất
# dễ bỏ sót). Nhân đôi thành "%%" KHÔNG sửa được (đã thử, vẫn lỗi y hệt) —
# cách đúng là tắt hẳn cú pháp mở rộng bằng `expansion=none` trên MỌI
# drawtext dùng textfile= (xem 4 chỗ dùng trong file này), giữ % thật trong
# chữ mà không cần escape gì cả.


def to_posix(p):
    """Chuyển path sang dạng ffmpeg đọc được cho concat demuxer / -i thường —
    KHÔNG escape dấu hai chấm (khác esc_filter_path, dùng nhầm sẽ hỏng path ổ đĩa Windows)."""
    return str(p).replace("\\", "/")


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        print("ffmpeg failed:", result.stderr[-3000:], file=sys.stderr)
        sys.exit(1)


def ffprobe_duration(path):
    """Đọc độ dài thật (giây) của 1 file media qua ffprobe — dùng để biết lời
    đọc AI dài bao nhiêu, từ đó tính thẻ kết thúc cần kéo dài thêm bao nhiêu."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode != 0 or not result.stdout.strip():
        print("ffprobe failed:", result.stderr[-2000:], file=sys.stderr)
        sys.exit(1)
    return float(result.stdout.strip())


def generate_narration(text, voice, out_path):
    """Tạo giọng đọc AI qua Edge-TTS (Microsoft, miễn phí, không cần API key,
    không tốn phí — đúng giới hạn "không gọi API AI trả phí" trong CLAUDE.md).
    Đây chỉ là LỜI ĐỌC diễn giải thêm — hình ảnh vẫn 100% clip thật, không
    dựng cảnh giả nào để khớp lời đọc."""
    cmd = [
        sys.executable, "-m", "edge_tts",
        "--voice", voice,
        "--text", text,
        "--write-media", str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0 or not out_path.exists():
        print(
            "edge-tts failed (đã cài chưa? chạy: pip install edge-tts):",
            result.stderr[-2000:], file=sys.stderr,
        )
        sys.exit(1)


def trim_clip(src, start, duration, out_path, motion="zoom"):
    """Cắt 1 đoạn từ clip thật, resize/crop phủ kín khung 1080x1920, mã hoá
    thống nhất để nối (concat) an toàn ở bước sau. Chuyển động máy quay ẢO
    ĐỘNG thật (kiểu Ken Burns, không phải hiệu ứng giả) — dùng filter
    `zoompan` (kiểm tra 2026-09-05: chạy mượt, không giật; bản `crop` với
    biểu thức theo thời gian trước đây không dùng được vì bản ffmpeg cũ
    không hỗ trợ eval=frame cho crop).

    `motion` — chọn kiểu chuyển động, tránh mọi cảnh đều zoom-vào-giữa giống
    hệt nhau (chốt 2026-09-05, sau phản hồi video nhìn "lặp công thức"):
      - "zoom" (mặc định): zoom vào giữa khung hình, mức ZOOM_START (1.12).
      - "zoom_detail": zoom vào giữa nhưng mạnh hơn (ZOOM_DETAIL, 1.22) —
        hợp cảnh cận chi tiết hoặc cảnh chốt cuối video.
      - "pan_left" / "pan_right": giữ zoom cố định ZOOM_START, lia ngang
        khung hình từ phải sang trái (hoặc ngược lại) — hợp cảnh có đường
        nét ngang (hàng dây leo, dãy khay) hoặc cảnh tay đang thao tác.

    Có thêm 1 lớp chỉnh màu nhẹ (eq contrast/saturation) áp dụng ĐỀU cho mọi
    clip, để ảnh thật chụp khác thời điểm/ánh sáng trông "cùng một bộ" hơn —
    chỉ chỉnh tông màu, không thêm/bớt nội dung hình ảnh."""
    n_frames = max(1, round(duration * FPS))
    n_ref = max(n_frames - 1, 1)

    if motion == "zoom_detail":
        step = (ZOOM_DETAIL - 1.0) / n_frames
        z_expr = f"min(zoom+{step:.6f},{ZOOM_DETAIL})"
        x_expr, y_expr = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif motion == "pan_left":
        z_expr = f"{ZOOM_START}"
        x_expr = f"(iw-iw/zoom)*(1-on/{n_ref})"
        y_expr = "ih/2-(ih/zoom/2)"
    elif motion == "pan_right":
        z_expr = f"{ZOOM_START}"
        x_expr = f"(iw-iw/zoom)*(on/{n_ref})"
        y_expr = "ih/2-(ih/zoom/2)"
    else:  # "zoom" mặc định
        step = (ZOOM_START - 1.0) / n_frames
        z_expr = f"min(zoom+{step:.6f},{ZOOM_START})"
        x_expr, y_expr = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"

    is_image = str(src).lower().endswith((".jpg", ".jpeg", ".png"))
    if is_image:
        # Ảnh tĩnh không có timeline riêng — dùng -loop 1 để ffmpeg lặp lại
        # đúng 1 khung hình cho zoompan "vẽ" chuyển động lên trên, bỏ qua
        # -ss/-t (không có ý nghĩa với ảnh tĩnh).
        input_args = ["-loop", "1", "-t", str(duration), "-i", str(src)]
    else:
        input_args = ["-ss", str(start), "-t", str(duration), "-i", str(src)]

    cmd = [
        "ffmpeg", "-y",
        *input_args,
        "-vf", (
            f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},setsar=1,fps={FPS},"
            f"eq=contrast=1.05:saturation=1.08,"
            f"zoompan=z='{z_expr}':d=1:x='{x_expr}':y='{y_expr}':s={WIDTH}x{HEIGHT}:fps={FPS}"
        ),
        "-frames:v", str(n_frames),
        "-an",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        str(out_path),
    ]
    run(cmd)


def build_end_card(text_lines, out_path, tmp, duration=END_CARD_SECONDS, text_lines_en=None):
    """Thẻ kết thúc: nền màu thương hiệu + logo thật + thông tin liên hệ thật.
    `duration` có thể dài hơn mặc định nếu lời đọc AI chưa đọc xong khi hình
    ảnh quy trình đã hết (xem build_video). `text_lines_en` (tuỳ chọn) thêm
    1 dòng tiếng Anh nhỏ hơn, in nghiêng, nằm dưới chữ tiếng Việt chính."""
    lines_txt = tmp / "endcard.txt"
    lines_txt.write_text("\n".join(text_lines), encoding="utf-8")

    en_block = ""
    if text_lines_en:
        en_txt = tmp / "endcard_en.txt"
        en_txt.write_text("\n".join(text_lines_en), encoding="utf-8")

    cmd = ["ffmpeg", "-y"]
    cmd += ["-f", "lavfi", "-i", f"color=c=0x2F5233:s={WIDTH}x{HEIGHT}:d={duration}:r={FPS}"]
    if LOGO.exists():
        cmd += ["-loop", "1", "-t", str(duration), "-i", str(LOGO)]
        filter_parts = [
            f"[1:v]scale=320:-1,format=rgba,fade=in:st=0:d=0.4:alpha=1[logo]",
            f"[0:v][logo]overlay=(W-w)/2:260[bg]",
            f"[bg]drawtext=fontfile='{esc_filter_path(FONT_BOLD)}':expansion=none:"
            f"textfile='{esc_filter_path(lines_txt)}':fontcolor=white:fontsize=44:"
            f"line_spacing=14:x=(w-text_w)/2:y=680:alpha='min(1,t/0.4)'[vi]",
        ]
        cur = "vi"
        if text_lines_en:
            en_y = 680 + len(text_lines) * END_CARD_LINE_PITCH + 20
            filter_parts.append(
                f"[{cur}]drawtext=fontfile='{esc_filter_path(FONT_ITALIC)}':expansion=none:"
                f"textfile='{esc_filter_path(en_txt)}':fontcolor=0xCFE0CF:fontsize=30:"
                f"line_spacing=10:x=(w-text_w)/2:y={en_y}:alpha='min(1,t/0.4)'[vout]"
            )
            cur = "vout"
        else:
            filter_parts[-1] = filter_parts[-1].replace("[vi]", "[vout]")
        cmd += ["-filter_complex", ";".join(filter_parts), "-map", "[vout]"]
    else:
        filter_parts = [
            f"drawtext=fontfile='{esc_filter_path(FONT_BOLD)}':expansion=none:"
            f"textfile='{esc_filter_path(lines_txt)}':fontcolor=white:fontsize=44:"
            f"line_spacing=14:x=(w-text_w)/2:y=(h-text_h)/2:alpha='min(1,t/0.4)'"
        ]
        if text_lines_en:
            en_half_offset = (len(text_lines) * END_CARD_LINE_PITCH) / 2 + 20
            filter_parts.append(
                f"drawtext=fontfile='{esc_filter_path(FONT_ITALIC)}':expansion=none:"
                f"textfile='{esc_filter_path(en_txt)}':fontcolor=0xCFE0CF:fontsize=30:"
                f"line_spacing=10:x=(w-text_w)/2:y=(h/2)+{en_half_offset}:alpha='min(1,t/0.4)'"
            )
        cmd += ["-vf", ",".join(filter_parts)]
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
    narration_cfg = config.get("narration")
    music_cfg = config.get("music")
    end_card_lines = config.get("end_card_text", "Nhắn Zalo để đặt hàng").split("\n")
    end_card_text_en = config.get("end_card_text_en")
    end_card_lines_en = end_card_text_en.split("\n") if end_card_text_en else None

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
            trim_clip(src, clip.get("start", 0), duration, seg_path, motion=clip.get("motion", "zoom"))
            segment_paths.append(seg_path)
            durations.append(duration)

        # 2) Nối các clip quy trình bằng crossfade (mượt hơn cắt cứng), rồi
        #    lấy offset tuyệt đối thật của từng clip để canh chữ caption cho
        #    đúng lúc — KHÔNG dùng cộng dồn thô nữa vì crossfade rút ngắn
        #    thời lượng tổng.
        transitioned = tmp / "transitioned.mp4"
        caption_offsets = crossfade_sequence(segment_paths, durations, TRANSITION_SECONDS, transitioned)
        body_duration = ffprobe_duration(transitioned)

        # 2b) Giọng đọc AI (tuỳ chọn) — tạo trước để biết lời đọc dài bao
        #     nhiêu giây, từ đó quyết định thẻ kết thúc có cần kéo dài thêm
        #     không (để lời đọc không bị cắt cụt giữa chừng).
        narration_path = None
        end_card_duration = END_CARD_SECONDS
        if narration_cfg:
            narration_path = tmp / "narration.mp3"
            voice = narration_cfg.get("voice", DEFAULT_VOICE)
            generate_narration(narration_cfg["text"], voice, narration_path)
            narration_duration = ffprobe_duration(narration_path)
            needed_total = narration_duration + 0.3  # đệm nhỏ để lời đọc không bị cắt cụt
            if needed_total > body_duration + end_card_duration:
                extended = needed_total - body_duration
                if extended > MAX_END_CARD_SECONDS:
                    print(
                        f"CẢNH BÁO: lời đọc ({narration_duration:.1f}s) dài hơn nhiều so với video "
                        f"({body_duration:.1f}s) — thẻ kết thúc bị chặn ở {MAX_END_CARD_SECONDS}s, "
                        f"lời đọc có thể bị cắt cụt. Rút ngắn narration.text hoặc thêm clip.",
                        file=sys.stderr,
                    )
                    extended = MAX_END_CARD_SECONDS
                end_card_duration = extended
                print(f"Lời đọc dài hơn video gốc — kéo dài thẻ kết thúc lên {end_card_duration:.1f}s.")

        # 3) Thẻ kết thúc — nối vào bằng cắt cứng (không crossfade), giữ cảm
        #    giác "chốt lại" rõ ràng khi chuyển sang màn hình thương hiệu.
        end_card_path = tmp / "endcard.mp4"
        build_end_card(
            end_card_lines, end_card_path, tmp,
            duration=end_card_duration, text_lines_en=end_card_lines_en,
        )

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
        #    không bị lỗi escape trong ffmpeg filter). Video-only ở bước này
        #    — âm thanh (nếu có lời đọc) được ghép ở bước 5, sau cùng.
        visual_path = tmp / "visual.mp4" if (narration_path or music_cfg) else out_path
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
            stage = 0
            for i, cap in enumerate(captions):
                start_abs = starts_abs[i]
                end_abs = ends_abs[i]
                fade_alpha = (
                    f"if(lt(t,{start_abs}+{TEXT_FADE_SECONDS}),(t-{start_abs})/{TEXT_FADE_SECONDS},"
                    f"if(gt(t,{end_abs}-{TEXT_FADE_SECONDS}),({end_abs}-t)/{TEXT_FADE_SECONDS},1))"
                )
                enable = f"enable='between(t,{start_abs},{end_abs})'"

                # Dòng chữ tiếng Việt (chính) — dải dưới cùng, như cũ.
                txt_file = tmp / f"cap{i}.txt"
                txt_file.write_text(cap["text"], encoding="utf-8")
                stage += 1
                box_out = f"s{stage}"
                filter_lines.append(
                    f"[{cur}]drawbox=x=0:y={HEIGHT-260}:w={WIDTH}:h=260:"
                    f"color=black@0.55:t=fill:{enable}[{box_out}]"
                )
                cur = box_out
                stage += 1
                text_out = f"s{stage}"
                filter_lines.append(
                    f"[{cur}]drawtext=fontfile='{esc_filter_path(FONT_BOLD)}':expansion=none:"
                    f"textfile='{esc_filter_path(txt_file)}':fontcolor=white:fontsize=48:"
                    f"line_spacing=8:x=(w-text_w)/2:y={HEIGHT-190}:"
                    f"alpha='{fade_alpha}':{enable}[{text_out}]"
                )
                cur = text_out

                # Phụ đề tiếng Anh (phụ, tuỳ chọn) — dải ngay phía trên, chữ
                # nhỏ hơn + nghiêng để rõ đây là bản dịch, không phải chữ chính.
                text_en = cap.get("text_en")
                if text_en:
                    en_txt_file = tmp / f"cap{i}_en.txt"
                    en_txt_file.write_text(text_en, encoding="utf-8")
                    en_band_y = HEIGHT - 260 - EN_BAND_HEIGHT
                    stage += 1
                    en_box_out = f"s{stage}"
                    filter_lines.append(
                        f"[{cur}]drawbox=x=0:y={en_band_y}:w={WIDTH}:h={EN_BAND_HEIGHT}:"
                        f"color=black@0.4:t=fill:{enable}[{en_box_out}]"
                    )
                    cur = en_box_out
                    stage += 1
                    en_text_out = f"s{stage}"
                    filter_lines.append(
                        f"[{cur}]drawtext=fontfile='{esc_filter_path(FONT_ITALIC)}':expansion=none:"
                        f"textfile='{esc_filter_path(en_txt_file)}':fontcolor=0xE8E8E8:fontsize=32:"
                        f"line_spacing=6:x=(w-text_w)/2:y={en_band_y + 20}:"
                        f"alpha='{fade_alpha}':{enable}[{en_text_out}]"
                    )
                    cur = en_text_out

            filter_lines.append(f"[{cur}]null[vout]")
            filter_script = tmp / "captions.txt"
            filter_script.write_text(";\n".join(filter_lines), encoding="utf-8")

            run([
                "ffmpeg", "-y", "-i", str(concatenated),
                "-filter_complex_script", str(filter_script),
                "-map", "[vout]",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                str(visual_path),
            ])
        else:
            shutil.copy(concatenated, visual_path)

        # 5) Ghép âm thanh cuối: lời đọc AI (nếu có) + nhạc nền (nếu có) —
        #    video đã được đảm bảo đủ dài ở bước 2b nên không cần cắt lời
        #    đọc. KHÔNG dùng -shortest: nếu lời đọc NGẮN hơn video (hết
        #    trước đoạn thẻ kết thúc), -shortest sẽ cắt cụt mất cả đoạn hình
        #    ảnh còn lại — hình luôn phải chạy hết, phần cuối im lặng (hoặc
        #    chỉ còn nhạc nền) nếu lời đọc đã xong sớm.
        if narration_path and music_cfg:
            music_src = ROOT / music_cfg["file"]
            if not music_src.exists():
                print(f"ERROR: không tìm thấy file nhạc nền: {music_src}")
                sys.exit(1)
            total_duration = body_duration + end_card_duration
            volume = music_cfg.get("volume", MUSIC_VOLUME_DEFAULT)
            fade_out_start = max(0.0, total_duration - MUSIC_FADE_OUT)
            run([
                "ffmpeg", "-y",
                "-i", str(visual_path), "-i", str(narration_path), "-i", str(music_src),
                "-filter_complex",
                (
                    f"[1:a]apad=whole_dur={total_duration}[narr];"
                    f"[2:a]atrim=0:{total_duration},asetpts=PTS-STARTPTS,"
                    f"afade=t=in:st=0:d={MUSIC_FADE_IN},"
                    f"afade=t=out:st={fade_out_start}:d={MUSIC_FADE_OUT},"
                    f"volume={volume}[music];"
                    f"[narr][music]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]"
                ),
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                "-movflags", "+faststart",
                str(out_path),
            ])
        elif narration_path:
            run([
                "ffmpeg", "-y",
                "-i", str(visual_path), "-i", str(narration_path),
                "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                "-movflags", "+faststart",
                str(out_path),
            ])
        elif music_cfg:
            music_src = ROOT / music_cfg["file"]
            if not music_src.exists():
                print(f"ERROR: không tìm thấy file nhạc nền: {music_src}")
                sys.exit(1)
            total_duration = body_duration + end_card_duration
            volume = music_cfg.get("volume", MUSIC_VOLUME_DEFAULT)
            fade_out_start = max(0.0, total_duration - MUSIC_FADE_OUT)
            run([
                "ffmpeg", "-y",
                "-i", str(visual_path), "-i", str(music_src),
                "-filter_complex",
                (
                    f"[1:a]atrim=0:{total_duration},asetpts=PTS-STARTPTS,"
                    f"afade=t=in:st=0:d={MUSIC_FADE_IN},"
                    f"afade=t=out:st={fade_out_start}:d={MUSIC_FADE_OUT},"
                    f"volume={volume}[aout]"
                ),
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                "-movflags", "+faststart",
                str(out_path),
            ])

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
    if shutil.which("ffprobe") is None:
        print("ERROR: không tìm thấy ffprobe trên PATH.")
        sys.exit(1)

    with open(args.config, encoding="utf-8") as f:
        config = json.load(f)

    build_video(config)


if __name__ == "__main__":
    main()
