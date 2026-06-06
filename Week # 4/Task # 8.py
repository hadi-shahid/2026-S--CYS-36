def total (*numbers):
    sum = 0
    for num in numbers:
        sum = sum + num
    print(f"Total : {sum}")

total(2,10,8)