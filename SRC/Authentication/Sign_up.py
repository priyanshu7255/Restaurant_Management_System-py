import json
import os
import uuid
import sys

if os.name == 'nt':  
    import msvcrt
    def get_password(prompt="Enter your password: "):
        print(prompt, end="", flush=True)
        password = ""
        while True:
            char = msvcrt.getch().decode("utf-8")
            if char == "\r" or char == "\n":  
                print() 
                break
            elif char == "\b":  
                if len(password) > 0:
                    sys.stdout.write("\b \b")  
                    sys.stdout.flush()
                    password = password[:-1]
            else:
                sys.stdout.write("*") 
                sys.stdout.flush()
                password += char
        return password

class EmployeeManager:
    def __init__(self):
        self.path = os.getcwd()
        self.file_path = os.path.join(self.path, 'Restaurant_Management_System-py', 'SRC', 'Database', 'Employee.json')
        self.employee_list = self.load_employees()  

    def load_employees(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def save_employees(self):
        with open(self.file_path, "w") as f:
            json.dump(self.employee_list, f, indent=4)

    def is_email_registered(self, email):
        return any(employee["Email_id"].lower() == email.lower() for employee in self.employee_list)

    def sign_up(self, role):
        name = input("Enter employee name: ").strip()
        email = input("Enter employee email id: ").strip()

        if self.is_email_registered(email):
            print("This email is already registered. Try logging in instead.")
            return

        password = get_password("Enter employee password: ").strip()
        employee_dict = {
            "Role": role,
            "Id": str(uuid.uuid4())[:7],  
            "Name": name,
            "Email_id": email,
            "Password": password  
        }

        self.employee_list.append(employee_dict)
        self.save_employees()  

        print(f"{role} signed up successfully.")
        
        self.employee_list = self.load_employees()

       
        self.sign_in_after_signup(email, password)

    def sign_in_after_signup(self, email, password):
        print("\nYou have successfully signed up!")
        self.load_employees()  
        
        for employee in self.employee_list:
            if email.lower() == employee["Email_id"].lower() and password == employee["Password"]:
              
                print("🙏 Welcome to our restaurant 🙏")
                return
        print("Error during auto sign-in. Please try to log in manually.")
    
    def sign_up_staff(self):
       
        self.sign_up("Staff")

    def sign_up_admin(self):
        
        invite_code = input("Enter invite code: ")
        if invite_code == self.Admin_invite_code:
            self.sign_up("Admin")
        else:
            print("Invalid invite code.")
