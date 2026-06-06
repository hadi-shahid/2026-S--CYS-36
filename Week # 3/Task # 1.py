def factorial(n):
    fact = 1
    for i in range (1,n+1):
        fact = fact * i
    return fact

def permutation (n,r):
    return factorial(n) // factorial(n-r)

def combination (n,r):
    return factorial(n) // factorial(r)*factorial(n-r)

n = int(input("Enter The Value of n : "))
r = int(input("Enter The Value of r : "))
print(f"\nPermutation of (n,r) : {permutation(n,r)}")
print(f"Combinatiaon of (n,r) : {combination(n,r)}")