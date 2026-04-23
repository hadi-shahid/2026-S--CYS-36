d = int(input("Enter total number of students : "))
i = 1
while i<d:
    print( )
    e = (input("Enter Student Name : "))
    f = int(input("Enter Student Roll no. : "))
    a = int(input("Enter Obtained Marks : "))
    b = 300
    c = a/b  * 100
    print ( )
    print ("Name : ",e)
    print ("Roll NO. : ",f)
    print ("Obtained Marks : ",a)
    print ("Percentage : ",c)

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
    i += 1


