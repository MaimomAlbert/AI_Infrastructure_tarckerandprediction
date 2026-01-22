import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib

# Generate synthetic data
np.random.seed(42)

n = 200
data = pd.DataFrame({
    "progress": np.random.randint(5, 100, n),
    "sector": np.random.choice([0, 1], n),  # 0=Road, 1=Rail
    "elapsed_ratio": np.random.uniform(0.2, 1.0, n)
})

# Define delay risk logically
data["delay_risk"] = (
    (data["progress"] < 40) &
    (data["elapsed_ratio"] > 0.6)
).astype(int)

X = data[["progress", "sector", "elapsed_ratio"]]
y = data["delay_risk"]

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "ml/model.pkl")
print("ML model trained and saved.")
