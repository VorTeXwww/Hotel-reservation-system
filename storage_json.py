"""
Модуль для работы с JSON-хранилищем.
Загрузка и сохранение данных о комнатах и гостях.
"""

import json
from pathlib import Path

from models import Room, Guest
from exceptions import JsonStorageError


class HotelJsonFileIO:
    """Класс для работы с JSON-хранилищем комнат и гостей."""

    def __init__(
        self, rooms_path: str = "rooms.json", guests_path: str = "guests.json"
    ) -> None:
        """
        Инициализация хранилища.

        Args:
            rooms_path (str): Путь к файлу с комнатами.
            guests_path (str): Путь к файлу с гостями.
        """
        self.rooms_file = Path(rooms_path)
        self.guests_file = Path(guests_path)

    def load_rooms(self) -> list[Room]:
        """
        Загрузить комнаты из JSON.

        Returns:
            list[Room]: Список объектов Room.

        Raises:
            JsonStorageError: Если ошибка при чтении файла.
        """
        if not self.rooms_file.exists():
            return []
        try:
            with self.rooms_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise JsonStorageError(f"Failed to load rooms: {e}")

        rooms: list[Room] = []
        for item in data:
            try:
                room = Room(
                    number=item["number"],
                    room_type=item["room_type"],
                    price_per_night=item["price_per_night"],
                    is_occupied=item.get("is_occupied", False),
                )
                rooms.append(room)
            except (KeyError, ValueError) as e:
                raise JsonStorageError(f"Invalid room data: {e}")
        return rooms

    def save_rooms(self, rooms: list[Room]) -> None:
        """
        Сохранить комнаты в JSON.

        Args:
            rooms (list[Room]): Список объектов Room.

        Raises:
            JsonStorageError: Если ошибка при записи файла.
        """
        data = [
            {
                "number": r.number,
                "room_type": r.room_type,
                "price_per_night": r.price_per_night,
                "is_occupied": r.is_occupied,
            }
            for r in rooms
        ]
        try:
            with self.rooms_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise JsonStorageError(f"Failed to save rooms: {e}")

    def load_guests(self) -> list[Guest]:
        """
        Загрузить гостей из JSON.

        Returns:
            list[Guest]: Список объектов Guest.

        Raises:
            JsonStorageError: Если ошибка при чтении файла.
        """
        if not self.guests_file.exists():
            return []
        try:
            with self.guests_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise JsonStorageError(f"Failed to load guests: {e}")

        guests: list[Guest] = []
        for item in data:
            try:
                guest = Guest(
                    guest_id=item["guest_id"],
                    name=item["name"],
                    contact=item["contact"],
                )
                guests.append(guest)
            except (KeyError, ValueError) as e:
                raise JsonStorageError(f"Invalid guest data: {e}")
        return guests

    def save_guests(self, guests: list[Guest]) -> None:
        """
        Сохранить гостей в JSON.

        Args:
            guests (list[Guest]): Список объектов Guest.

        Raises:
            JsonStorageError: Если ошибка при записи файла.
        """
        data = [
            {
                "guest_id": g.guest_id,
                "name": g.name,
                "contact": g.contact,
            }
            for g in guests
        ]
        try:
            with self.guests_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise JsonStorageError(f"Failed to save guests: {e}")
