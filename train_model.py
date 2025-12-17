import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier

# Load Data
df = pd.read_csv("User_profiling.csv")

# 1. Define the Mappings (Make sure these match actions.py)
talk_resrv_dict = {'Talkative': 0, 'Reserved': 1}
prefers_listening_dict = {'Yes': 1, 'No': 0}
Energised_or_Drained_dict = {'Drained': 0, 'Energized': 1}
Persuasion_dict = {'I don’t like persuasion': 0, 'Am not fond but ok with persuasion': 1, 'I like persuasion': 2}
personal_involvement_dict = {'Low': 0, 'Medium': 1, 'High': 2}

# *** CRITICAL FIX: Force the Label Mapping ***
# actions.py expects: 0=Formal, 1=Personal, 2=Moderate
Label_dict = {'Formal': 0, 'Personal': 1, 'Moderate': 2}

# 2. Apply Mappings
df["Talk/Reserved"] = df["Talk/Reserved"].map(talk_resrv_dict)
df["prefers listening or not"] = df["prefers listening or not"].map(prefers_listening_dict)
df["Energized or drained"] = df["Energized or drained"].map(Energised_or_Drained_dict)
df["persuasion"] = df["persuasion"].map(Persuasion_dict)
df["personal involvement"] = df["personal involvement"].map(personal_involvement_dict)
df["label"] = df["label"].map(Label_dict) # <--- Apply the label mapping here

# 3. Train
X = df[["Talk/Reserved", "prefers listening or not", "Energized or drained", "persuasion", "personal involvement"]]
y = df["label"]

clf = DecisionTreeClassifier()
clf.fit(X, y)

# 4. Save
joblib.dump(clf, "actions/PERSONALITY_MODEL.joblib")
print("Model saved successfully with correct mappings.")