#!/usr/bin/env bash
# Dựng lại hàng loạt video theo configs/ rồi xuất bản nhẹ cho website (docs/assets/).
# Viết 2026-10-19 khi đổi thương hiệu sang THOC. Chạy từ Git Bash:
#   bash content/video/dung_lai_va_xuat_web.sh                 # tất cả config
#   bash content/video/dung_lai_va_xuat_web.sh slug1 slug2      # chỉ vài video
# Máy yếu: chạy TUẦN TỰ từng video, mỗi video vài phút. Log ở content/video/output/dung_lai.log
set -u
cd "$(dirname "$0")"
PY=/c/Users/Admin/AppData/Local/Python/bin/python.exe
WEB=../../docs/assets
LOG=output/dung_lai.log
mkdir -p output

# slug config -> tên file trên website (chỉ những video website đang dùng)
web_name() {
  case "$1" in
    quy-trinh-say-san-day) echo san-day-quy-trinh-say ;;
    quy-trinh-dao-cu-may-xuc) echo san-day-thu-hoach ;;
    cam-duongcanh-ham-nong|cam-vuon-mua-truoc|san-day-buoi-sang-tren-nuong|san-day-cu-tuoi|\
    san-day-gioi-thieu-xuat-khau|san-day-hanh-trinh-day-du|gioi-thieu-thoc|gioi-thieu-thoc-en) echo "$1" ;;
    *) echo "" ;;
  esac
}

if [ $# -gt 0 ]; then SLUGS="$*"; else SLUGS=$(ls configs/*.json | xargs -n1 basename | sed 's/\.json$//'); fi

for s in $SLUGS; do
  echo "=== $(date +%H:%M) dựng $s" | tee -a "$LOG"
  if ! "$PY" make_process_video.py --config "configs/$s.json" >> "$LOG" 2>&1; then
    echo "!!! LỖI khi dựng $s (xem $LOG)" | tee -a "$LOG"; continue
  fi
  w=$(web_name "$s")
  [ -z "$w" ] && continue
  W=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "output/$s.mp4")
  if [ "$W" -gt 1500 ]; then SCALE=1280:720; else SCALE=540:960; fi
  ffmpeg -v error -y -i "output/$s.mp4" -vf "scale=$SCALE" -c:v libx264 -crf 28 -preset medium \
    -c:a aac -b:a 96k -movflags +faststart "$WEB/$w.mp4" >> "$LOG" 2>&1
  if [ "$s" = san-day-gioi-thieu-xuat-khau ]; then  # bản nhẹ để gửi email
    ffmpeg -v error -y -i "output/$s.mp4" -vf "scale=480:854" -c:v libx264 -crf 30 -preset medium \
      -c:a aac -b:a 80k -movflags +faststart "$WEB/$w-email.mp4" >> "$LOG" 2>&1
  fi
  echo "    -> web: $WEB/$w.mp4 ($(du -h "$WEB/$w.mp4" | cut -f1))" | tee -a "$LOG"
done
echo "=== $(date +%H:%M) XONG" | tee -a "$LOG"
