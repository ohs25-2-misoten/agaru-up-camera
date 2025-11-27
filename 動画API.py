from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from picamera2 import Picamera2
import time
import os

app = FastAPI()

camera = Picamera2()

@app.get("/videos")
async def get_video(time: int):
    # time が 0 以下などの場合
    if time <= 0:
        raise HTTPException(status_code=400, detail="time must be positive integer")

    filepath = "/tmp/output.mp4"

    # 既存ファイルがあれば削除
    if os.path.exists(filepath):
        os.remove(filepath)

    # カメラ録画スタート
    camera.start_recording(filepath)
    time.sleep(time)
    camera.stop_recording()

    # 動画ファイルを返す
    return FileResponse(
        filepath,
        media_type="video/mp4",
        filename="recorded.mp4"
    )
