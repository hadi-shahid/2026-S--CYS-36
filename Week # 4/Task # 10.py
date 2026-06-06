a = int(input("Enter 1st Number (a) : "))
b = int(input("Enter 2nd Number (b) : "))
operation = input("Enter The Operation you want to Perform (+,-,*,/) : ")
if operation == "+":
    sum = a + b
    print(f"The Sum is : {sum}")
elif operation == "-":
    sub = a - b
    print(f"The Subtraction is : {sub}")
elif operation == "*":
    mul = a * b
    print(f"The Multiplication is : ")
elif operation == "/":
    div = a / b
    print(f"The Division is : {div}")
else:
    print("Invalid Operation !")