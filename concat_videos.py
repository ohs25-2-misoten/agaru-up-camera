# concut_videos.py
import os
import glob
import subprocess
import datetime

def concat_latest_videos(N_CLIPS=30, VIDEO_DIR=None, OUTPUT_DIR=None, OUTPUT_FILENAME="combined_video"):
    """
    最新N_CLIPS個の動画を結合して1本の動画にする
    return: 結合後のファイルパスと実行したcmd
    """
    if VIDEO_DIR is None:
        VIDEO_DIR = os.path.join(os.getcwd(), "webcam_videos_py")
    if OUTPUT_DIR is None:
        OUTPUT_DIR = os.getcwd()

    FILE_PATTERN = "video_*.mp4"

    # 最新N個のファイルを取得
    search_path = os.path.join(VIDEO_DIR, FILE_PATTERN)
    video_files = sorted(glob.glob(search_path))
    required_files = N_CLIPS + 1

    if len(video_files) < 2:
        raise Exception("結合する動画ファイルが足りません（最低2つ必要です）")

    if len(video_files) < required_files:
        latest_files = video_files[:-1]
    else:
        latest_files = video_files[-(N_CLIPS + 1):-1]

    if len(latest_files) == 0:
        raise Exception("結合対象の動画がありません")

    # ffmpeg用リストファイル作成
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    list_path = os.path.join(OUTPUT_DIR, f"filelist_{timestamp}.txt")
    with open(list_path, "w") as f:
        for path in latest_files:
            f.write(f"file '{path}'\n")

    # 出力ファイル名
    output_file = os.path.join(OUTPUT_DIR, f"{OUTPUT_FILENAME}_{timestamp}.mp4")

    # ffmpegコマンド
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", list_path,
        "-c", "copy",
        "-y",
        output_file
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise Exception("ffmpegでの結合に失敗しました")
    finally:
        if os.path.exists(list_path):
            os.remove(list_path)

    return output_file, cmd
