import json
import uuid
import os

path = os.getcwd()
file_path = os.path.join(path, 'SRC', 'Database', 'order.json')
Bill_path = os.path.join(path, 'SRC', 'Database', 'bill.json')

def customerbills():

    with open(file_path, "r") as f:
        orderlist = json.load(f)

    payment_id = str(uuid.uuid4())[0:6] 

    if "items" in orderlist:
        total_amount = 0
        bill_items = []

        print("Payment Id: ", payment_id)
        for item in orderlist["items"]:
            print(f"Item: {item['Item Name']}, Quantity: {item['Quantity']}, Size: {item['Size']}, Price: ₹{item['Total Price']}")
            total_amount += item["Total Price"]

            bill_items.append({
                "Item": item['Item Name'],
                "Quantity": item['Quantity'],
                "Size": item['Size'],
                "Price": item['Total Price']
            })

        print("\nTotal Order Amount: ₹", total_amount)

        final_bill = {
            "Payment Id": payment_id,
            "Items": bill_items,
            "Total Amount": total_amount
        }

        if os.path.exists(Bill_path) and os.path.getsize(Bill_path) > 0:
            with open(Bill_path, "r") as f:
                existing_data = json.load(f) 
                if not isinstance(existing_data, list): 
                    existing_data = []
        else:
            existing_data = [] 

        existing_data.append(final_bill)

        with open(Bill_path, "w") as f:
            json.dump(existing_data, f, indent=4)

        print(f"\nYour order has been saved to '{Bill_path}'.")

    else:
        print("Invalid JSON format: 'items' key not found!")

customerbills()

