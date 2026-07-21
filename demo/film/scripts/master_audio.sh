#!/bin/bash
# Two-pass -14 LUFS / -1 dBTP loudness master. Video stream is copied untouched.
# Usage: master_audio.sh <in.mp4> <out.mp4>
set -e
IN="$1"; OUT="$2"
STATS=$(ffmpeg -hide_banner -i "$IN" -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
II=$(echo "$STATS"  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['input_i'])")
TP=$(echo "$STATS"  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['input_tp'])")
LRA=$(echo "$STATS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['input_lra'])")
TH=$(echo "$STATS"  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['input_thresh'])")
OFF=$(echo "$STATS" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['target_offset'])")
echo "measured: I=$II TP=$TP LRA=$LRA"
ffmpeg -y -v error -i "$IN" \
  -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$II:measured_TP=$TP:measured_LRA=$LRA:measured_thresh=$TH:offset=$OFF:linear=true" \
  -c:v copy -c:a aac -b:a 256k -movflags +faststart "$OUT"
echo "master written: $OUT"
ffmpeg -hide_banner -i "$OUT" -af loudnorm=I=-14:TP=-1:print_format=summary -f null - 2>&1 | grep -A2 "Input Integrated" | head -3
