import numpy as np
import pandas as pd
import random

# Reproducibility
np.random.seed(42)
random.seed(42)

N_STUDENTS = 2000

# Nigerian names
FIRST_NAMES = [
    "Chinedu", "Amina", "Tunde", "Sola", "Ibrahim", "Blessing",
    "Emeka", "Zainab", "Yusuf", "Ngozi", "Samuel", "Funke",
    "Abdul", "Halima", "David", "Esther", "Musa", "Maryam",
    "Daniel", "Peace", "Joseph", "Ngozi", "Ifeoma", "Nnamdi",
    "Emeka", "Chiamaka", "Chibuzo", "Nkiru", "Chukwuka", 
    "Ifeanyi", "Amarachi"
]

LAST_NAMES = [
    "Okafor", "Balogun", "Abdullahi", "Adebayo", "Mohammed",
    "Okoye", "Sule", "Lawal", "Ahmed", "Onyekachi",
    "Olatunji", "Danladi", "Ibrahim", "Adesina", "Yakubu",
    "Sadiq", "Kabiru", "Bashir", "Abdul", "Ibrahim", "Musa", "Sule"
]

# Subjects and topics
SUBJECTS = ["Mathematics", "Physics", "Chemistry", "Biology", "English"]

TOPICS = {
    "Mathematics": ["Algebra", "Geometry", "Calculus", "Probability"],
    "Physics": ["Mechanics", "Optics", "Thermodynamics"],
    "Chemistry": ["Organic", "Inorganic", "Physical"],
    "Biology": ["Genetics", "Ecology", "Anatomy"],
    "English": ["Grammar", "Comprehension", "Vocabulary"]
}

MASTERY_MAP = {"Low": 0, "Medium": 50, "High": 80}

records = []

for student_id in range(1, N_STUDENTS + 1):

    student_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    subject = random.choice(SUBJECTS)
    topic = random.choice(TOPICS[subject])

    quiz_score = round(np.clip(np.random.normal(65, 12), 0, 100), 2)
    assignment_score = round(np.clip(np.random.normal(68, 15), 0, 100), 2)
    attendance = round(np.clip(np.random.normal(75, 10), 40, 100), 2)

    attempts = random.randint(1, 4)
    mastery_level = random.choices(
        ["Low", "Medium", "High"],
        weights=[0.3, 0.5, 0.2]
    )[0]

    mastery_numeric = MASTERY_MAP[mastery_level]

    # Final exam score (realistic academic weighting)
    final_exam_score = (
        0.30 * quiz_score +
        0.30 * assignment_score +
        0.15 * attendance +
        0.10 * mastery_numeric +
        0.15 * (attempts * 10)
    )

    final_exam_score += np.random.normal(0, 5)
    final_exam_score = round(np.clip(final_exam_score, 0, 100), 2)

    records.append([
        student_id,
        student_name,
        subject,
        topic,
        quiz_score,
        assignment_score,
        attempts,
        mastery_level,
        attendance,
        final_exam_score
    ])

# Create DataFrame
df = pd.DataFrame(records, columns=[
    "student_id",
    "student_name",
    "subject",
    "topic",
    "quiz_score",
    "assignment_score",
    "attempts",
    "mastery_level",
    "attendance",
    "final_exam_score"
])

# Save dataset
df.to_csv("training_data.csv", index=False)

print("✅ Clean, rounded, Nigerian student dataset generated → training_data.csv")
