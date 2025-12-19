#!/bin/bash
set -e
set -o pipefail

# Ctrl+CやSIGQUITで中断された場合の処理（録画を終了して正常終了メッセージを表示）
trap 'echo "Terminating recording..."; exit 0' SIGINT SIGQUIT

# スクリプトのディレクトリを取得
SCRIPT_DIR=$(cd "$(dirname "$0")" ; pwd)

# .env ファイルを読み込む
ENV_FILE="$SCRIPT_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: .env file not found: $ENV_FILE"
    exit 1
fi
set -a
source "$ENV_FILE"
set +a

# デバイス確認
if [ ! -e "$VIDEO_DEVICE" ]; then
    echo "Error: Video device $VIDEO_DEVICE not found"
    exit 1
fi

# ディレクトリ作成
mkdir -p "$RECORDING_DIR"

echo "Starting recording..."
echo "Segment duration: ${SEGMENT_TIME}s, Total lookback: $((SEGMENT_TIME * MAX_SEGMENTS))s"

ffmpeg \
    -f v4l2 -thread_queue_size 8192 -input_format mjpeg -s "$VIDEO_RESOLUTION" -framerate "$VIDEO_FRAMERATE" -i "$VIDEO_DEVICE" \
    -c:v h264_v4l2m2m -pix_fmt yuv420p -b:v "$VIDEO_BITRATE" -g "$VIDEO_FRAMERATE" \
    -f segment -segment_time "$SEGMENT_TIME" -segment_format mp4 -segment_wrap "$MAX_SEGMENTS" \
    -segment_list "$RECORDING_DIR/out.ffconcat" -segment_list_size "$MAX_SEGMENTS" -reset_timestamps 1 \
    "$RECORDING_DIR/segment_%03d.mp4"

# エラーハンドリング
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FFmpeg process terminated with error (exit code: $EXIT_CODE)"
    exit $EXIT_CODE
fi
