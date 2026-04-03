a = int(input("Enter Obtained Marks : "))
b = int(input("Enter Total Marks : "))
c = a/b  * 100
print("Your average is : ",c )
if c == 0:
    print("Invalid Grade")
    
elif c > 100:
    print("Invalid Grade")
    
elif a > b or a > 300:
    print("Invalid Grade")
else: 

      if c >= 90:
        print("Grade A")
      elif c >= 85:
        print("Grade A-")
      elif c >= 80:
         print("Grade B+")
      elif c >= 75:
          print("Grade B")
      elif c >= 70:
         print("Grade B-")
      elif c >= 65:
         print("Grade C+")
      elif c >= 60:
         print("Grade C")
      elif c >= 55:
            ("Grade C-")
      elif c >= 50:
            print("Grade D")
      elif c <= 49:
            print("Grade F")


