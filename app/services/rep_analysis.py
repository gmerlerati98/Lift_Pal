from collections import Counter

def aggregate_squat_reps(pose_data):
    """
    Aggregate frame-based squat feedback into reps.
    Uses hip y-coordinate movement to detect reps.
    """
    reps = []
    current_rep = {"frames": [], "messages": []}
    descending = False
    threshold = 0.01
    previous_hip_y = None

    for frame_name, joints in pose_data.items():
        left_hip = joints.get("LEFT_HIP")
        right_hip = joints.get("RIGHT_HIP")
        if not left_hip or not right_hip:
            continue

        hip_y = (left_hip["y"] + right_hip["y"]) / 2

        if previous_hip_y is None:
            previous_hip_y = hip_y
            continue

        # Detect descent
        if hip_y - previous_hip_y > threshold:
            descending = True
        # Detect ascent (rep finished)
        elif descending and hip_y - previous_hip_y < -threshold:
            descending = False
            if current_rep["frames"]:
                reps.append({
                    "frames": current_rep["frames"],
                    "message": summarize_rep_feedback(current_rep["messages"])
                })
                current_rep = {"frames": [], "messages": []}

        # Add frame to current rep
        current_rep["frames"].append(frame_name)
        # Simple per-frame feedback
        if hip_y > previous_hip_y:  
            current_rep["messages"].append("Going down")
        else:
            current_rep["messages"].append("Coming up")

        previous_hip_y = hip_y

    # Add last rep if any
    if current_rep["frames"]:
        reps.append({
            "frames": current_rep["frames"],
            "message": summarize_rep_feedback(current_rep["messages"])
        })

    return reps

def summarize_rep_feedback(messages):
    """
    Summarize a list of frame messages into a single rep message.
    Currently returns the most frequent message.
    """
    if not messages:
        return "No feedback"
    most_common = Counter(messages).most_common(1)[0][0]
    return most_common


# Placeholder for bench and deadlift reps
def aggregate_bench_reps(pose_data):
    reps = []
    # simple placeholder logic
    for frame_name in pose_data.keys():
        reps.append({"frames": [frame_name], "message": "Bench rep feedback placeholder"})
    return reps

def aggregate_deadlift_reps(pose_data):
    reps = []
    # simple placeholder logic
    for frame_name in pose_data.keys():
        reps.append({"frames": [frame_name], "message": "Deadlift rep feedback placeholder"})
    return reps
