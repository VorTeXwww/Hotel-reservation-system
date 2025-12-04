"""
Основной сервис для управления отелем.
Содержит классы Hotel и HotelService с полной бизнес-логикой.
"""

from __future__ import annotations

from datetime import date
from typing import Dict, Optional
import uuid

from models import Room, Guest, Booking, BookingStatus
from exceptions import (
    EntityNotFoundError,
    BookingConflictError,
    InvalidOperationError,
)


class Hotel:
    """
    Модель отеля, управляющая номерами, гостями и бронированиями.

    Атрибуты:
        name (str): Название отеля.
        rooms (Dict[int, Room]): Словарь номеров (ключ - номер комнаты).
        guests (Dict[str, Guest]): Словарь гостей (ключ - ID гостя).
        bookings (Dict[str, Booking]): Словарь броней (ключ - ID брони).
    """

    def __init__(self, name: str) -> None:
        """Инициализация отеля."""
        if not name:
            raise InvalidOperationError("Hotel name is required")
        self.name: str = name
        self.rooms: Dict[int, Room] = {}
        self.guests: Dict[str, Guest] = {}
        self.bookings: Dict[str, Booking] = {}

    def add_room(self, number: int, room_type: str, price_per_night: float) -> Room:
        """
        Добавить номер в отель.

        Args:
            number (int): Номер комнаты.
            room_type (str): Тип комнаты.
            price_per_night (float): Цена за ночь.

        Returns:
            Room: Созданный объект номера.

        Raises:
            InvalidOperationError: Если номер уже существует.
        """
        if number in self.rooms:
            raise InvalidOperationError(f"Room {number} already exists")
        room = Room(number=number, room_type=room_type, price_per_night=price_per_night)
        self.rooms[number] = room
        return room

    def remove_room(self, number: int) -> None:
        """
        Удалить номер из отеля.

        Args:
            number (int): Номер комнаты.

        Raises:
            EntityNotFoundError: Если номер не найден.
            InvalidOperationError: Если номер занят.
        """
        if number not in self.rooms:
            raise EntityNotFoundError(f"Room {number} does not exist")
        if self.rooms[number].is_occupied:
            raise InvalidOperationError("Cannot remove occupied room")
        del self.rooms[number]

    def list_rooms(self) -> list[Room]:
        """Получить список всех номеров."""
        return list(self.rooms.values())

    def get_room(self, number: int) -> Room:
        """
        Получить номер по номеру.

        Args:
            number (int): Номер комнаты.

        Returns:
            Room: Объект номера.

        Raises:
            EntityNotFoundError: Если номер не найден.
        """
        if number not in self.rooms:
            raise EntityNotFoundError(f"Room {number} does not exist")
        return self.rooms[number]

    def __repr__(self) -> str:
        """Строковое представление отеля."""
        return f"Hotel({self.name}, rooms={len(self.rooms)}, guests={len(self.guests)})"


