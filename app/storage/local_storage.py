import os
import shutil
from fastapi import UploadFile

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_video(video: UploadFile) -> str:
    """Save uploaded video to disk and return the file path."""
    file_path = os.path.join(UPLOAD_FOLDER, video.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    return file_path
