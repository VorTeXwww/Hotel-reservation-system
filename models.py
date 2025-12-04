"""
Модель данных для системы бронирования отеля.
Содержит классы Room, Guest, Booking и статусы.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from exceptions import InvalidOperationError


class BookingStatus:
    """Статусы брони (enum-подобный класс)."""

    BOOKED = "booked"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"

    @classmethod
    def is_valid(cls, status: str) -> bool:
        """Проверить, является ли строка валидным статусом."""
        return status in (
            cls.BOOKED,
            cls.CHECKED_IN,
            cls.CHECKED_OUT,
            cls.CANCELLED,
        )

    @classmethod
    def all_statuses(cls) -> list[str]:
        """Получить все возможные статусы."""
        return [cls.BOOKED, cls.CHECKED_IN, cls.CHECKED_OUT, cls.CANCELLED]


class Room:
    """
    Модель номера в отеле.

    Атрибуты:
        number (int): Номер комнаты (уникальный).
        room_type (str): Тип комнаты (single, double, suite и т.д.).
        price_per_night (float): Цена за ночь.
        is_occupied (bool): Занята ли комната в настоящий момент.
    """

    def __init__(
        self,
        number: int,
        room_type: str,
        price_per_night: float,
        is_occupied: bool = False,
    ) -> None:
        """Инициализация номера с валидацией."""
        if number <= 0:
            raise InvalidOperationError("Room number must be positive")
        if price_per_night <= 0:
            raise InvalidOperationError("Room price must be positive")
        if not room_type:
            raise InvalidOperationError("Room type is required")

        self.number: int = number
        self.room_type: str = room_type
        self.price_per_night: float = price_per_night
        self.is_occupied: bool = is_occupied

    def __repr__(self) -> str:
        """Строковое представление номера."""
        return (
            f"Room({self.number}, {self.room_type}, "
            f"${self.price_per_night}/night, occupied={self.is_occupied})"
        )


@dataclass
class Guest:
    """
    Модель гостя отеля.

    Атрибуты:
        guest_id (str): Уникальный ID гостя.
        name (str): Имя гостя.
        contact (str): Контакт гостя (email или телефон).
    """

    guest_id: str
    name: str
    contact: str

    def __post_init__(self) -> None:
        """Валидация полей гостя."""
        if not self.guest_id:
            raise InvalidOperationError("Guest ID is required")
        if not self.name:
            raise InvalidOperationError("Guest name is required")
        if not self.contact:
            raise InvalidOperationError("Guest contact is required")

    def __repr__(self) -> str:
        """Строковое представление гостя."""
        return f"Guest({self.guest_id}, {self.name})"


@dataclass
class Booking:
    """
    Модель брони номера.

    Атрибуты:
        booking_id (str): Уникальный ID брони.
        guest (Guest): Объект гостя.
        room (Room): Объект номера.
        check_in (date): Дата заезда.
        check_out (date): Дата выезда.
        status (str): Статус брони.
    """

    booking_id: str
    guest: Guest
    room: object
    check_in: date
    check_out: date
    status: str = field(default=BookingStatus.BOOKED)

    def __post_init__(self) -> None:
        """Валидация полей брони."""
        if not self.booking_id:
            raise InvalidOperationError("Booking ID is required")
        if self.check_out <= self.check_in:
            raise InvalidOperationError("check_out must be after check_in")
        if not BookingStatus.is_valid(self.status):
            raise InvalidOperationError(f"Invalid status: {self.status}")

    def nights_count(self) -> int:
        """Вычислить количество ночей в бронировании."""
        return (self.check_out - self.check_in).days

    def calculate_total_price(self) -> float:
        """
        Вычислить итоговую стоимость брони.

        Returns:
            float: Стоимость = количество ночей × цена за ночь.
        """
        nights = self.nights_count()
        return nights * self.room.price_per_night

    def __repr__(self) -> str:
        """Строковое представление брони."""
        return (
            f"Booking({self.booking_id}, {self.guest.name}, "
            f"Room {self.room.number}, {self.check_in} to {self.check_out})"
        )
