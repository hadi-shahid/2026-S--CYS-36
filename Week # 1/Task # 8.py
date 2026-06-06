username = input("Enter Your Username : ")
if (username == "Admin" or username == "admin"):
    print("Welcome Administrator")
elif (username == "Guest" or username == "guest"):
    print("Welcome Guest")
else:
    print("Access Denied")