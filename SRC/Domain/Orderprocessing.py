import json
import uuid
import os

path = os.getcwd()
file_path = os.path.join(path, 'SRC', 'Database', 'menu.json')
order_file_path = os.path.join(path, 'SRC', 'Database', 'order.json')

with open(file_path, "r") as f:
    Items_list = json.load(f)

def display_menu():
    print("\n***** MENU *****\n")
    
    for category, items in Items_list.items():
        print(f"\n {category.upper()} ")
        print("+----+----------------------+-------------------+------------+")
        print("| #  | Item Name            | Available Sizes   | Price (₹)  |")
        print("+----+----------------------+-------------------+------------+")
        index = 1
        
        for item in items:
            item_name = item["Item Name"].strip()
            sizes = ", ".join(item["Price"].keys())  
            price_details = ", ".join([f"{k}: ₹{v}" for k, v in item["Price"].items()])
            print(f"| {str(index).ljust(2)} | {item_name.ljust(20)} | {sizes.ljust(17)} | {price_details.ljust(10)} |")
            index += 1
        
        print("+----+----------------------+-------------------+------------+")       

def order():
    order_id = str(uuid.uuid4())[0:5]  
    ordered_items = []
    userchoice=input("Enter 1 for display menu: ")
    if userchoice == "1":
        display_menu()   

    while True:
        print("\n1. Add item.")
        print("2. Remove item.")
        print("3. Exit.")
        userinput1 = input("Enter your choice: ").strip()

        if userinput1 == "1":
            user_input = input("Enter the item name you want to order: ").strip().lower()
            found = False

            for category, items in Items_list.items():  
                for item in items:
                    if user_input == item["Item Name"].strip().lower():
                        found = True
                        price_options = item["Price"]
                        
                        if len(price_options) > 1:
                            print("Available sizes:", ", ".join(price_options.keys()))
                            size = input("Enter size (half/full): ").strip().lower()
                            if size not in price_options:
                                print("Invalid size. Please try again.")
                                continue
                            price = price_options[size]
                        else:
                            size = "single"
                            price = price_options[size]

                        quantity = input(f"How many '{size}' of '{item['Item Name'].strip()}' would you like? ").strip()
                        try:
                            quantity = int(quantity)
                            total_price = price * quantity
                            ordered_items.append({
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

        elif userinput1 == "2":
            if not ordered_items:
                print("No items to remove.")
            else:
                print("\nYour Current Order:")
                print("+----+----------------------+--------+----------+--------------+")
                print("| #  | Item Name            | Size   | Quantity | Total Price (₹) |")
                print("+----+----------------------+--------+----------+--------------+")
                index = 1
                for item in ordered_items:
                    print(f"| {str(index).ljust(2)} | {item['Item Name'].ljust(20)} | {item['Size'].ljust(6)} | {str(item['Quantity']).ljust(8)} | {str(item['Total Price']).ljust(12)} |")
                    index += 1
                print("+----+----------------------+--------+----------+--------------+")

                try:
                    remove_idx = int(input("Enter the number of the item to remove: "))
                    if 1 <= remove_idx <= len(ordered_items):
                        removed_item = ordered_items.pop(remove_idx - 1)
                        print(f"Removed '{removed_item['Item Name']}' from your order.")
                    else:
                        print("Invalid item number.")
                except ValueError:
                    print("Please enter a valid number.")

        elif userinput1 == "3":
            print("Please wait for your food. Your order is being processed.")
            break

        else:
            print("Invalid input. Please enter 1, 2, or 3.")

    print("\nYour Order Summary:")
    print(f"Order ID: {order_id}")
    print("+----+----------------------+--------+----------+--------------+")
    print("| #  | Item Name            | Size   | Quantity | Total Price (₹) |")
    print("+----+----------------------+--------+----------+--------------+")
    index = 1
    for item in ordered_items:
        print(f"| {str(index).ljust(2)} | {item['Item Name'].ljust(20)} | {item['Size'].ljust(6)} | {str(item['Quantity']).ljust(8)} | {str(item['Total Price']).ljust(12)} |")
        index += 1
    print("+----+----------------------+--------+----------+--------------+")

    order_data = {
        "order_id": order_id,
        "items": ordered_items
    }

    with open(order_file_path, "w") as order_file:
        json.dump(order_data, order_file, indent=4)

    print(f"\nYour order has been saved to '{order_file_path}'.")
