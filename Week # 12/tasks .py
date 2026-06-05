# def name():
#     print("Hadi Shahid")
# name()
# def name():
#     print("Hadi Shahid")
#     print("UET Lahore")
#     print("Department of Computer Engineering")
#     print("DHA Lahore")
# name()


# def show(n):
#     if n == 0:
#         return
#     print(n)
#     show (n-1)
# show(5)

# def fac(n):
#     if (n == 0 or n==1):
#          return 1
#     else:
#          return n* fac(n-1)
       
# print(fac(6))

# try:
#     name = int(input("Enter any Number : "))
#     print(name)
   
# except Exception as e:
#     print(e)

# print("Hello World")

def fiba (n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fiba(n-1) + fiba(n-2)
    
num = int(input("Enter the number of which you want to calculate the Fibannaci Series : "))
for i in range(num):
    print(fiba(i))

