import os

os.mkdir("Scripts")
for i in range(1, 6):
    open(f"Scripts/script{i}.py", "w")