import cv2
import datetime
import os
import time
import glob

# --- 設定 ---
OUTPUT_DIR = "webcam_videos_py"  # 保存先フォルダ
WIDTH = 1280
HEIGHT = 720
FPS = 30.0
DURATION = 1  # ファイル分割間隔（秒）
MAX_FILES = 600  # 【追加】保存するファイルの最大数

# フォルダがなければ作成
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- カメラ初期化 (エラー対策済み) ---
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.CAP_PROP_FPS, FPS)

actual_fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Camera initialized: {WIDTH}x{HEIGHT} @ {actual_fps}fps")

# コーデック設定
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

def get_output_filename():
    now = datetime.datetime.now()
    filename = now.strftime("video_%Y%m%d_%H%M%S.mp4")
    return os.path.join(OUTPUT_DIR, filename)

def cleanup_old_files():
    """
    フォルダ内のmp4ファイルを確認し、MAX_FILESを超えていたら古いものから削除する
    """
    # フォルダ内の動画ファイル一覧を取得（作成日時順に並べ替える必要はないが、名前が日付なので名前順＝日付順になる）
    files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "video_*.mp4")))
    
    # ファイル数が上限を超えている場合
    while len(files) >= MAX_FILES:
        oldest_file = files[0] # リストの先頭が一番古い（sorted済みのため）
        try:
            os.remove(oldest_file)
            print(f"[Cleanup] Deleted: {oldest_file}")
            files.pop(0) # リストからも削除して再チェック
        except OSError as e:
            print(f"Error deleting file: {e}")
            break

writer = None
start_time = time.time()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("フレームの取得に失敗しました (Retrying...)")
            time.sleep(0.1)
            continue

        current_time = time.time()

        # ファイル分割タイミング
        if writer is None or (current_time - start_time) >= DURATION:
            # 古いライターを閉じる
            if writer is not None:
                writer.release()
            
            # 【追加】新しいファイルを作る前に、古いファイルを削除して容量を空ける
            cleanup_old_files()
            
            # 新しいファイル作成
            output_path = get_output_filename()
            writer = cv2.VideoWriter(output_path, fourcc, actual_fps, (WIDTH, HEIGHT))
            start_time = current_time
            print(f"Recording: {output_path}")

        writer.write(frame)

except KeyboardInterrupt:
    print("\n録画を停止します")

finally:
    if writer is not None:
        writer.release()
    cap.release()
    cv2.destroyAllWindows()