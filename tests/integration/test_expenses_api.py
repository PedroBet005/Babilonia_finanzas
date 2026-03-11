from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_expense_endpoint():
    response = client.post(
        "/api/v1/expenses/",
        json={
            "amount": 200,
            "category": "Food",
            "description": "Groceries",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["amount"] == 200
    assert data["category"] == "Food"
