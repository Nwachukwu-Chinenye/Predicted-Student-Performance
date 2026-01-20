import pandas as pd
import numpy as np
import pickle
import gradio as gr
import tempfile

# ── Load model ──
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception:
    model = None

# Status assignment
def assign_status(score):
    if score < 50:
        return "🔴 At Risk"
    elif score >= 75:
        return "🟢 Excelling"
    else:
        return "🟡 Needs Improvement"

# Study strategies
study_strategies = {
    "Mathematics": "Practice problem sets daily for 30 mins.",
    "Physics": "Focus on concepts and solve numerical exercises.",
    "Chemistry": "Review reactions and practice exercises.",
    "Biology": "Study diagrams and key concepts thoroughly.",
    "English": "Read passages and practice comprehension exercises."
}

REQUIRED_COLS = [
    "quiz_score",
    "assignment_score",
    "attempts",
    "attendance",
    "subject",
    "topic",
    "mastery_level"
]

def predict_and_guide(
    file,
    target_score=None,   # 🔑 target score is now OPTIONAL
    manual_subject="Mathematics",
    manual_quiz_score=65,
    manual_assignment_score=68,
    manual_attempts=2,
    manual_mastery_level="Medium",
    manual_attendance=75,
    manual_topic="Algebra"
):

    if model is None:
        return None, None, "Model not loaded. Retrain and ensure model.pkl exists."

    has_target = target_score is not None  # 🔑 GUARD

    # ── Load data ──
    if file is not None:
        df = pd.read_csv(file.name)
    else:
        df = pd.DataFrame({
            "subject": [manual_subject],
            "topic": [manual_topic or "Unknown"],
            "quiz_score": [manual_quiz_score],
            "assignment_score": [manual_assignment_score],
            "attempts": [manual_attempts],
            "mastery_level": [manual_mastery_level],
            "attendance": [manual_attendance]
        })

    # ── HARD SAFETY FIX ──
    df = df[[c for c in df.columns if c in REQUIRED_COLS]]

    for col in REQUIRED_COLS:
        if col not in df.columns:
            if col in ["quiz_score", "assignment_score", "attendance"]:
                df[col] = 50.0
            elif col == "attempts":
                df[col] = 2
            else:
                df[col] = "Unknown"

    df["subject"] = df["subject"].astype(str)
    df["topic"] = df["topic"].astype(str)
    df["mastery_level"] = df["mastery_level"].astype(str)

    # ── Predict (ALWAYS RUNS) ──
    preds = model.predict(df[REQUIRED_COLS])
    df["Predicted_Final_Score"] = np.round(preds, 2)
    df["Status"] = df["Predicted_Final_Score"].apply(assign_status)

    # ── Advice & Goal Plan ──
    advice_list, goal_list, hours_list = [], [], []

    for _, row in df.iterrows():
        advice, goals = [], []
        score = row["Predicted_Final_Score"]
        study_hours = 0

        if score < 75:
            if row["attendance"] < 70:
                advice.append("Improve attendance.")
            if row["quiz_score"] < 60:
                advice.append("Review quizzes.")
            if row["assignment_score"] < 60:
                advice.append("Improve assignments.")
        else:
            advice.append("Great job so far!")

        if has_target:
            diff = target_score - score
            if diff > 0:
                goals.append(f"Gap to target: +{diff:.1f} points")
                strategy = study_strategies.get(row["subject"], "")
                if strategy:
                    goals.append(f"Strategy: {strategy}")
                study_hours = max(0, diff / 4)
                if study_hours > 0:
                    goals.append(f"Study ~{study_hours:.1f} extra hours/week")

        advice_list.append(" • ".join(advice))
        goal_list.append(" • ".join(goals) if has_target else "No target score provided")
        hours_list.append(round(study_hours, 1) if has_target else 0)

    df["Advice"] = advice_list
    df["Goal_Seeker_Plan"] = goal_list
    df["Extra_Hours_Per_Week_Needed"] = hours_list

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    df.to_csv(temp.name, index=False)

    status_msg = "Prediction completed"
    if has_target:
        status_msg += f" | Target: {target_score}%"

    return df, temp.name, status_msg

# ── UI ──
iface = gr.Interface(
    fn=predict_and_guide,
    inputs=[
        gr.File(label="Upload CSV (optional)"),
        gr.Number(label="Target Score (%)", value=None),
        gr.Dropdown(["Mathematics", "Physics", "Chemistry", "Biology", "English"], value="Mathematics"),
        gr.Number(value=65),
        gr.Number(value=68),
        gr.Number(value=2),
        gr.Dropdown(["Low", "Medium", "High"], value="Medium"),
        gr.Number(value=75),
        gr.Textbox(value="Algebra")
    ],
    outputs=[
        gr.Dataframe(),
        gr.File(),
        gr.Textbox()
    ],
    title="🎓 Student Goal Seeker & Predictor"
)

iface.launch()
