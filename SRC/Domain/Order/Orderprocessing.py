import json
import uuid
import os

class OrderSystem:
    def __init__(self):
        self.path = os.getcwd()
        self.file_path = os.path.join(self.path, 'SRC', 'Database', 'menu.json')
        self.order_file_path = os.path.join(self.path, 'SRC', 'Database', 'order.json')
        self.items_list = self.load_menu()
        self.ordered_items = []
        self.order_id = str(uuid.uuid4())[0:5]

    def load_menu(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

    def add_item(self):
        user_input = input("Enter the item name you want to order: ").strip().lower()
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
                            print("Invalid size. Please try again.")
                            continue
                        price = price_options[size]
                    else:
                        size = "single"
                        price = price_options if isinstance(price_options, (int, float)) else list(price_options.values())[0]

                    quantity = input(f"How many '{size}' of '{item['Item Name'].strip()}' would you like? ").strip()
                    try:
                        quantity = int(quantity)
                        total_price = price * quantity
                        self.ordered_items.append({
                            "Item Name": item["Item Name"].strip(),
                            "Size": size,
                            "Quantity": quantity,
                            "Total Price": total_price
                        })
                        print(f"'{item['Item Name'].strip()}' x{quantity} ({size}) added to your order.")
                    except ValueError:
                        print("Invalid quantity. Please enter a number.")
                    break

            if found:
                break  

        if not found:
            print("Item not available. Please try again.")

    def remove_item(self):
        if not self.ordered_items:
            print("No items to remove.")
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
                print("Invalid item number.")
        except ValueError:
            print("Please enter a valid number.")

    def finalize_order(self):
        print("Please wait for your food. Your order is being processed.")
        self.display_order_summary()
        self.save_order()

    def display_order_summary(self):
        print("\nYour Order Summary:")
        print(f"Order ID: {self.order_id}")
        for index, item in enumerate(self.ordered_items, start=1):
            print(f"{index}. {item['Item Name']} - {item['Size']} x {item['Quantity']} - ₹{item['Total Price']}")

    def save_order(self):
        order_data = {
            "order_id": self.order_id,
            "items": self.ordered_items
        }
        with open(self.order_file_path, "w") as order_file:
            json.dump(order_data, order_file, indent=4)
        print(f"\nYour order has been saved to '{self.order_file_path}'.")

    def start_order(self):
        while True:
            print("\nOrder Your Food.")
            print("1. Add Item.")
            print("2. Remove Item.")
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
