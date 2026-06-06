base = int(input("Enter a Base Number : "))
exponant = int(input("Enter an Exponent Number : "))
def power (base,exponent = 2):
    power = base ** exponant
    print(f"The Power of the Number will be : {power}")
    return
    
power(base,exponant)
power (base)