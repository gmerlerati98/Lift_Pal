from app.services.rep_analysis import (
    aggregate_squat_reps,
    aggregate_bench_reps,
    aggregate_deadlift_reps
)

def analyze_lift_feedback(pose_data, lift_type):
    if lift_type == "squat":
        return aggregate_squat_reps(pose_data)
    elif lift_type == "bench":
        return aggregate_bench_reps(pose_data)
    elif lift_type == "deadlift":
        return aggregate_deadlift_reps(pose_data)
    return [{"frames": list(pose_data.keys()), "message": "Feedback not implemented"}]
