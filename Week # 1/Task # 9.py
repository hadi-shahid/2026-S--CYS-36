sentence = input("Enter a Sentence : ").lower( )
if "python" in sentence:
    if sentence.startswith ("python"):
        print("Sentence Starts with Python.")
    elif sentence.endswith ("python"):
        print("Sentence Ends with Python.")
    else:
        print("Sentence Contains Python.")
else:
    print("Sentence does Not contain Python")