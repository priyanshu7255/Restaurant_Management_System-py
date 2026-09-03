import json
import uuid
import os
import logging
import datetime
from SRC.Domain.Order.Orderprocessing import OrderSystem

order = OrderSystem()

path = os.getcwd()
log_file_path = os.path.join(path,'Restaurant_Management_System-py','SRC','Logs','Application_log.txt')

logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class CustomerBill:
    def __init__(self):
        self.path = os.getcwd()
        self.file_path = os.path.join(self.path,'Restaurant_Management_System-py','SRC', 'Database', 'order.json')
        self.bill_path = os.path.join(self.path, 'Restaurant_Management_System','SRC', 'Database', 'bill.json')
        self.payment_id = str(uuid.uuid4())[0:6]
        self.table = order.table_number
    
    def read_orders(self):
        try:
            if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
                with open(self.file_path, "r") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logging.error(f"Error reading orders: {e}")
            return {}
    
    def generate_bill(self):
        """Generate the bill for the latest order, including the table number."""

        try:
            orderlist = self.read_orders()

            if not orderlist or "items" not in orderlist:
                print("⚠ No valid orders found!")
                return

            total_amount = 0
            bill_items = []

            table_number = orderlist.get("table_number", "N/A")
            customer_name = orderlist.get("customer_name", "N/A")

            print("\n🧾 BILL DETAILS 🧾")
            print("--------------------------")
            print(f"Date = {datetime.datetime.now().date()}")
            print(f"Payment ID: {self.payment_id}")
            print(f"Table Number: {table_number}")
            print(f"Customer Name: {customer_name}")
            print("--------------------------")

            for item in orderlist["items"]:
                print(f"Item: {item['Item Name']}, Quantity: {item['Quantity']}, Size: {item['Size']}, Price: ₹{item['Total Price']}")
                total_amount += item["Total Price"]

                bill_items.append({
                    "Item": item['Item Name'],
                    "Quantity": item['Quantity'],
                    "Size": item['Size'],
                    "Price": item['Total Price']
                })

            print("--------------------------")
            print(f"Total Order Amount: ₹{total_amount}")
            print("--------------------------")

            final_bill = {
                "Payment ID": self.payment_id,
                "Table Number": table_number,
                "Customer Name": customer_name,
                "Items": bill_items,
                "Total Amount": total_amount
            }

            self.save_bill(final_bill)
            print(f"\n✅ Your bill has been saved to '{self.bill_path}'.")

        except Exception as e:
            print(f"⚠ Error generating bill: {e}")

    
    def save_bill(self, bill):
        try:
            if os.path.exists(self.bill_path) and os.path.getsize(self.bill_path) > 0:
                with open(self.bill_path, "r") as f:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, list):
                        existing_data = []
            else:
                existing_data = []
            
            existing_data.append(bill)
            
            with open(self.bill_path, "w") as f:
                json.dump(existing_data, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving bill: {e}")
