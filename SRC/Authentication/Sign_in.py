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
        self.file_path = os.path.join(self.path, 'SRC', 'Database', 'Employee.json')
        self.load_employees()

    def load_employees(self):
        try:
            with open(self.file_path, "r") as f:
                self.Employees = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.Employees = []

    def signin(self, role):
        while True:
            username = input("Enter your name: ")    
            password = get_password("Enter your password: ") 

            for employee in self.Employees:
                if username == employee["Name"] and password == employee["password"] and role == employee["Role"]:
                    print("Profile Matched.")
                    print("🙏 Welcome to our restaurant 🙏")   
                    return
            else:
                print("Invalid credentials.Please enter correct credentials for sign in.")                                  
                
    def signin_staff(self):
        return self.signin("Staff")

    def signin_admin(self):
        return self.signin("Admin")
