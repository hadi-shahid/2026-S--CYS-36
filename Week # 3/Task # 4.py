def fahrenheit_to_celsius (f):
    return (f-32) * 5 / 9

def celsius_to_fahrenheit (c):
    return (c * 9/5) + 32

choice = input("Enter 'F' to convert from Fahrenheit to Celsius  or 'C' to convert form Celsius to Fahrenheit: ").upper()

if choice == "F":
    f = float(input("Enter temp in Fahrenheit : "))
    print(f"Temperature in Celsius is : {fahrenheit_to_celsius(f)}")

elif choice == "C":
    c = float(input("Enter Temperature in Celsius : "))
    print(f"Temperature in Fahrenheit : {celsius_to_fahrenheit(c)}")

else:
    print("Invalid Choice !")