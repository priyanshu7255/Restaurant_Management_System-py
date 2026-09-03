import json 
import os
import sys
from SRC.Domain.Menu.menu import MenuManager

manage = MenuManager()

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


class EmployeeManagement:
    def __init__(self):
        self.path = os.getcwd()
        self.file_path = os.path.join(self.path, 'Restaurant_Management_System-py', 'SRC', 'Database', 'Employee.json')
        self.load_employees()

    def load_employees(self):
        try:
            with open(self.file_path, "r") as f:
                self.Employees = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.Employees = []

    def signin(self):
        email = input("Enter email id: ")    
        password = get_password("Enter your password: ") 

       
        self.load_employees()

      
        for employee in self.Employees:
            if email.lower() == employee["Email_id"].lower() and password == employee["Password"]:
                print("Profile Matched.")
                print("🙏 Welcome to our restaurant 🙏")   
                return
        else:
            print("Invalid credentials. Please enter correct credentials for sign in.")                                  

    def signin_staff(self):
        from SRC.Authentication.manageprofile import AuthenticationManager
        authmgr = AuthenticationManager()
    
        email = input("Enter email id: ")    
        password = get_password("Enter your password: ") 

        self.load_employees()  

        for employee in self.Employees:
            if email.lower() == employee["Email_id"].lower() and password == employee["Password"]:
                print("Profile Matched.")
                print("🙏 Welcome to our restaurant 🙏")
                authmgr.staff_menu()   
                return
        else:
            print("Invalid credentials. Please enter correct credentials for sign in.")
    

    def signin_admin(self):
        from SRC.Authentication.manageprofile import AuthenticationManager
        authmgr = AuthenticationManager()
        
        email = input("Enter email id: ")    
        password = get_password("Enter your password: ") 

        self.load_employees()  

        for employee in self.Employees:
            if email.lower() == employee["Email_id"].lower() and password == employee["Password"]:
                print("Profile Matched.")
                print("🙏 Welcome to our restaurant 🙏") 
                authmgr.admin_menu()  
                return
        else:
            print("Invalid credentials. Please enter correct credentials for sign in.")
