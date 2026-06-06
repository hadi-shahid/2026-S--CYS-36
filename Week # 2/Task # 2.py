sentence = input("Enter a Sentence : ")
vowels = "aeiouAEIOU"
vowel_count = 0
constant_count = 0
for i in range(len(sentence)):
    char = sentence[i]
    if ("a" <= char <= "z") or ("A" <= char <= "Z"):
        if char in vowels:
            vowel_count += 1
        else:
            constant_count += 1

print("The Number of Vowels : ",vowel_count)
print("The Number of Consonants : ",constant_count) 