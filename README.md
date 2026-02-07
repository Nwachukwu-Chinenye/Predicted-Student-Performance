# 🎓 Student Performance Predictor & Goal Setter

A machine learning-powered web application that predicts students' final exam scores and provides personalized study recommendations to help them achieve their target grades.

---

## 📌 Overview

This project predicts a student’s **final exam score (0–100)** using historical academic performance data and offers **goal-oriented study guidance**.

The model takes into account:

- Quiz scores
- Assignment scores
- Attendance percentage
- Number of quiz/assignment attempts
- Subject and topic
- Self-reported mastery level (Low / Medium / High)

The system then:
- Predicts the final exam score
- Assigns a performance status:
  - 🔴 **At Risk** (< 50)
  - 🟡 **Needs Improvement** (50–74)
  - 🟢 **Excelling** (≥ 75)
- If a **target score** is provided:
  - Calculates the performance gap
  - Estimates extra study hours per week
  - Recommends subject-specific study strategies

The application supports **both single-student manual input and batch predictions via CSV upload**, using an interactive web interface built with **Gradio**.

---

## ✨ Features

- Single-student prediction using form inputs
- Batch prediction via CSV upload
- Performance classification with visual emoji indicators
- Subject-specific study recommendations
- Goal-based planning with gap analysis
- Estimated extra study hours per week
- Downloadable prediction results as CSV
- Trained on **synthetic but realistic student performance data**

---

## 🖼️ Demo

*(Add screenshots or a demo video link here)*

**Example Output (Single Student):**

| Predicted Score | Status              | Advice                              | Goal Plan (Target = 85) |
|-----------------|---------------------|-------------------------------------|--------------------------|
| 62.4            | 🟡 Needs Improvement | Improve attendance and assignments  | Gap: +22.6 points<br>Study ~5.7 extra hours/week<br>Strategy: Practice problem sets daily for 30 mins |

---

## 🚀 Installation & Quick Start


# 1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/student-performance-predictor.git
cd student-performance-predictor
```

# 2. (Recommended) Create and activate a virtual environment
```bash
python -m venv venv
```

# Windows
```bash
venv\Scripts\activate
```

# macOS / Linux
```bash
source venv/bin/activate
```

# 3. Install dependencies
```bash
pip install -r requirements.txt
```

# 4. (Optional) Generate synthetic training data
```bash
python generate_training_data.py
```

# 5. Train the machine learning model
```bash
python train_model.py
```
# Expected evaluation metrics:
# R² Score: 0.89 – 0.92
# MAE:      3.2 – 4.1 points

# 6. Launch the application
```bash
python app.py
```

## 🌐 Running the Application

Open your browser and visit:  
👉 http://127.0.0.1:7860

---

## 📁 Project Structure

```text
student-performance-predictor/
├── app.py                    # Gradio interface & prediction logic
├── train_model.py            # Model training script
├── generate_training_data.py # Synthetic dataset generator
├── model.pkl                 # Trained machine learning model
├── training_data.csv         # Generated training dataset
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## 🧾 Input Requirements

### Required Fields (Manual Input or CSV Upload)

- **subject**  
  Mathematics, Physics, Chemistry, Biology, English

- **topic**  
  e.g., Algebra, Mechanics, Organic Chemistry

- **quiz_score**  
  0–100

- **assignment_score**  
  0–100

- **attendance**  
  0–100

- **attempts**  
  Positive integer, typically 1–4, representing quiz/assignment attempts

- **mastery_level**  
  Low, Medium, High

### Optional CSV Columns

- **student_id**
- **student_name**

> These identifiers are preserved in the output but are **not used for model prediction**.

---

## 🤖 Model Details

### Algorithm
- **RandomForestRegressor**

### Why Random Forest?
Random Forest was chosen because it:
- Handles non-linear relationships effectively
- Works well with mixed numerical and categorical data
- Is robust to noise and outliers, which are common in educational datasets

### Hyperparameters
- Number of trees: **200**
- Maximum depth: **10**
- Random state: **42**

### Preprocessing
- Numeric features passed through unchanged
- Categorical features (`subject`, `topic`, `mastery_level`) one-hot encoded

### Model Performance (20% Hold-out Test Set)
- **R² Score:** ~0.89 – 0.92
- **Mean Absolute Error (MAE):** ~3.2 – 4.1 points

---

## 🧠 How Recommendations Are Calculated

### Advice Logic
- Low attendance → attendance improvement advice
- Low quiz scores → quiz review recommendation
- Low assignment scores → assignment improvement guidance

### Goal-Seeking Logic
- **Gap** = Target Score − Predicted Score
- **Extra Study Hours** ≈ Gap ÷ 4 (heuristic estimate)
- Subject-specific strategies are added when applicable

> These recommendations are **heuristic-based**, designed to be interpretable and educational rather than absolute guarantees.

---

## ⚠️ Limitations

- The model is trained on synthetic data and may not fully capture real-world academic behavior
- Study-hour estimates are approximations, not guarantees
- External factors such as teaching quality or personal challenges are not included

---

## 🛠️ Technology Stack

- Python 3
- pandas & numpy (data handling)
- scikit-learn (machine learning & preprocessing)
- Gradio (interactive web interface)
- pickle (model serialization)

---

## 🔮 Planned Enhancements

- Integration with real anonymized academic datasets
- Model explainability (e.g., SHAP values)
- Expanded subject and topic coverage
- PDF and Excel export options
- Cloud deployment (Hugging Face Spaces, Render, Railway)
- User accounts and progress tracking
- Mobile-responsive UI improvements

---

## 📄 License

MIT License  
You are free to use, modify, and distribute this project.


