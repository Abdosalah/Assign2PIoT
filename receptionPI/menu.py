

from dbLogic import DbUser


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
            
      newUser = DbUser('library.db')

    elif (choice=="2"):
      print ("Enter your UserName:")
      userName=input()
      print ("Enter your Password:")
      password=input()

    elif (choice == "3"):
      answer = False
          
    else:
      print("Invalid Choice")





      
