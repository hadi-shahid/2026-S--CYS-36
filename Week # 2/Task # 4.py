import random

print(" \t\t---Simple Password Generator--- \n")

length = int(input("Enter password length: "))

use_upper = input("Include uppercase letters? (y/n): ").lower()
use_lower = input("Include lowercase letters? (y/n): ").lower() 
use_digits = input("Include digits? (y/n): ").lower() 
use_special = input("Include special characters? (y/n): ").lower() 

char_pool = ""

if use_upper == "y":
    char_pool += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
if use_lower == "y":
    char_pool += "abcdefghijklmnopqrstuvwxyz"
if use_digits == "y":
    char_pool += "0123456789"
if use_special == "y":
    char_pool += "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

if char_pool == "":
    print("Error: You must select at least one character type!")
else:
    password = "".join(random.choice(char_pool) for _ in range(length))

    print(f"\nGenerated Password : \" {password} \"")