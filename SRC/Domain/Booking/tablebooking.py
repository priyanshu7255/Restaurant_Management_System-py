import json
import os
from datetime import datetime, timedelta

path = os.getcwd()
file_path = os.path.join(path, 'Restaurant_Management_System-py','SRC', 'Database', 'table_booking.json')

class Restaurant:
    def __init__(self, filename=file_path):  
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

    def is_valid_date(self, date):
        """Check if the date is valid (not in the past and not beyond one month)."""
        today = datetime.today().date()
        
        try:
            booking_date = datetime.strptime(date, "%d-%m-%Y").date()
            print(f"Today's date: {today}, Booking date: {booking_date}")  
            return today <= booking_date <= (today + timedelta(days=30))
        except ValueError:
            return False

    def get_total_booked_seats(self, date):
        """Calculate the total booked seats for a given date."""
        if date not in self.bookings:
            return 0         
        return sum(booking["seats"] for booking in self.bookings[date].values())

    def view_available_tables(self, date):
        """Show tables available for a specific date."""
        if not self.is_valid_date(date):
            return ["Invalid date. You can only book tables for today up to one month in advance."]
        
        booked_tables = self.bookings.get(date, {})
        available_tables = [
            f"Table {table_id}: Capacity {details['capacity']}"
            for table_id, details in self.tables.items() if str(table_id) not in booked_tables
        ]
        return available_tables if available_tables else ["No tables available on this date."]

    def book_table(self, number_of_seats, customer_name, date):
        """Automatically assign a table for booking based on seat availability."""
        

        #print(f"Booking requested for {customer_name} on {date} with {number_of_seats} seats.")

        if not self.is_valid_date(date):
            return "Invalid date. You can only book tables for today up to one month in advance."
        
        total_booked = self.get_total_booked_seats(date)
        available_seats = self.total_seats - total_booked

        # if number_of_seats > available_seats:
        #     return f"Only {available_seats} seats are available on {date}. Please adjust your request."

        if date not in self.bookings:
            self.bookings[date] = {}

        for table_id, details in self.tables.items():
            if str(table_id) not in self.bookings[date] and details["capacity"] >= number_of_seats:
                self.bookings[date][str(table_id)] = {
                    "customer": customer_name,
                    "seats": number_of_seats
                }
                self.save_data()
                return f"Table {table_id} booked successfully for {customer_name} ({number_of_seats} seats) on {date}!"

        return "No suitable table available for the requested seats. Try a different date or split into smaller groups."

    def view_bookings(self, date):
        """View all bookings for a specific date."""
        if not self.is_valid_date(date):
            return ["Invalid date. You can only view bookings for today up to one month in advance."]

        if date not in self.bookings or not self.bookings[date]:
            return ["No bookings found for this date."]

        return [f"Table {table_id} - Booked by {details['customer']} ({details['seats']} seats)"
                for table_id, details in self.bookings[date].items()]

    def cancel_booking(self, table_id, date):
        """Cancel a booking for a specific table and date."""
        if not self.is_valid_date(date):
            return "Invalid date. You can only cancel bookings for today up to one month in advance."

        if date in self.bookings and str(table_id) in self.bookings[date]:
            customer_name = self.bookings[date].pop(str(table_id))
            self.save_data()
            return f"Booking for Table {table_id} (Booked by {customer_name['customer']}) on {date} has been canceled."
        
        return "No booking found for this table on the specified date."
