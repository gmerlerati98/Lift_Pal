from fastapi import APIRouter, UploadFile, File
from app.storage.local_storage import save_video
from app.services.video_processing import extract_frames

router = APIRouter()

@router.post("/analyze")
async def analyze_lift(video: UploadFile = File(...)):
    # Save uploaded video
    file_path = save_video(video)
    
    # Extract frames
    num_frames = extract_frames(file_path)
    
    # Return response
    return {
        "message": "Video uploaded and frames extracted successfully!",
        "file_path": file_path,
        "num_frames": num_frames,
        "feedback": [
            "This is a placeholder feedback message.",
            "Pose analysis will be available after implementation."
        ]
    }
