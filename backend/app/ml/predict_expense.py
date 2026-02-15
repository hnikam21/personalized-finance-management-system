import joblib
import os
import re
import numpy as np

MODEL_PATH = "app/ml/models/expense_model.pkl"

model = joblib.load(MODEL_PATH)

def clean_text(text: str):
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def predict_category(description: str):
    cleaned = clean_text(description)

    prediction = model.predict([cleaned])[0]
    probabilities = model.predict_proba([cleaned])[0]

    confidence = float(np.max(probabilities))

    return prediction, confidence
