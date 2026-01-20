from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import pandas as pd
import pickle

# Load training dataset
df = pd.read_csv("training_data.csv")

# Features (everything except student_id and final_exam_score)
X = df.drop(columns=["student_id", "final_exam_score"])
y = df["final_exam_score"]

# Identify categorical & numeric columns
categorical_cols = ["subject", "topic", "mastery_level"]
numeric_cols = ["quiz_score", "assignment_score", "attempts", "attendance"]

# Column transformer (ERROR-PROOF)
preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols)

    ]
)

# Pipeline
model_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42
    ))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model_pipeline.fit(X_train, y_train)

# Evaluate
preds = model_pipeline.predict(X_test)
print("R² Score:", r2_score(y_test, preds))
print("MAE:", mean_absolute_error(y_test, preds))

# Save pipeline
with open("model.pkl", "wb") as f:
    pickle.dump(model_pipeline, f)

print("✅ Model trained and saved as model.pkl")