class HotelService:
    """
    Сервис отеля - главный фасад для работы с системой бронирования.
    Управляет гостями, комнатами, бронями и всеми операциями.
    """

    def __init__(self, hotel: Hotel) -> None:
        """Инициализация сервиса с объектом отеля."""
        self.hotel: Hotel = hotel

    # ===== ГОСТИ =====

    def register_guest(self, name: str, contact: str) -> Guest:
        """
        Зарегистрировать нового гостя.

        Args:
            name (str): Имя гостя.
            contact (str): Контакт гостя.

        Returns:
            Guest: Объект зарегистрированного гостя.
        """
        guest_id = str(uuid.uuid4())
        guest = Guest(guest_id=guest_id, name=name, contact=contact)
        self.hotel.guests[guest_id] = guest
        return guest

    def get_guest(self, guest_id: str) -> Guest:
        """
        Получить гостя по ID.

        Args:
            guest_id (str): ID гостя.

        Returns:
            Guest: Объект гостя.

        Raises:
            EntityNotFoundError: Если гость не найден.
        """
        if guest_id not in self.hotel.guests:
            raise EntityNotFoundError(f"Guest {guest_id} does not exist")
        return self.hotel.guests[guest_id]

    def list_guests(self) -> list[Guest]:
        """Получить список всех гостей."""
        return list(self.hotel.guests.values())

    # ===== НОМЕРА =====

    def add_room(self, number: int, room_type: str, price_per_night: float) -> Room:
        """
        Добавить номер в отель.

        Args:
            number (int): Номер комнаты.
            room_type (str): Тип комнаты.
            price_per_night (float): Цена за ночь.

        Returns:
            Room: Объект созданного номера.
        """
        return self.hotel.add_room(number, room_type, price_per_night)

    def list_rooms(self) -> list[Room]:
        """Получить список всех номеров."""
        return self.hotel.list_rooms()

    def get_available_rooms(
        self, check_in: date, check_out: date, room_type: Optional[str] = None
    ) -> list[Room]:
        """
        Получить доступные номера на период.

        Args:
            check_in (date): Дата заезда.
            check_out (date): Дата выезда.
            room_type (Optional[str]): Фильтр по типу комнаты.

        Returns:
            list[Room]: Список доступных номеров.

        Raises:
            InvalidOperationError: Если даты некорректны.
        """
        if check_out <= check_in:
            raise InvalidOperationError("check_out must be after check_in")

        available = []
        for room in self.hotel.list_rooms():
            if room_type and room.room_type != room_type:
                continue
            if self._room_is_available(room, check_in, check_out):
                available.append(room)
        return available

    def _room_is_available(
        self, room: Room, check_in: date, check_out: date
    ) -> bool:
        """Проверить, свободна ли комната на период."""
        for booking in self.hotel.bookings.values():
            if booking.room.number != room.number:
                continue
            if booking.status in (BookingStatus.CANCELLED, BookingStatus.CHECKED_OUT):
                continue
            if check_in < booking.check_out and booking.check_in < check_out:
                return False
        return True

    # ===== БРОНИРОВАНИЕ =====

    def create_booking(
        self, guest_id: str, room_number: int, check_in: date, check_out: date
    ) -> Booking:
        """
        Создать новую бронь.

        Args:
            guest_id (str): ID гостя.
            room_number (int): Номер комнаты.
            check_in (date): Дата заезда.
            check_out (date): Дата выезда.

        Returns:
            Booking: Объект созданной брони.

        Raises:
            EntityNotFoundError: Если гость или комната не найдены.
            BookingConflictError: Если комната не доступна.
        """
        guest = self.get_guest(guest_id)
        room = self.hotel.get_room(room_number)

        if not self._room_is_available(room, check_in, check_out):
            raise BookingConflictError(
                f"Room {room_number} is not available for {check_in} to {check_out}"
            )

        booking_id = str(uuid.uuid4())
        booking = Booking(
            booking_id=booking_id,
            guest=guest,
            room=room,
            check_in=check_in,
            check_out=check_out,
        )
        self.hotel.bookings[booking_id] = booking
        return booking

    def get_booking(self, booking_id: str) -> Booking:
        """
        Получить бронь по ID.

        Args:
            booking_id (str): ID брони.

        Returns:
            Booking: Объект брони.

        Raises:
            EntityNotFoundError: Если бронь не найдена.
        """
        if booking_id not in self.hotel.bookings:
            raise EntityNotFoundError(f"Booking {booking_id} does not exist")
        return self.hotel.bookings[booking_id]

    def get_guest_bookings(self, guest_id: str) -> list[Booking]:
        """
        Получить все брони гостя.

        Args:
            guest_id (str): ID гостя.

        Returns:
            list[Booking]: Список броней гостя.
        """
        self.get_guest(guest_id)
        return [b for b in self.hotel.bookings.values() if b.guest.guest_id == guest_id]

    def list_bookings(self) -> list[Booking]:
        """Получить список всех броней."""
        return list(self.hotel.bookings.values())

    def cancel_booking(self, booking_id: str) -> None:
        """
        Отменить бронь.

        Args:
            booking_id (str): ID брони.

        Raises:
            EntityNotFoundError: Если бронь не найдена.
            InvalidOperationError: Если бронь уже завершена.
        """
        booking = self.get_booking(booking_id)
        if booking.status == BookingStatus.CANCELLED:
            return
        if booking.status == BookingStatus.CHECKED_OUT:
            raise InvalidOperationError("Cannot cancel checked-out booking")
        booking.status = BookingStatus.CANCELLED

    # ===== CHECK-IN / CHECK-OUT =====

    def check_in(self, booking_id: str, current_date: date) -> None:
        """
        Заселить гостя (check-in).

        Args:
            booking_id (str): ID брони.
            current_date (date): Текущая дата.

        Raises:
            EntityNotFoundError: Если бронь не найдена.
            InvalidOperationError: Если статус некорректен или дата не совпадает.
        """
        booking = self.get_booking(booking_id)
        if booking.status != BookingStatus.BOOKED:
            raise InvalidOperationError(
                f"Cannot check-in: booking status is {booking.status}"
            )
        if current_date != booking.check_in:
            raise InvalidOperationError(
                f"Check-in date mismatch: expected {booking.check_in}, got {current_date}"
            )
        if booking.room.is_occupied:
            raise BookingConflictError("Room is already occupied")

        booking.status = BookingStatus.CHECKED_IN
        booking.room.is_occupied = True

    def check_out(self, booking_id: str, current_date: date) -> float:
        """
        Выселить гостя (check-out) и вернуть итоговую стоимость.

        Args:
            booking_id (str): ID брони.
            current_date (date): Текущая дата.

        Returns:
            float: Итоговая сумма к оплате.

        Raises:
            EntityNotFoundError: Если бронь не найдена.
            InvalidOperationError: Если статус некорректен или дата не совпадает.
        """
        booking = self.get_booking(booking_id)
        if booking.status != BookingStatus.CHECKED_IN:
            raise InvalidOperationError(
                f"Cannot check-out: booking status is {booking.status}"
            )
        if current_date != booking.check_out:
            raise InvalidOperationError(
                f"Check-out date mismatch: expected {booking.check_out}, got {current_date}"
            )

        booking.status = BookingStatus.CHECKED_OUT
        booking.room.is_occupied = False
        return booking.calculate_total_price()
    def get_active_bookings(self) -> list[Booking]:
        """Получить список активных броней (BOOKED или CHECKED_IN)."""
        return [
            b
            for b in self.hotel.bookings.values()
            if b.status in (BookingStatus.BOOKED, BookingStatus.CHECKED_IN)
        ]

    def get_occupancy_report(self) -> dict[str, int]:
        """Получить отчёт о загруженности номеров."""
        return {
            "total_rooms": len(self.hotel.rooms),
            "occupied_rooms": sum(1 for r in self.hotel.rooms.values() if r.is_occupied),
            "available_rooms": sum(1 for r in self.hotel.rooms.values() if not r.is_occupied),
        }

    def calculate_total_revenue(self) -> float:
        """Вычислить общий доход от завершённых броней."""
        total = 0.0
        for booking in self.hotel.bookings.values():
            if booking.status == BookingStatus.CHECKED_OUT:
                total += booking.calculate_total_price()
        return total
