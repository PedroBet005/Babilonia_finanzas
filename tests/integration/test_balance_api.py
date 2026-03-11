from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_balance_endpoint():
    # Primero creamos income
    client.post(
        "/api/v1/incomes/",
        json={
            "amount": 1000,
            "source": "Salary",
            "apply_tithe": False,
            "apply_debt": False,
        },
    )

    # Luego expense
    client.post(
        "/api/v1/expenses/",
        json={
            "amount": 200,
            "category": "Food",
        },
    )

    # Ahora consultamos balance
    response = client.get("/api/v1/balance/")

    assert response.status_code == 200

    data = response.json()

    assert data["balance"] == 800.0
