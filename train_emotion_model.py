import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("User_profiling.csv")

# Columns names from your dataset
feature_cols = [
    "Talk/Reserved",
    "prefers listening or not",
    "Energized or drained",
    "persuasion",
    "personal involvement"
]

target_col = "label"

# Encode categorical values
encoder = LabelEncoder()

for col in feature_cols:
    df[col] = encoder.fit_transform(df[col].astype(str))

df[target_col] = encoder.fit_transform(df[target_col].astype(str))

# Split dataset
X = df[feature_cols]
y = df[target_col]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model (Logistic Regression)
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: {accuracy}")

# Save model
joblib.dump(model, "emotion_model.pkl")

print("Model saved as emotion_model.pkl")
