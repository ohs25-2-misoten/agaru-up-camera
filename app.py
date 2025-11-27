from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from concat_videos import concat_latest_videos

app = FastAPI()

@app.get("/videos")
async def get_video(time: int):
    if time <= 0:
        raise HTTPException(status_code=400, detail="time must be positive integer")

    try:
        output_file = concat_latest_videos(N_CLIPS=time)
        #print("実行コマンド:", " ".join(cmd))  # 必要に応じてログに表示
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return FileResponse(output_file, media_type="video/mp4", filename="combined.mp4")
