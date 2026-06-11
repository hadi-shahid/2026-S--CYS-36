import os

for file in os.listdir("."):
    if file.endswith(".py"):
        size = os.path.getsize(file)
        print(f"{file} → {size} bytes")