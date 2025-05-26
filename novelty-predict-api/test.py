from fastapi.testclient import TestClient
from novelty_predict_api import app

client = TestClient(app)

def test_predict_novelty():
    response = client.post("/predict-novelty-time", json={
        "user_id": 123,
        "day": 3,
        "hour": 14
    })
    assert response.status_code == 200
