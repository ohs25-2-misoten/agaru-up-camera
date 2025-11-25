import os
import glob
import subprocess
import datetime

# ====== 設定 ======
# camera.py で保存したフォルダを指定
VIDEO_DIR = os.path.join(os.getcwd(), "webcam_videos_py")
FILE_PATTERN = "video_*.mp4"          # 対象ファイル名パターン
N_CLIPS = 30                          # 結合する動画数（1ファイル1秒なら30個で30秒分）
OUTPUT_DIR = os.getcwd()              # 出力先（現在のディレクトリ）
OUTPUT_FILENAME = "combined_video"    # 出力ファイル名の接頭辞

# ====== ステップ1: 最新N個のファイルを取得 ======
# ファイル一覧をフルパスで取得
search_path = os.path.join(VIDEO_DIR, FILE_PATTERN)
video_files = sorted(glob.glob(search_path))

# 必要なファイル数チェック（結合数 + 書き込み中の最新1つを除外するための1）
required_files = N_CLIPS + 1

if len(video_files) < 2:
    print("❌ 結合するための動画ファイルが足りません（最低2つ必要です）。")
    exit()

# ファイルが十分にある場合と、足りない場合の処理分け
if len(video_files) < required_files:
    print(f"⚠ 指定された {N_CLIPS}個 に満たないため、現在ある分（最新除く）だけで結合します。")
    latest_files = video_files[:-1]  # 最新の1つだけ除外して残りを全部使う
else:
    # 古い方から並んでいるので、後ろからスライスして取得
    # 例: [-31 : -1] -> 最新の1つ(書き込み中)を除外した、直近の30個を取得
    latest_files = video_files[-(N_CLIPS + 1):-1]

print(f"対象ファイル数: {len(latest_files)}個")
print(f"期間: {os.path.basename(latest_files[0])} 〜 {os.path.basename(latest_files[-1])}")

# ====== ステップ2: ffmpeg用リストファイルの作成 ======
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
list_path = os.path.join(OUTPUT_DIR, f"filelist_{timestamp}.txt")

with open(list_path, "w") as f:
    for path in latest_files:
        # ffmpegのconcatリスト形式: file '/path/to/file.mp4'
        f.write(f"file '{path}'\n")

# ====== ステップ3: 結合出力ファイル名の生成 ======
output_file = os.path.join(OUTPUT_DIR, f"{OUTPUT_FILENAME}_{timestamp}.mp4")

# ====== ステップ4: ffmpegで結合 ======
# -f concat : 結合モード
# -safe 0 : パス名の制限を緩和
# -c copy : 再エンコードなし（ストリームコピー）で高速結合
cmd = [
    "ffmpeg",
    "-f", "concat",
    "-safe", "0",
    "-i", list_path,
    "-c", "copy",
    "-y",  # 上書き許可
    output_file
]

try:
    print("🔄 結合処理中...")
    # stdout, stderrをDEVNULLに捨ててログをスッキリさせる（エラー時は例外キャッチへ）
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ 結合完了: {output_file}")
except subprocess.CalledProcessError as e:
    print("❌ ffmpegでの結合に失敗しました。")
    # デバッグ用にエラーコマンドを表示
    print(f"Command: {' '.join(cmd)}")

# ====== ステップ5: 後始末 ======
# 一時作成したリストファイルを削除
if os.path.exists(list_path):
    os.remove(list_path)
    print("🗑️ 一時ファイルを削除しました。")