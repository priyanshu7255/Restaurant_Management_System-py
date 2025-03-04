from SRC.Authentication.Sign_up import EmployeeManager
from SRC.Authentication.Sign_in import EmployeeManagement
from SRC.Domain.Menu.menu import MenuManager 
from SRC.Domain.Order.Orderprocessing import OrderSystem
from SRC.Domain.Bill.Generatebills import CustomerBill
from SRC.Domain.Booking.tablebooking import Restaurant

manage = MenuManager()
order = OrderSystem()
bill = CustomerBill()
restaurant = Restaurant()

class AuthenticationManager:
    def __init__(self):
        self.emp_mgmt = EmployeeManagement()
        self.emp_mgr = EmployeeManager()
    
    def display_menu(self):
            print("\n--- Authentication Menu ---")
            print("1. Sign in")
            print("2. Sign up")
            print("3. Exit")
            
            try:
                userchoice = int(input("Choose an option: "))
                if userchoice == 1:
                    self.sign_in()
                elif userchoice == 2:
                    self.sign_up()
                elif userchoice == 3:
                    print("Goodbye!")
                else:
                    print("Invalid input. Please enter 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def sign_in(self):
            print("\n--- Sign In ---")
            print("1. Admin Sign in")
            print("2. Staff Sign in")
            print("3. Exit")

            try:
                input1 = int(input("Enter your choice: "))

                if input1 == 1:
                    success = self.emp_mgmt.signin_admin()                    
                    self.admin_menu()

                elif input1 == 2:
                    success = self.emp_mgmt.signin_staff()
                    self.staff_menu()

                elif input1 == 3:
                    print("Goodbye!")
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def admin_menu(self):
        """ Admin menu after successful login """
        while True:
            print("\n--- Admin Menu ---")
            print("1. View Full Menu.")
            print("2. Add Item.")
            print("3. Remove Item.")
            print("4. Update Item.")
            print("5. Logout.")

            choice = input("Enter your choice: ").strip()
            if choice == "1":
                manage.display_full_menu()
            elif choice == "2":
                manage.add_menu_item()
            elif choice == "3":
                manage.remove_menu_item()
            elif choice == "4":
                manage.update_item()
            elif choice == "5":
                print("Logging out... Thank you!")
                break
            else:
                print("Invalid choice! Please try again.")

    def staff_menu(self):
        """ Staff menu after successful login """
        order_placed = False  

        while True:
            print("\n--- Staff Menu ---")
            print("1. View Full Menu.")
            print("2. Book your Table.")
            print("3. Order your food.")
            print("4. Generate bill.")
            print("5. Exit.") 

            try:
                ipt = int(input("Enter your choice: "))

                if ipt == 1:
                    manage.display_full_menu()
                
                elif ipt == 2:                            
                    while True:
                        print("\n--- Table Booking Menu ---")
                        print("1. View available tables")
                        print("2. Book a table")
                        print("3. View bookings")
                        print("4. Cancel booking")
                        print("5. Back to Staff Menu")
                        
                        try:
                            table_choice = int(input("Enter your choice: "))

                            if table_choice == 1:
                                date = input("Enter date (DD-MM-YYYY): ")
                                print("\n".join(restaurant.view_available_tables(date)))
                            elif table_choice == 2:
                                date = input("Enter booking date (DD-MM-YYYY): ")
                                customer_name = input("Enter your name: ")
                                seats = int(input("Enter number of seats required: "))
                                print(restaurant.book_table(seats, customer_name, date))
                            elif table_choice == 3:
                                date = input("Enter date (DD-MM-YYYY) to view bookings: ")
                                print("\n".join(restaurant.view_bookings(date)))
                            elif table_choice == 4:
                                date = input("Enter booking date (DD-MM-YYYY): ")
                                table_number = int(input("Enter table number to cancel: "))
                                print(restaurant.cancel_booking(table_number, date))
                            elif table_choice == 5:
                                break  
                            else:
                                print("Invalid choice, please try again.")
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")

                elif ipt == 3:    
                    order.start_order()
                    order_placed = True 
                
                elif ipt == 4:
                    if not order_placed:
                        print("Error: You must place an order before generating a bill!")
                    else:
                        bill.generate_bill()
                
                elif ipt == 5:
                    print("Goodbye!")
                    break
                
                else:
                    print("Invalid number.")

            except ValueError:
                print("Invalid input. Please enter a number.")

    def sign_up(self):
        while True:
            print("\n--- Sign Up ---")
            print("1. Admin Signup")
            print("2. Staff Signup")
            print("3. Back to Main Menu")

            try:
                userinput = int(input("Choose your role: "))
                if userinput == 1:
                    self.emp_mgr.sign_up_admin()
                elif userinput == 2:
                    self.emp_mgr.sign_up_staff()
                elif userinput == 3:
                    break
                else:
                    print("Invalid input. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
