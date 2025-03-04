import json
import os

path = os.getcwd()
log_file_path = os.path.join(path,'SRC','Logs','Application_log.txt')

def log_error(error_message):
    with open(log_file_path, "a") as log_file:
        log_file.write(error_message + "\n")

class MenuManager:
    def __init__(self):
        self.path = os.getcwd()
        self.new_path = os.path.join(self.path, 'SRC', 'Database', 'menu.json')
        self.menu_data = self.load_menu()

    def load_menu(self):
        """Load menu data from a JSON file."""
        try:
            with open(self.new_path, "r") as file:
                return json.load(file)
        except FileNotFoundError as e:
            log_error(str(e))
            print("Menu file not found! Creating a new one.")
            return {"breakfast": [], "ice cream": [], "lunch": [], "south indian": [], "dinner": [], "drinks": []}
        except Exception as e:
            log_error(str(e))
            print("An error occurred while loading the menu.")
            return {}

    def save_menu(self):
        """Save menu data to a JSON file."""
        try:
            with open(self.new_path, "w") as file:
                json.dump(self.menu_data, file, indent=4)
        except Exception as e:
            log_error(str(e))
            print("An error occurred while saving the menu.")

    def display_full_menu(self):
        """Display the entire menu across all categories."""
        try:
            print("\n***** FULL MENU *****\n")
            for category, items in self.menu_data.items():
                if not items:
                    continue
                print(f"\n {category.upper()} ")
                print("+----+----------------------+-------------------+------------------------------+")
                print("| #  | Item Name            | Available Sizes   | Price (₹)                    |")
                print("+----+----------------------+-------------------+------------------------------+")
                for index, item in enumerate(items, start=1):
                    item_name = item["Item Name"].strip()
                    sizes = ", ".join(item["Price"].keys())
                    price_details = ", ".join([f"{k}: ₹{v}" for k, v in item["Price"].items()])
                    print(f"| {str(index).ljust(2)} | {item_name.ljust(20)} | {sizes.ljust(17)} | {price_details.ljust(28)} |")
                print("+----+----------------------+-------------------+------------------------------+")
        except Exception as e:
            log_error(str(e))
            print("An error occurred while displaying the menu.")

    def add_menu_item(self):
        """Add a new item to a selected category."""
        try:
            category = input("Enter the category(Breakfast,Drinks,Ice-cream,Lunch,Dinner,South Indian): ").strip().lower()
            if category not in self.menu_data:
                print("Invalid category!")
                return
            item_name = input("Enter item name: ").strip()
            price_data = {}
            if input("Does this item have Full/Half price options? (yes/no): ").strip().lower() == "yes":
                price_data["Full"] = float(input("Enter price for Full: ₹").strip())
                price_data["Half"] = float(input("Enter price for Half: ₹").strip())
            else:
                price_data["Single"] = float(input("Enter price for Single: ₹").strip())
            self.menu_data[category].append({"Item Name": item_name, "Price": price_data})
            self.save_menu()
            print(f"Item '{item_name}' added successfully to {category}!")
        except Exception as e:
            log_error(str(e))
            print("An error occurred while adding the item.")

    def remove_menu_item(self):
        """Remove a menu item from a selected category."""
        try:
            category = input("Enter the category(Breakfast,Drinks,Ice-cream,Lunch,Dinner,South Indian): ").strip().lower()
            if category not in self.menu_data:
                print("Invalid category!")
                return
            self.display_full_menu()
            item_to_remove = int(input("Enter the serial number of the item to remove: ")) - 1
            if 0 <= item_to_remove < len(self.menu_data[category]):
                removed_item = self.menu_data[category].pop(item_to_remove)
                self.save_menu()
                print(f"Item '{removed_item['Item Name']}' removed successfully!")
            else:
                print("Invalid serial number!")
        except ValueError as e:
            log_error(str(e))
            print("Invalid input! Please enter a valid number.")
        except Exception as e:
            log_error(str(e))
            print("An error occurred while removing the item.")

    def update_item(self):
        """Update an item in the menu."""
        try:
            category = input("Enter the category: ").strip().lower()
            if category not in self.menu_data:
                print("Invalid category!")
                return
            self.display_full_menu()
            item_to_update = int(input("Enter the serial number of the item to update: ")) - 1
            if 0 <= item_to_update < len(self.menu_data[category]):
                item = self.menu_data[category][item_to_update]
                new_name = input(f"New name (current: {item['Item Name']}): ").strip()
                if new_name:
                    item["Item Name"] = new_name
                if input("Do you want to update prices? (yes/no): ").strip().lower() == "yes":
                    for size in item["Price"].keys():
                        new_price = input(f"New price for {size} (current: ₹{item['Price'][size]}): ").strip()
                        if new_price:
                            item["Price"][size] = float(new_price)
                self.save_menu()
                print("Item updated successfully!")
            else:
                print("Invalid serial number!")
        except ValueError as e:
            log_error(str(e))
            print("Invalid input! Please enter a valid number.")
        except Exception as e:
            log_error(str(e))
            print("An error occurred while updating the item.")

    def menucard(self):
        """Main function to manage menu operations."""
        while True:
            print("\n1. View Full Menu")
            print("2. Add Item")
            print("3. Remove Item")
            print("4. Update Item")
            print("5. Exit")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.display_full_menu()
            elif choice == "2":
                self.add_menu_item()
            elif choice == "3":
                self.remove_menu_item()
            elif choice == "4":
                self.update_item()
            elif choice == "5":
                print("Exiting... Thank you! 🙏")
                break
            else:
                print("Invalid choice! Please try again.")
