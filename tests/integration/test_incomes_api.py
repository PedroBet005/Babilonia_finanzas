from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_income_endpoint():
    response = client.post(
        "/api/v1/incomes/",
        json={
            "amount": 1000,
            "source": "Salary",
            "apply_tithe": False,
            "apply_debt": False,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["available"] == 900.0
    assert data["savings"] == 100.0
    assert data["income"]["amount"] == 1000
