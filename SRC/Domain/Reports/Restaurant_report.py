import json
import os

class RevenueReport:
    def __init__(self, file_path=None):
        """Initialize the RevenueReport class and load data from JSON file."""
        if file_path is None:
            path = os.getcwd()
            file_path = os.path.join(path, 'SRC', 'Database', 'bill.json')
        
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        """Load billing data from JSON file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return []

    def display_report(self):
        """Display total revenue report in tabular format."""
        total_revenue = 0
        print("\n***** REVENUE REPORT *****\n")
        print("+----+----------------------+-------------------+")
        print("| #  | Payment ID           | Total Amount     |")
        print("+----+----------------------+-------------------+")

        for index, bill in enumerate(self.data, start=1):
            payment_id = bill.get("Payment Id", "N/A")
            total_amount = bill.get("Total Amount", 0)
            total_revenue += total_amount
            print(f"| {index:<2} | {payment_id:<20} | {total_amount:<17} |")

        print("+----+----------------------+-------------------+")
        print(f"|    | TOTAL REVENUE        | {total_revenue:<17} |")
        print("+----+----------------------+-------------------+")


