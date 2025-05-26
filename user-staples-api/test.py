from fastapi.testclient import TestClient
from user_staples_api import app

client = TestClient(app)

def test_root():
    response = client.post("/user-staples", json={"user_id": 123})
    assert response.status_code == 200
