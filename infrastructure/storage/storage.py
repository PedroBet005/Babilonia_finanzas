import os
import json
from typing import Dict, Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

DATA_PATH = os.path.join(DATA_DIR, "datos.json")
LOG_PATH = os.path.join(DATA_DIR, "log.txt")


def load_data() -> Dict[str, Any]:
    if not os.path.exists(DATA_PATH):
        return {
            "incomes": [],
            "expenses": [],
            "summary": {
                "income": 0.0,
                "expenses": 0.0,
                "savings": 0.0,
                "tithe": 0.0,
                "debts": 0.0,
            },
            "open": True,
        }

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: Dict[str, Any]) -> None:
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

