import cv2
import os

FRAME_FOLDER = "extracted_frames"
os.makedirs(FRAME_FOLDER, exist_ok=True)

def extract_frames(video_path: str, step: int = 5) -> int:
    """Extract every `step`th frame from a video and save them to a subfolder."""
    if not os.path.exists(video_path):
        return 0

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_frame_folder = os.path.join(FRAME_FOLDER, video_name)
    os.makedirs(video_frame_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return 0

    count = 0
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % step == 0:
            frame_path = os.path.join(video_frame_folder, f"frame_{count:04d}.jpg")
            cv2.imwrite(frame_path, frame)
            count += 1

        frame_idx += 1

    cap.release()
    return count
