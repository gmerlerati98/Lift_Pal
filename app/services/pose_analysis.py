import cv2
import mediapipe as mp
from app.config.lift_joints import LANDMARKS, LIFT_LANDMARKS

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, model_complexity=2)

def analyze_frames(video_path: str, lift_type: str, sample_rate: float = 0.2):
    """
    Optimized frame processing for lifts.

    Parameters:
    - video_path: path to uploaded video
    - lift_type: 'squat', 'bench', or 'deadlift'
    - sample_rate: seconds between frames to process

    Returns:
    - dict with frame_name -> filtered landmarks
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(1, int(fps * sample_rate))  # skip frames

    frame_count = 0
    results_data = {}

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Skip frames according to sample_rate
        if frame_count % frame_interval != 0:
            frame_count += 1
            continue

        frame_name = f"frame_{frame_count:04d}.jpg"

        # Convert to RGB and resize for faster processing
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb = cv2.resize(image_rgb, (640, 480))

        results = pose.process(image_rgb)

        if results.pose_landmarks:
            selected = {}
            for idx, name in [(i, k) for k, i in LANDMARKS.items() if i in LIFT_LANDMARKS[lift_type]]:
                lm = results.pose_landmarks.landmark[idx]
                selected[name] = {
                    "x": lm.x,
                    "y": lm.y,
                    "z": lm.z,
                    "visibility": lm.visibility
                }
            results_data[frame_name] = selected

        frame_count += 1

    cap.release()
    return results_data
