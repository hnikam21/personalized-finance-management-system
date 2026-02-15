import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity
from app.models.user_training_data import UserTrainingData

MODEL_PATH = os.path.join("app", "ml", "models", "expense_model.pkl")
global_model = joblib.load(MODEL_PATH)


def train_user_model(db, user_id):

    data = db.query(UserTrainingData).filter(
        UserTrainingData.user_id == user_id
    ).all()

    if len(data) < 5:
        return None

    descriptions = [d.description for d in data]
    categories = [d.category_name for d in data]

    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression())
    ])

    model.fit(descriptions, categories)
    return model


def classify_expense(db, user_id, description):

    # --------------------
    # 1️⃣ Try user model
    # --------------------

    user_model = train_user_model(db, user_id)

    if user_model:
        prediction = user_model.predict([description])[0]
        return prediction, "user_model"

    # --------------------
    # 2️⃣ Fallback to global model
    # --------------------

    probabilities = global_model.predict_proba([description])[0]
    max_index = probabilities.argmax()
    confidence = probabilities[max_index]
    category = global_model.classes_[max_index]

    if confidence >= 0.6:
        return category, "global_model"

    return "Miscellaneous", "fallback"
