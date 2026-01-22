import joblib
import pandas as pd

model = joblib.load("ml/model.pkl")

def predict_delay_risk(progress, sector, elapsed_ratio):
    X = pd.DataFrame([{
        "progress": progress,
        "sector": sector,
        "elapsed_ratio": elapsed_ratio
    }])
    return model.predict_proba(X)[0][1]  # risk score
