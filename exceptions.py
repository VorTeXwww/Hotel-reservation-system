"""
Модуль исключений для системы бронирования отеля.
Содержит иерархию собственных исключений для отловки ошибок.
"""


class HotelError(Exception):
    """Базовое исключение для всей системы отеля."""
    pass


class EntityNotFoundError(HotelError):
    """Исключение: сущность (гость, комната, бронь) не найдена."""
    pass


class BookingConflictError(HotelError):
    """Исключение: конфликт дат при бронировании."""
    pass


class InvalidOperationError(HotelError):
    """Исключение: некорректная операция (check-in/check-out)."""
    pass


class JsonStorageError(HotelError):
    """Исключение: ошибка при работе с JSON-хранилищем."""
    pass


class PaymentError(HotelError):
    """Исключение: ошибка при расчёте платежа."""
    pass
