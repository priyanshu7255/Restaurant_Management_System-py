import json
import os

path = os.getcwd()
file_path = os.path.join(path,'SRC','Database','table_booking.json')

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

    def get_total_booked_seats(self, date):
        """Calculate the total booked seats for a given date."""
        if date not in self.bookings:
            return 0
        return sum(details["seats"] for details in self.bookings[date].values()) 

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
            if date not in self.bookings or str(table_id) not in self.bookings[date]:
                if details["capacity"] >= number_of_seats:
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



