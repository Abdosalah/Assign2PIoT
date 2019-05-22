# from consolemenu import *
# from consolemenu.items import *
# menu = consolemenu("Register", "login")
# menu_item = MenuItem("Menu Item")
# function_item = FunctionItem("Register:", input, )
# from "filename" import "classname"

from dbLogic import DbUser
import re

answer = True
while answer:
    print("""
    1.Register
    2.Login
    """)
    choice=input("Choose 1 or 2:")
    if (choice=="1"):
      print ("Enter your UserName:")
      userName=input()
      print ("Enter your Password:")
      password=input()
      print ("Enter your FirstName:")
      firstName=input()
      print ("Enter your LastName:")
      lastName=input()
      print ("Email:")
      email=input()
      if re.match("\A(?P<name>[\w\-_]+)@(?P<domain>[\w\-_]+).(?P<toplevel>[\w]+)\Z",email,re.IGNORECASE):
        print("Email is valid")
      else
        print("Email is invalid")
            
      newUser = DbUser(userName, password, firstName, lastName, email)

    elif (choice=="2"):
      print ("Enter your UserName:")
      userName=input()
      print ("Enter your Password:")
      password=input()

    elif (choice == "3"):
      answer = False
          
    else:
      print("Invalid Choice")


      
