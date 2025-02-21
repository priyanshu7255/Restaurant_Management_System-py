from SRC.Authentication.Sign_up import signUp_Admin
from SRC.Authentication.Sign_up import signUp_staff
from SRC.Authentication.Sign_in import Signin_staff

def AuthenticationMenu(): 
    print("1. Sign in") 
    print("2. Sign up") 
    print("3. Exit") 

    while True:
        userchoice = input("Do you want to sign in/sign up/Exit: ")
        if userchoice == "1":
            Signin_staff()

        elif userchoice == "2":
            while True:
                print("1. Admin Signup")
                print("2. Staff Signup")
                print("3. Exit")
                
                userinput = input("Do you want to sign up as an admin or staff: ")
                if userinput == "1":
                    signUp_Admin() 

                elif userinput == "2":
                    signUp_staff()

                elif userinput == "3":
                    print("Thank you for visiting our restaurant.")
                    break

                else:
                    print("Invalid input.")
        elif userchoice == "3":
            print("Goodbyee!!")
            break

        else:
            print("Invalid input.") 
        


        