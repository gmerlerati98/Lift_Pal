from fastapi import APIRouter, UploadFile, File, HTTPException
from app.storage.local_storage import save_video
from app.services.pose_analysis import analyze_frames
from app.services.lift_feedback import analyze_lift_feedback
from app.config.lift_joints import LIFT_LANDMARKS

router = APIRouter()

@router.post("/analyze/{lift_type}")
async def analyze_lift(lift_type: str, video: UploadFile = File(...)):
    # Validate lift type
    if lift_type not in LIFT_LANDMARKS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid lift type. Available types: {', '.join(LIFT_LANDMARKS.keys())}"
        )

    # Save uploaded video
    file_path = save_video(video)

    # Run pose analysis with optimized sampling
    # This is the line you asked about:
    pose_data = analyze_frames(file_path, lift_type, sample_rate=0.2)

    # Generate lift-specific feedback
    feedback = analyze_lift_feedback(pose_data, lift_type)

    return {
        "message": f"Pose analysis completed for {lift_type}",
        "file_path": file_path,
        "frames_analyzed": len(pose_data),
        "landmarks": pose_data,
        "feedback": feedback
    }
