import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import mlflow
import mlflow.sklearn

# Load data
df = pd.read_csv("../cleaned_dataset_part1.csv")

# Use only time-based features
X = df[["order_hour_of_day", "order_dow"]]
y = df["includes_novelty"]  # real label column

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save locally
joblib.dump(model, "novelty_model.pkl")

with mlflow.start_run():
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="novelty-model",
        input_example=X_test.head(1),  
        registered_model_name="novelty-model"
    )
    acc = accuracy_score(y_test, model.predict(X_test))
    mlflow.log_metric("accuracy", acc)

