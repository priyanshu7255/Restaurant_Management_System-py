import json
import os
import uuid

path = r"C:\IndixpertRestaurantProject\Restaurant_Management_System-py\SRC\Database\Employee.json"

if os.path.exists(path):
    with open(path, "r") as f:
        try:
            Employee_list = json.load(f)  
        except json.JSONDecodeError:
            Employee_list = []     
else:        
    Employee_list = []

unique = str(uuid.uuid4())[0:7]   

def signUp_Admin():
        Employee_Dict = {}
        Employee_Dict["Role"] = "Admin"
        Employee_Dict["Id"] = unique
        Employee_Dict["Name"] = input("Enter employee name: ")
        Employee_Dict["Email_id"] = input("Enter employee email id: ")
        Employee_Dict["password"] = input("Enter employee password: ")
    
        Employee_list.append(Employee_Dict)
        with open(path, "w") as f:
            json.dump(Employee_list,f, indent = 4)

        print("Employee signed up successfully.")  

def signUp_staff():
        Employee_Dict = {}
        Employee_Dict["Role"] = "Staff"
        Employee_Dict["Id"] = unique
        Employee_Dict["Name"] = input("Enter employee name: ")
        Employee_Dict["Email_id"] = input("Enter employee email id: ")
        Employee_Dict["password"] = input("Enter employee password: ")
        
        Employee_list.append(Employee_Dict)
        with open(path, "w") as f:
            json.dump(Employee_list,f, indent = 4)

        print("Employee signed up successfully.")            

 
     
         