#!/bin/bash

# 使用法: ./combine_segments.sh <秒数> [出力ファイル名]
# 例: ./combine_segments.sh 30 output.mp4

# スクリプトのディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RECORDING_DIR="${SCRIPT_DIR}/recordings"

# 引数チェック
if [ $# -lt 1 ]; then
    echo "使用方法: $0 <秒数> [出力ファイル名]"
    echo "例: $0 30 output.mp4"
    echo ""
    echo "引数:"
    echo "  <秒数>          : 結合する動画の長さ（秒単位、最大120秒）"
    echo "  [出力ファイル名]: 出力MP4ファイル名（省略時: lookback_YYYYMMDD_HHMMSS.mp4）"
    exit 1
fi

DURATION=$1
OUTPUT_FILE="${2:-lookback_$(date +%Y%m%d_%H%M%S).mp4}"

# 入力値の検証
if ! [[ "$DURATION" =~ ^[0-9]+$ ]]; then
    echo "エラー: 秒数は正の整数で指定してください"
    exit 1
fi

if [ "$DURATION" -le 0 ]; then
    echo "エラー: 秒数は1以上で指定してください"
    exit 1
fi

if [ "$DURATION" -gt 120 ]; then
    echo "警告: 秒数は最大120秒です。120秒に調整します"
    DURATION=120
fi

# セグメント時間と必要なセグメント数を計算
SEGMENT_TIME=1
REQUIRED_SEGMENTS=$DURATION

# ディレクトリ確認
if [ ! -d "$RECORDING_DIR" ]; then
    echo "エラー: 録画ディレクトリが見つかりません: $RECORDING_DIR"
    exit 1
fi

# out.ffconcatファイルを使用
FFCONCAT_FILE="$RECORDING_DIR/out.ffconcat"

# out.ffconcatが存在するか確認
if [ ! -f "$FFCONCAT_FILE" ]; then
    echo "エラー: ffconcatファイルが見つかりません: $FFCONCAT_FILE"
    exit 1
fi

# out.ffconcatから指定秒数分のセグメントを抽出
TEMP_FILELIST="${RECORDING_DIR}/.tmp_filelist_$(date +%s%N)_$$.txt"
trap "rm -f $TEMP_FILELIST" EXIT

# out.ffconcatの内容から"file"行を抽出し、最後の$REQUIRED_SEGMENTS個を取得
grep "^file " "$FFCONCAT_FILE" | tail -n "$REQUIRED_SEGMENTS" > "$TEMP_FILELIST"

# ファイルが存在するか確認
if [ ! -s "$TEMP_FILELIST" ]; then
    echo "エラー: 結合するセグメントが見つかりません"
    exit 1
fi

# 動画を結合
echo "結合処理を開始します..."
ffmpeg -f concat -safe 0 -i "$TEMP_FILELIST" -c copy -y "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "結合完了: $OUTPUT_FILE"
    ls -lh "$OUTPUT_FILE"
else
    echo "結合処理に失敗しました"
    exit 1
fi
