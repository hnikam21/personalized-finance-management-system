import pandas as pd
import random
import joblib
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# ---------------------------------------------------
# 1️⃣ Realistic Merchant + Keyword Dataset
# ---------------------------------------------------

category_data = {
    "Food": [
        "swiggy", "zomato", "restaurant", "pizza", "burger",
        "cafe", "starbucks", "dominos", "kfc",
        "SWIGGY*1234", "ZOMATO ONLINE", "STARBUCKS INDIA"
    ],
    "Transport": [
        "uber", "ola", "metro", "bus ticket",
        "petrol", "diesel", "auto fare",
        "UBER TRIP", "OLA RIDE", "HP PETROL PUMP"
    ],
    "Shopping": [
        "amazon", "flipkart", "mall shopping",
        "clothes", "electronics",
        "AMAZON PAY", "FLIPKART ONLINE", "MYNTRA STORE"
    ],
    "Bills": [
        "electricity bill", "water bill", "gas bill",
        "wifi recharge", "phone recharge",
        "AIRTEL POSTPAID", "JIO RECHARGE"
    ],
    "Entertainment": [
        "movie ticket", "netflix", "spotify",
        "concert", "gaming",
        "NETFLIX.COM", "SPOTIFY INDIA"
    ],
    "Health": [
        "doctor visit", "hospital", "medicine",
        "pharmacy", "medical checkup",
        "APOLLO PHARMACY"
    ],
    "Education": [
        "course fee", "udemy", "coursera",
        "exam fee", "college fees",
        "UDACITY PAYMENT"
    ],
    "Travel": [
        "flight ticket", "hotel booking",
        "train ticket", "airbnb",
        "MAKEMYTRIP", "GOIBIBO"
    ],
    "Groceries": [
        "vegetables", "milk", "supermarket",
        "dmart", "big bazaar",
        "DMART STORE", "RELIANCE FRESH"
    ],
    "Investment": [
        "mutual fund", "sip investment",
        "stock purchase", "fd deposit",
        "ZERODHA", "GROWW", "ICICI DIRECT"
    ],
    "Miscellaneous": [
        "gift", "donation", "random expense",
        "unknown payment"
    ]
}

# ---------------------------------------------------
# 2️⃣ Generate Realistic Variations
# ---------------------------------------------------

def generate_variations(keyword):
    templates = [
        f"{keyword}",
        f"Paid for {keyword}",
        f"{keyword} payment",
        f"Monthly {keyword}",
        f"Spent on {keyword}",
        f"{keyword} txn",
        f"{keyword} {random.randint(100,5000)}",
        f"UPI-{keyword}",
        f"{keyword} online transaction"
    ]

    variation = random.choice(templates)

    # Random casing
    variation = random.choice([
        variation.lower(),
        variation.upper(),
        variation.title()
    ])

    return variation


data = []

for category, keywords in category_data.items():
    for keyword in keywords:
        for _ in range(150):   # 150 variations per keyword
            description = generate_variations(keyword)
            data.append((description, category))

df = pd.DataFrame(data, columns=["description", "category"])

# ---------------------------------------------------
# 3️⃣ Clean Text Function
# ---------------------------------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\d+", "", text)  # remove numbers
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["description"] = df["description"].apply(clean_text)

# ---------------------------------------------------
# 4️⃣ Train/Test Split
# ---------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    df["description"],
    df["category"],
    test_size=0.2,
    random_state=42
)

# ---------------------------------------------------
# 5️⃣ ML Pipeline
# ---------------------------------------------------

model = Pipeline([
    ("vectorizer", TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english",
        max_features=5000
    )),
    ("classifier", LogisticRegression(
        max_iter=300,
        class_weight="balanced"
    ))
])

model.fit(X_train, y_train)

# ---------------------------------------------------
# 6️⃣ Evaluation
# ---------------------------------------------------

predictions = model.predict(X_test)
print("\n📊 Classification Report:\n")
print(classification_report(y_test, predictions))

# ---------------------------------------------------
# 7️⃣ Save Model
# ---------------------------------------------------

os.makedirs("app/ml/models", exist_ok=True)
joblib.dump(model, "app/ml/models/expense_model.pkl")

print("\n✅ Production-ready Expense Model trained & saved!")
