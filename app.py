import subprocess
import os
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

@app.get("/videos")
def get_videos(time: int, background_tasks: BackgroundTasks):
    """
    指定された秒数分の動画を結合して返す

    Args:
        time: 動画の長さ（秒単位、1～60秒）
        background_tasks: バックグラウンドタスク

    Returns:
        MP4動画ファイル
    """

    # 秒数のバリデーション
    if time < 1:
        return {"error": "秒数は1以上で指定してください"}

    if time > 120:
        return {"error": "秒数は最大120秒です"}

    # スクリプトディレクトリを取得
    script_dir = Path(__file__).parent.resolve()
    combine_script = script_dir / "combine_segments.sh"

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
            return {"error": "動画の結合に失敗しました", "details": result.stderr}

        # ファイルが存在することを確認
        if not output_path.exists():
            return {"error": "出力ファイルが生成されませんでした"}

        # バックグラウンドタスクにファイル削除を追加
        background_tasks.add_task(os.remove, str(output_path))

        # ファイルをレスポンスで返す
        return FileResponse(
            path=output_path,
            media_type="video/mp4",
            filename=output_filename
        )

    except subprocess.TimeoutExpired:
        return {"error": "動画の結合がタイムアウトしました"}
    except Exception as e:
        return {"error": f"エラーが発生しました: {str(e)}"}
