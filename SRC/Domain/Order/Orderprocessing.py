import json
import uuid
import os
import datetime 
from SRC.Domain.Booking.tablebooking import Restaurant
from SRC.Domain.Reports.tablebooking_report import TableBookingReport 
class OrderSystem:
    

    def __init__(self):
        """Initialize the order system with restaurant booking integration."""
        self.restaurant = Restaurant()
        self.table = TableBookingReport() 
        self.path = os.getcwd()
        self.file_path2 = os.path.join(self.path,'SRC','Database','table_booking.json')
        self.file_path = os.path.join(self.path, 'SRC', 'Database', 'menu.json')
        self.order_file_path = os.path.join(self.path, 'SRC', 'Database', 'order.json')
        self.items_list = self.load_menu()
        self.ordered_items = []
        self.order_id = str(uuid.uuid4())[0:5]
        self.table_number = None
        self.customer_name = None

    def load_menu(self):
        """Load the menu from the JSON file."""
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(" Menu file not found! Please check the file path.")
            return {}
        

    def add_item(self):
        """Add food items to the order."""
        user_input = input("\nEnter the item name you want to order: ").strip().lower()
        found = False

        for category, items in self.items_list.items():
            for item in items:
                if user_input == item["Item Name"].strip().lower():
                    found = True
                    price_options = item["Price"]

                    if isinstance(price_options, dict) and len(price_options) > 1:
                        print("Available sizes:", ", ".join(price_options.keys()))
                        size = input(f"Enter size ({'/'.join(price_options.keys())}): ").strip().lower()
                        if size not in price_options:
                            print("⚠ Invalid size. Please try again.")
                            return
                        price = price_options[size]
                    else:
                        size = "single"
                        price = price_options if isinstance(price_options, (int, float)) else list(price_options.values())[0]

                    try:
                        quantity = int(input(f"How many '{size}' of '{item['Item Name'].strip()}' would you like? ").strip())
                        total_price = price * quantity
                        self.ordered_items.append({
                            "Item Name": item["Item Name"].strip(),
                            "Size": size,
                            "Quantity": quantity,
                            "Total Price": total_price
                        })
                        print(f" '{item['Item Name'].strip()}' x{quantity} ({size}) added to your order.")
                    except ValueError:
                        print("⚠ Invalid quantity. Please enter a number.")
                    break

            if found:
                break

        if not found:
            print("⚠ Item not available. Please try again.")

    def remove_item(self):
        """Remove items from the order."""
        if not self.ordered_items:
            print("ℹ No items to remove.")
            return
        
        print("\nYour Current Order:")
        for index, item in enumerate(self.ordered_items, start=1):
            print(f"{index}. {item['Item Name']} - {item['Size']} x {item['Quantity']} - ₹{item['Total Price']}")

        try:
            remove_idx = int(input("Enter the number of the item to remove: "))
            if 1 <= remove_idx <= len(self.ordered_items):
                removed_item = self.ordered_items.pop(remove_idx - 1)
                print(f"Removed '{removed_item['Item Name']}' from your order.")
            else:
                print("⚠ Invalid item number.")
        except ValueError:
            print("⚠ Please enter a valid number.")

    def finalize_order(self):
        """Finalize the order and book a table after ordering."""
        print("\nOrder Placed! Please wait while we process your order.")
        self.display_order_summary()
        self.book_table_after_order()
        self.save_order()

    def display_order_summary(self):
        """Display the final order summary."""
        print("\n Your Order Summary:")
        print(f" Order ID: {self.order_id}")
        for index, item in enumerate(self.ordered_items, start=1):
            print(f"{index}. {item['Item Name']} - {item['Size']} x {item['Quantity']} - ₹{item['Total Price']}")
        if self.table_number:
            print(f"Table Number: {self.table_number}")

    def load_booked_tables(self):
        """Load the booked tables from the JSON file."""
        try:
            with open(self.file_path2, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def is_table_booked(self, table_number):
        """Check if a table is already booked."""
        booked_tables = self.load_booked_tables()
        today_date = datetime.date.today().strftime("%d-%m-%Y")

        if today_date in booked_tables:
            if isinstance(booked_tables[today_date], list):
                return any(entry.get('table_number') == table_number for entry in booked_tables[today_date])
    
        return False


    def book_table_after_order(self):
        """Ask the user if they want to book a table after placing their order."""

        self.file_path2 = os.path.join(self.path, 'SRC', 'Database', 'table_booking.json')

        # Available tables with their seating capacities
        available_tables = {1: 2, 2: 4, 3: 6, 4: 8, 5: 10, 6: 12, 7: 14, 8: 16, 9: 18, 10: 20}
        today_date = datetime.date.today().strftime("%d-%m-%Y")

        # Load already booked tables
        booked_tables = set()
        bookings = {}

        try:
            with open(self.file_path2, "r") as file:
                bookings = json.load(file)
                if today_date in bookings:
                    booked_tables = set(map(int, bookings[today_date].keys()))
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠ Error accessing booking data. Assuming no prior bookings.")

        while True:
            # Display available tables
            print("\nAvailable Tables:")
            for table, capacity in available_tables.items():
                status = "(Booked)" if table in booked_tables else "(Available)"
                print(f"Table {table}: Capacity {capacity} {status}")

            book_table = input("\nWould you like to book a table now? (yes/no): ").strip().lower()

            if book_table in ["yes", "no"]:
                # Ask for customer name in both cases
                while True:
                    self.customer_name = input("Enter your name: ").strip()
                    if self.customer_name:
                        break
                    print("⚠ Name cannot be empty. Please enter a valid name.")

            if book_table == "yes":
                try:
                    table_number = int(input("Enter the table number you want to book: ").strip())

                    if table_number not in available_tables:
                        print("⚠ Table not available. Please select another table.")
                        continue
                    if table_number in booked_tables:
                        print("⚠ This table is already booked. Please choose another.")
                        continue
                except ValueError:
                    print("⚠ Invalid input! Please enter a valid table number.")
                    continue

                if today_date not in bookings:
                    bookings[today_date] = {}
                bookings[today_date][str(table_number)] = {
                    "customer": self.customer_name,
                    "seats": available_tables[table_number]
                }

                with open(self.file_path2, "w") as file:
                    json.dump(bookings, file, indent=4)

                print(f"✅ Table {table_number} successfully booked for {self.customer_name}.")
                self.table_number = table_number  # Store table number for bill
                break  

            elif book_table == "no":
                while True:
                    inpt = input("Do you have any previous booking? (yes/no): ").strip().lower()

                    if inpt == "yes":
                        try:
                            with open(self.file_path2, "r") as file:
                                previous_bookings = json.load(file)

                            
                                prev_table_number = input("Enter the table number you booked: ").strip()
                                if not prev_table_number.isdigit():
                                    print("⚠ Invalid input! Please enter a valid table number.")
                                    continue
                                prev_table_number = int(prev_table_number)

                                if today_date in previous_bookings and str(prev_table_number) in previous_bookings[today_date]:
                                    print(f"✅ Your booking for Table {prev_table_number} is confirmed.")
                                    self.table_number = prev_table_number  # Store previous table number for bill
                                    break
                                else:
                                    print("⚠ No booking found for this table. Please enter the correct table number.")
                                    break
                        except (FileNotFoundError, json.JSONDecodeError):
                            print("⚠ Error accessing previous bookings. Please try again.")

                    break  
            else:
                print("⚠ Invalid input. Please enter 'yes' or 'no'.")

 
   
    def save_order(self):
        """Save only the latest order to a JSON file (overwrite previous orders)."""

        order_data = {
            "order_id": self.order_id,
            "items": self.ordered_items,
            "table_number": self.table_number,
            "customer_name": self.customer_name
        }

        with open(self.order_file_path, "w") as order_file:
            json.dump(order_data, order_file, indent=4)

        print(f"\nYour latest order has been saved to '{self.order_file_path}'.")


    def start_order(self):
        """Start the ordering process."""
        while True:
            print("\n Order Your Food:")
            print("1. Add Item")
            print("2. Remove Item")
            print("3. Finalize Order")
            userinput = input("Enter your choice: ").strip()

            if userinput == "1":
                self.add_item()
            elif userinput == "2":
                self.remove_item()
            elif userinput == "3":
                self.finalize_order()
                break
            else:
                print("Invalid input. Please enter 1, 2, or 3.")


