"""
Модуль для инициализации тестовых данных.
Создаёт начальные JSON-файлы с комнатами и гостями.
"""

import json
from pathlib import Path


def create_initial_data() -> None:
    """Создать начальные JSON-файлы если их нет."""

    rooms_data = [
        {"number": 101, "room_type": "single", "price_per_night": 100.0, "is_occupied": False},
        {"number": 102, "room_type": "double", "price_per_night": 150.0, "is_occupied": False},
        {
            "number": 103,
            "room_type": "suite",
            "price_per_night": 250.0,
            "is_occupied": False,
        },
    ]

    guests_data = [
        {"guest_id": "guest-001", "name": "John Doe", "contact": "john@example.com"},
        {"guest_id": "guest-002", "name": "Jane Smith", "contact": "jane@example.com"},
    ]

    rooms_path = Path("rooms.json")
    guests_path = Path("guests.json")

    if not rooms_path.exists():
        with rooms_path.open("w", encoding="utf-8") as f:
            json.dump(rooms_data, f, ensure_ascii=False, indent=2)
        print("✓ Created rooms.json")

    if not guests_path.exists():
        with guests_path.open("w", encoding="utf-8") as f:
            json.dump(guests_data, f, ensure_ascii=False, indent=2)
        print("✓ Created guests.json")


if __name__ == "__main__":
    create_initial_data()
