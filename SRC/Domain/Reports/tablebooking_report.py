import json
import os

class TableBookingReport:
    def __init__(self):
        """Initialize the class and load data from JSON file."""
        self.file_path = os.path.join(os.getcwd(), 'SRC', 'Database', 'table_booking.json')
        self.bookings = self.load_data()

    def load_data(self):
        """Load table booking data from the JSON file."""
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error: Table booking file not found.")
            return {}
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in table booking file.")
            return {}
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}

    def display_report(self):
        """Display the table booking report in tabular format."""
        if not self.bookings:
            print("No booking data available.")
            return

        print("\n***** TABLE BOOKING REPORT *****\n")
        print("+------------+-------+-----------+-------+")
        print("|    Date    | Table | Customer  | Seats |")
        print("+------------+-------+-----------+-------+")

        for date, tables in self.bookings.items():
            for table_no, details in tables.items():
                customer = details.get("customer", "N/A")
                seats = details.get("seats", 0)
                print(f"| {date} |  {table_no:<5} | {customer:<9} | {seats:<5} |")

        print("+------------+-------+-----------+-------+\n")

