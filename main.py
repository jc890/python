import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# ============================
# LOAD DATA
# ============================
data = pd.read_csv('csvs/User_profiling.csv', encoding='utf_8')

# ============================
# ENCODING DICTIONARIES
# ============================
talk_resrv_dict = {'Talkative': 0, 'Reserved': 1}
prefers_listening_dict = {'Yes': 1, 'No': 0}
Energised_or_Drained_dict = {'Drained': 0, 'Energized': 1}
Persuasion_dict = {
    'I don’t like persuasion': 0,
    'Am not fond but ok with persuasion': 1,
    'I like persuasion': 2
}
personal_involvement_dict = {'Low': 0, 'Medium': 1, 'High': 2}
Label_dict = {'Formal': 3, 'Moderate': 2, 'Personal': 1}

# ============================
# APPLY ENCODING
# ============================
data['Talk/Reserved'] = data['Talk/Reserved'].replace(talk_resrv_dict)
data['prefers listening or not'] = data['prefers listening or not'].replace(prefers_listening_dict)
data['Energized or drained'] = data['Energized or drained'].replace(Energised_or_Drained_dict)
data['persuasion'] = data['persuasion'].replace(Persuasion_dict)
data['personal involvement'] = data['personal involvement'].replace(personal_involvement_dict)
data['label'] = data['label'].replace(Label_dict)

# ============================
# SPLIT FEATURES / LABEL
# ============================
X = data.drop('label', axis=1)
y = data['label']

# ============================
# TRAIN MODEL
# ============================
dt_clf = DecisionTreeClassifier(criterion='gini')
dt_clf.fit(X, y)

print("Model trained successfully!")
print("Training features:", list(X.columns))

# For label decoding
inv_label_dict = {v: k for k, v in Label_dict.items()}


# ============================
# PREDICTION FUNCTION (NO WARNINGS)
# ============================
def Classifier(talk_reserve, listen_pref, energy, persu, involvement):
    input_df = pd.DataFrame([{
        'Talk/Reserved': talk_reserve,
        'prefers listening or not': listen_pref,
        'Energized or drained': energy,
        'persuasion': persu,
        'personal involvement': involvement
    }])

    label_value = dt_clf.predict(input_df)[0]
    label_name = inv_label_dict[label_value]
    return label_name


# ============================
# TEST THE FUNCTION
# ============================
test_prediction = Classifier(
    talk_reserve=talk_resrv_dict['Reserved'],
    listen_pref=prefers_listening_dict['Yes'],
    energy=Energised_or_Drained_dict['Drained'],
    persu=Persuasion_dict['Am not fond but ok with persuasion'],
    involvement=personal_involvement_dict['Low']
)

print("Prediction:", test_prediction)
