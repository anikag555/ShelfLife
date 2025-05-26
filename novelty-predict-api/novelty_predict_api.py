from fastapi import FastAPI
from pydantic import BaseModel
import joblib  # for loading trained ML model
import pandas as pd

app = FastAPI()
model = joblib.load("novelty_model.pkl")  # your trained model

class UserRequest(BaseModel):
    user_id: int
    day: int
    hour: int

@app.post("/predict-novelty-time")
def predict_novelty(req: UserRequest):
    features = pd.DataFrame([{
        "user_id": req.user_id,
        "order_dow": req.day,
        "order_hour_of_day": req.hour,
        # Add other engineered features here
    }])
    prob = model.predict_proba(features)[0][1]
    return {
        "user_id": req.user_id,
        "day": req.day,
        "hour": req.hour,
        "novelty_probability": round(prob, 3)
    }
