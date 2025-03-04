import json
import uuid
import os
import logging

path = os.getcwd()
log_file_path = os.path.join(path,'SRC','Logs','Application_log.txt')

logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class CustomerBill:
    def __init__(self):
        self.path = os.getcwd()
        self.file_path = os.path.join(self.path, 'SRC', 'Database', 'order.json')
        self.bill_path = os.path.join(self.path, 'SRC', 'Database', 'bill.json')
        self.payment_id = str(uuid.uuid4())[0:6]
    
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
        try:
            orderlist = self.read_orders()
            
            if "items" not in orderlist:
                error_message = "Invalid JSON format: 'items' key not found!"
                print(error_message)
                logging.error(error_message)
                return
            
            total_amount = 0
            bill_items = []
            
            print("Payment Id: ", self.payment_id)
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
                "Payment Id": self.payment_id,
                "Items": bill_items,
                "Total Amount": total_amount
            }

            self.save_bill(final_bill)
            print(f"\nYour order has been saved to '{self.bill_path}'.")
        
        except Exception as e:
            logging.error(f"Error generating bill: {e}")
    
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
