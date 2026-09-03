import json
import os
from datetime import datetime

class Restaurant:
    def __init__(self, filename="booking_data.json"):
        self.filename = filename
        self.total_seats = 20
        self.tables = {
            1: {"capacity": 2},
            2: {"capacity": 4},
            3: {"capacity": 6},
            4: {"capacity": 8},
            5: {"capacity": 10},
            6: {"capacity": 12},
            7: {"capacity": 14},
            8: {"capacity": 16},
            9: {"capacity": 18},
            10: {"capacity": 20},
        }
        self.bookings = {}

        self.load_data()

    def save_data(self):
        """Save the current state of bookings to a JSON file."""
        with open(self.filename, "w") as file:
            json.dump(self.bookings, file, indent=4)

    def load_data(self):
        """Load bookings from the JSON file if it exists."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                self.bookings = json.load(file)

    def get_total_booked_seats(self, date):
        """Calculate the total booked seats for a given date."""
        if date not in self.bookings:
            return 0
        return sum(self.tables[int(table_id)]["capacity"] for table_id in self.bookings[date])

    def view_available_tables(self, date):
        """Show tables available for a specific date."""
        booked_tables = self.bookings.get(date, {})
        available_tables = [
            f"Table {table_id}: Capacity {details['capacity']}"
            for table_id, details in self.tables.items() if str(table_id) not in booked_tables
        ]
        return available_tables if available_tables else ["No tables available on this date."]

    def book_table(self, number_of_seats, customer_name, date):
        """Book a table for a specific date based on seat availability."""
        total_booked = self.get_total_booked_seats(date)
        available_seats = self.total_seats - total_booked

        if number_of_seats > available_seats:
            return f"Only {available_seats} seats are available on {date}. Please adjust your request."

        for table_id, details in self.tables.items():
            if str(table_id) not in self.bookings.get(date, {}) and details["capacity"] >= number_of_seats:
                if date not in self.bookings:
                    self.bookings[date] = {}
                self.bookings[date][str(table_id)] = {"customer": customer_name, "seats": number_of_seats}
                self.save_data()
                return f"Table {table_id} booked successfully for {customer_name} ({number_of_seats} seats) on {date}!"

        return "No suitable table available for the requested seats. Try a different date or split into smaller groups."

    def view_bookings(self, date):
        """View all bookings for a specific date."""
        if date not in self.bookings or not self.bookings[date]:
            return [f"No bookings on {date}."]

        return [
            f"Table {table_id} - Booked by {details['customer']} ({details['seats']} seats)"
            for table_id, details in self.bookings[date].items()
        ]

    def cancel_booking(self, table_id, date):
        """Cancel a booking for a specific table and date."""
        if date in self.bookings and str(table_id) in self.bookings[date]:
            customer_name = self.bookings[date].pop(str(table_id))
            self.save_data()
            return f"Booking for Table {table_id} (Booked by {customer_name['customer']}) on {date} has been canceled."
        return "No booking found for this table on the specified date."

def main():
    restaurant = Restaurant()

    while True:
        print("\nRestaurant Table Booking System")
        print("1. View available tables for a date")
        print("2. Book a table")
        print("3. View bookings for a date")
        print("4. Cancel booking")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            date = input("Enter the date (DD-MM-YYYY): ")
            print("\n".join(restaurant.view_available_tables(date)))
        elif choice == "2":
            date = input("Enter booking date (DD-MM-YYYY): ")
            customer_name = input("Enter customer name: ")
            try:
                seats = int(input("Enter number of seats required: "))
                print(restaurant.book_table(seats, customer_name, date))
            except ValueError:
                print("Invalid input. Please enter a valid number of seats.")
        elif choice == "3":
            date = input("Enter the date (DD-MM-YYYY) to view bookings: ")
            print("\n".join(restaurant.view_bookings(date)))
        elif choice == "4":
            date = input("Enter booking date (DD-MM-YYYY): ")
            try:
                table_number = int(input("Enter table number to cancel booking: "))
                print(restaurant.cancel_booking(table_number, date))
            except ValueError:
                print("Invalid input. Please enter a valid table number.")
        elif choice == "5":
            print("Exiting... Thank you!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
