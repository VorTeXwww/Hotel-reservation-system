# Hotel-reservation-system
# Hotel Reservation System

Полнофункциональная система бронирования номеров отеля на Python 3.8+ с ООП архитектурой, JSON-хранилищем и полным покрытием тестами.

## Структура проекта
hotel-reservation-system/

├── exceptions.py # Иерархия исключений

├── models.py # Room, Guest, Booking, BookingStatus

├── hotel_service.py # Hotel + HotelService

├── storage_json.py # JSON I/O

├── payments.py # Invoice

├── hotel_app.py # Консольное приложение (ГЛАВНЫЙ ФАЙЛ)

├── seed_data.py # Инициализация данных

├── tests/

│ └── test_hotel_system.py # 12 юнит-тестов

├── rooms.json

├── guests.json

├── uml_diagram.puml

├── uml_diagram.png

├── requirements.txt

├── README.md

└── .gitignore
## Функционал 

- Управление номерами
- Регистрация гостей
- Создание и отмена броней
- Check-in и check-out
- Проверка доступности
- Расчёт стоимости
- Поиск броней гостя
- Отчёты (загруженность, доход)
- Инвойсы с налогами
- JSON-хранилище
### Консольное меню
Hotel Reservation System - Main Menu
1.Add room

2.List rooms

3.Register guest

4.List guests

5.Check availability

6.Create booking

7.Get guest bookings

8.Cancel booking

9.Check-in

10.Check-out

11.Active bookings

12.Occupancy report

13.Revenue report

14.Exit
HotelError

├── EntityNotFoundError

├── BookingConflictError

├── InvalidOperationError

├── JsonStorageError

└── PaymentError

## ООП принципы

- **Инкапсуляция**: приватные методы и валидация
- **Наследование**: иерархия исключений
- **Полиморфизм**: методы с одинаковыми именами
- **Абстракция**: интерфейсы через классы

##Автор

Проект для учебного курса по ООП - Система бронирования отеля

##Лицензия

MIT
