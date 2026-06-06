larger = lambda a,b : a if a > b else b

def print_table(num,range_limit):
    print(f"Table of {num} : ")
    for i in range (1,range_limit + 1):
        print(f"{num} x {i} = {num*i}")

a = int(input("Enter the 1st Number : "))
b = int(input("Enter the 2nd Number : "))
r = int(input("Enter the Range for the Table : "))
max_num = larger(a,b)
print(f"Larger Number is : {max_num}")
print_table(max_num,r)