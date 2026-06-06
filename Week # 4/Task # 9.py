def average(*number):
    pass
    if len(number) == 0:
        return 0 
    total = sum(number)
    amount = len(number)
    average = total // amount
    return average

print(f"The Average of Numbers ; 2,3,4,5 is : {average(2,3,4,5)}")