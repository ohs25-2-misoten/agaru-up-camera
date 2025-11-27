from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import glob
import subprocess
import datetime

app = FastAPI()

# ====== 設定 ======
VIDEO_DIR = os.path.join(os.getcwd(), "webcam_videos_py")   # 上の recorder と同じ
FILE_PATTERN = "video_*.mp4"
OUTPUT_DIR = "/tmp"                                          # 一時出力先
OUTPUT_PREFIX = "combined"

# ====== API: 最新N秒間の動画を返す ======
@app.get("/videos")
async def get_video(time: int):
    if time <= 0:
        raise HTTPException(status_code=400, detail="time must be positive integer")

    # N秒 = N個のファイル（1ファイル1秒）
    N_CLIPS = time

    # 動画ファイル一覧
    files = sorted(glob.glob(os.path.join(VIDEO_DIR, FILE_PATTERN)))

    if len(files) < 2:
        raise HTTPException(status_code=500, detail="Not enough video files to combine")

    # 最新の1つ（書き込み中）を除外して N_CLIPS 取得
    if len(files) < N_CLIPS + 1:
        latest_files = files[:-1]
    else:
        latest_files = files[-(N_CLIPS + 1):-1]

    if len(latest_files) == 0:
        raise HTTPException(status_code=500, detail="No valid video files available")

    # ffmpeg のリストファイル生成
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    list_path = os.path.join(OUTPUT_DIR, f"filelist_{timestamp}.txt")

    with open(list_path, "w") as f:
        for p in latest_files:
            f.write(f"file '{p}'\n")

    output_path = os.path.join(OUTPUT_DIR, f"{OUTPUT_PREFIX}_{timestamp}.mp4")

    # ffmpeg 実行（再エンコードなし）
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", list_path,
        "-c", "copy",
        "-y",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        raise HTTPException(status_code=500, detail="ffmpeg concat failed")
    finally:
        if os.path.exists(list_path):
            os.remove(list_path)

    return FileResponse(output_path, media_type="video/mp4", filename="combined.mp4")
