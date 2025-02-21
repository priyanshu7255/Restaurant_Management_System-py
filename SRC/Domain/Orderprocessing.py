import json
import uuid
import os

path = os.getcwd()

file_path = os.path.join(path, 'SRC', 'Database', 'menu.json')


with open(file_path, "r") as f:
    Items_list = json.load(f)
def order():
    Items_json = json.dumps(Items_list, indent=4).lower()
    print("Available Menu Items:")
    
    order_id = str(uuid.uuid4())[0:5]  
    ordered_items = []  

    while True:
        user_input = input("What do you want to eat? ")
        if user_input not in Items_json:
            print("Item is not available.")
        else:
            ordered_items.append(user_input)  
            userinput1 = input("Do you want to add more dishes? (1: yes / 0: no): ")
            if userinput1 == "1":
                continue  
            elif userinput1 == "0":
                print("Please wait for your food.")
                break
            else:
                print("Invalid input. Please enter either 1 or 0.")


    print("\nYour Order:")
    print(f"Order ID: {order_id}")
    counter = 1
    for item in ordered_items:
        print(f"{counter}. {item}") 
        counter += 1 


