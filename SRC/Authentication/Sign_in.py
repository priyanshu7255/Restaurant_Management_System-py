import json 
import os

path = os.getcwd()

file_path = os.path.join(path,'SRC','Database','Employee.json')

with open(file_path,"r") as f:
    Employees = json.load(f)

def Signin_staff():

    Username = input("Enter your name: ")    
    Password = input("Enter your password: ")

    for E in Employees:
        
        if Username == E["Name"] and Password == E["password"]:
            print("Profile Matched.")
            print("🙏 Welcome to our restaurant 🙏")
            break
    else:
        print("Invalid credintials.")

            