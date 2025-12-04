"""
Демонстрационное консольное приложение для системы бронирования отеля.
Главный файл для запуска: python hotel_app.py
"""

from datetime import date

from hotel_service import Hotel, HotelService
from storage_json import HotelJsonFileIO, JsonStorageError
from exceptions import HotelError
from payments import Invoice


def read_date(prompt: str) -> date:
    """Прочитать дату у пользователя в формате YYYY-MM-DD."""
    while True:
        try:
            raw = input(prompt + " (YYYY-MM-DD): ").strip()
            year, month, day = map(int, raw.split("-"))
            return date(year, month, day)
        except (ValueError, IndexError):
            print("Invalid date format. Use YYYY-MM-DD")


def display_menu() -> None:
    """Показать главное меню."""
    print("\n" + "=" * 50)
    print("Hotel Reservation System - Main Menu")
    print("=" * 50)
    print("1.  Add room")
    print("2.  List rooms")
    print("3.  Register guest")
    print("4.  List guests")
    print("5.  Check availability")
    print("6.  Create booking")
    print("7.  Get guest bookings")
    print("8.  Cancel booking")
    print("9.  Check-in")
    print("10. Check-out")
    print("11. Active bookings")
    print("12. Occupancy report")
    print("13. Revenue report")
    print("0.  Exit")
    print("=" * 50)


def main() -> None:
    """Главная функция приложения."""
    hotel = Hotel("Luxury Hotel")
    service = HotelService(hotel)
    storage = HotelJsonFileIO()

    try:
        for room in storage.load_rooms():
            hotel.rooms[room.number] = room
        for guest in storage.load_guests():
            hotel.guests[guest.guest_id] = guest
        print("✓ Initial data loaded from JSON")
    except JsonStorageError as e:
        print(f"⚠ Warning: {e}")

    while True:
        try:
            display_menu()
            choice = input("Choose option: ").strip()

            if choice == "1":
                number = int(input("Room number: "))
                room_type = input("Room type (single/double/suite): ")
                price = float(input("Price per night: "))
                service.add_room(number, room_type, price)
                print("✓ Room added successfully")

            elif choice == "2":
                rooms = service.list_rooms()
                if not rooms:
                    print("No rooms in hotel")
                else:
                    print("\nRooms:")
                    for r in rooms:
                        status = "occupied" if r.is_occupied else "available"
                        print(
                            f"  Room {r.number}: {r.room_type} | "
                            f"${r.price_per_night}/night | {status}"
                        )

            elif choice == "3":
                name = input("Guest name: ")
                contact = input("Contact (email or phone): ")
                guest = service.register_guest(name, contact)
                print(f"✓ Guest registered with ID: {guest.guest_id}")

            elif choice == "4":
                guests = service.list_guests()
                if not guests:
                    print("No guests registered")
                else:
                    print("\nGuests:")
                    for g in guests:
                        print(f"  {g.guest_id}: {g.name} ({g.contact})")

            elif choice == "5":
                ci = read_date("Check-in date")
                co = read_date("Check-out date")
                room_type = (
                    input("Room type filter (leave empty for any): ").strip() or None
                )
                available = service.get_available_rooms(ci, co, room_type)
                if not available:
                    print("No rooms available for these dates")
                else:
                    print("\nAvailable rooms:")
                    for r in available:
                        print(f"  Room {r.number}: {r.room_type} (${r.price_per_night}/night)")

            elif choice == "6":
                guest_id = input("Guest ID: ").strip()
                room_number = int(input("Room number: "))
                ci = read_date("Check-in date")
                co = read_date("Check-out date")
                booking = service.create_booking(guest_id, room_number, ci, co)
                print(f"✓ Booking created with ID: {booking.booking_id}")

            elif choice == "7":
                guest_id = input("Guest ID: ").strip()
                bookings = service.get_guest_bookings(guest_id)
                if not bookings:
                    print("No bookings for this guest")
                else:
                    print(f"\nBookings for guest {guest_id}:")
                    for b in bookings:
                        print(
                            f"  {b.booking_id}: Room {b.room.number} | "
                            f"{b.check_in} to {b.check_out} | {b.status}"
                        )

            elif choice == "8":
                booking_id = input("Booking ID: ").strip()
                service.cancel_booking(booking_id)
                print("✓ Booking cancelled")

            elif choice == "9":
                booking_id = input("Booking ID: ").strip()
                current = read_date("Today's date")
                service.check_in(booking_id, current)
                print("✓ Check-in successful")

            elif choice == "10":
                booking_id = input("Booking ID: ").strip()
                current = read_date("Today's date")
                total = service.check_out(booking_id, current)
                booking = service.get_booking(booking_id)
                invoice = Invoice(booking)
                print(invoice.generate_invoice_text())

            elif choice == "11":
                active = service.get_active_bookings()
                if not active:
                    print("No active bookings")
                else:
                    print("\nActive bookings:")
                    for b in active:
                        print(
                            f"  {b.booking_id}: {b.guest.name} | Room {b.room.number} | {b.status}"
                        )

            elif choice == "12":
                report = service.get_occupancy_report()
                print("\nOccupancy Report:")
                print(f"  Total rooms: {report['total_rooms']}")
                print(f"  Occupied: {report['occupied_rooms']}")
                print(f"  Available: {report['available_rooms']}")

            elif choice == "13":
                revenue = service.calculate_total_revenue()
                print(f"\nTotal Revenue: ${revenue:.2f}")

            elif choice == "0":
                storage.save_rooms(list(hotel.rooms.values()))
                storage.save_guests(list(hotel.guests.values()))
                print("✓ Data saved. Goodbye!")
                break

            else:
                print("Unknown option")

        except (ValueError, HotelError, JsonStorageError) as e:
            print(f"✗ Error: {e}")


if __name__ == "__main__":
    main()
