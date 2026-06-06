start = int(input("Enter The Start of the Range : "))
end = int(input("Enter The End of the Range : "))
prime_numbers = []
prime_sum = 0

for num in range(start,end,1):
    if num > 1:
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            prime_numbers.append(num)
            prime_sum += num

print (f"Prime numbers in the range : {prime_numbers}")
print(f"Sum of the Prime Numbers :  {prime_sum}")