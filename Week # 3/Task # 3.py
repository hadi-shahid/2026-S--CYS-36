to_uppercase = lambda text: text.upper()

def invert(uppercased_string):
  
    reversed_string = uppercased_string[::-1]
    print(f"Inverted Uppercased String: {reversed_string}")

user_input = input("Enter a string: ")
upper_str = to_uppercase(user_input)

print(f"Uppercased String: {upper_str}")
invert(upper_str)