import json
import uuid

path = r"C:\IndixpertRestaurantProject\Restaurant_Management_System-py\SRC\Database\order.json"

def bills():
    with open(path, "r") as f:
        orderlist = json.load(f)

    payment_id = str(uuid.uuid4())[0:6]

    if "items" in orderlist:
        total_amount = 0

        print("Payment Id: ",payment_id)
        for item in orderlist["items"]:
            print(f"Item: {item['Item Name']},Quantity: {item['Quantity']} Price: ₹{item['Total Price']}")
            total_amount += item["Total Price"] 

        print("\nTotal Order Amount: ₹", total_amount)  
    else:
        print("Invalid JSON format: 'items' key not found!")