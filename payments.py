"""
Модуль для работы с платежами и инвойсами.
Содержит функции расчёта стоимости и генерации инвойсов.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Booking


class Invoice:
    """Счёт за проживание."""

    def __init__(self, booking: Booking) -> None:
        """Инициализация счёта."""
        self.booking = booking

    def calculate_base_cost(self) -> float:
        """Базовая стоимость (дни × цена за ночь)."""
        return self.booking.calculate_total_price()

    def calculate_tax(self, tax_rate: float = 0.1) -> float:
        """Вычислить налог (по умолчанию 10%)."""
        return self.calculate_base_cost() * tax_rate

    def calculate_total_with_tax(self, tax_rate: float = 0.1) -> float:
        """Итоговая сумма с налогом."""
        return self.calculate_base_cost() + self.calculate_tax(tax_rate)

    def generate_invoice_text(self, tax_rate: float = 0.1) -> str:
        """Сгенерировать текст счёта."""
        base_cost = self.calculate_base_cost()
        tax = self.calculate_tax(tax_rate)
        total = self.calculate_total_with_tax(tax_rate)

        text = f"""
{'='*50}
INVOICE
{'='*50}
Guest: {self.booking.guest.name}
Contact: {self.booking.guest.contact}

Room: {self.booking.room.number} ({self.booking.room.room_type})
Check-in: {self.booking.check_in}
Check-out: {self.booking.check_out}
Nights: {self.booking.nights_count()}

Rate per night: ${self.booking.room.price_per_night:.2f}
Base cost: ${base_cost:.2f}
Tax ({int(tax_rate*100)}%): ${tax:.2f}
---
TOTAL: ${total:.2f}
{'='*50}
"""
        return text
