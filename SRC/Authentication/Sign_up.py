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
        self.file_path = os.path.join(self.path, 'SRC', 'Database', 'Employee.json')
        self.employee_list = self.load_employees()
        self.Admin_invite_code = "Admin@123"
        self.Staff_invite_code = "Staff@123"

    def load_employees(self):
        """Load employee data from a JSON file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def save_employees(self):
        """Save employee data to a JSON file."""
        with open(self.file_path, "w") as f:
            json.dump(self.employee_list, f, indent=4)

    def is_email_registered(self, email):
        """Check if an email is already registered."""
        return any(employee["Email_id"].lower() == email.lower() for employee in self.employee_list)

    def sign_up(self, role, invite_code=None):
        """Sign up a new employee with the given role."""
        if role == "Admin":
            entered_code = get_password("Enter admin invitation code: ").strip()
            if entered_code != self.Admin_invite_code:
                print("Invalid invitation code! Only authorized users can sign up as admin.")
                return
        elif role == "Staff":
            entered_code = get_password("Enter staff invitation code: ").strip()
            if entered_code != self.Staff_invite_code:
                print("Invalid invitation code! Only authorized users can sign up as staff.")
                return

        name = input("Enter employee name: ").strip()
        email = input("Enter employee email id: ").strip()

        if self.is_email_registered(email):
            print("This email is already registered. Try logging in instead.")
            return

        password = input("Enter employee password: ").strip()
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

    def sign_up_admin(self):
        """Sign up a new admin with an invitation code."""
        self.sign_up("Admin")

    def sign_up_staff(self):
        """Sign up a new staff member (no invite code needed)."""
        self.sign_up("Staff")

if __name__ == "__main__":
    manager = EmployeeManager()
    
    while True:
        print("\n1. Sign up as Admin")
        print("2. Sign up as Staff")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            manager.sign_up_admin()
        elif choice == "2":
            manager.sign_up_staff()
        elif choice == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Please select again.")
