from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserRequest(BaseModel):
    user_id: int

@app.post("/user-staples")
def get_staples(req: UserRequest):
    # Placeholder — replace with your actual logic
    return {
        "user_id": req.user_id,
        "staple_items": [
            {"product_name": "milk", "order_pct": 88},
            {"product_name": "bread", "order_pct": 81}
        ]
    }
