import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import numpy as np

df = pd.read_csv("../cleaned_dataset_part1.csv")

X = df[["order_hour_of_day", "order_dow", "days_since_prior_order"]]
y = df["includes_novelty"] = np.random.choice([0, 1], size=len(df))


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "novelty_model.pkl")
