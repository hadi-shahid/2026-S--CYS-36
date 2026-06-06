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

