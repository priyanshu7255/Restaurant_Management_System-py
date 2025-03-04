import json
import os
import uuid

class EmployeeManager:
    def __init__(self):
        self.path = os.getcwd()
        self.file_path = os.path.join(self.path, 'SRC', 'Database', 'Employee.json')
        self.employee_list = self.load_employees()

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

    def sign_up(self, role):
        """Sign up a new employee with the given role."""
        employee_dict = {
            "Role": role,
            "Id": str(uuid.uuid4())[:7],
            "Name": input("Enter employee name: ").strip(),
            "Email_id": input("Enter employee email id: ").strip(),
            "Password": input("Enter employee password: ").strip()
        }
        
        self.employee_list.append(employee_dict)
        self.save_employees()
        print(f"{role} signed up successfully.")

    def sign_up_admin(self):
        """Sign up a new admin."""
        self.sign_up("Admin")

    def sign_up_staff(self):
        """Sign up a new staff member."""
        self.sign_up("Staff")


