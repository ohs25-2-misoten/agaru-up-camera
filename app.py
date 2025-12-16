import subprocess
import os
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

@app.get("/videos")
def get_videos(time: int, background_tasks: BackgroundTasks):
    """
    指定された秒数分の動画を結合して返す

    Args:
        time: 動画の長さ（秒単位、1～120秒）
        background_tasks: バックグラウンドタスク

    Returns:
        MP4動画ファイル
    """

    max_time = 120

    # 秒数のバリデーション
    if time < 1:
        raise HTTPException(status_code=400, detail="秒数は1以上で指定してください")

    if time > max_time:
        raise HTTPException(status_code=400, detail=f"秒数は最大{max_time}秒です")

    # スクリプトディレクトリを取得
    script_dir = Path(__file__).parent.resolve()
    combine_script = script_dir / "combine_segments.sh"

    if not combine_script.exists():
        raise HTTPException(status_code=500)

    # 出力ファイル名を生成（lookback_YYYYMMDD_HHMMSS.mp4）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"lookback_{timestamp}.mp4"
    output_path = script_dir / output_filename

    try:
        # combine_segments.shを実行
        result = subprocess.run(
            ["bash", str(combine_script), str(time), str(output_path)],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode != 0:
            raise HTTPException(status_code=500)

        # ファイルが存在することを確認
        if not output_path.exists():
            raise HTTPException(status_code=500)

        # ファイルをレスポンスで返す
        return FileResponse(
            path=output_path,
            media_type="video/mp4",
            filename=output_filename,
            background=BackgroundTasks(os.remove, str(output_path))
        )

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="リクエストがタイムアウトしました")
    except Exception as e:
        raise HTTPException(status_code=500)
