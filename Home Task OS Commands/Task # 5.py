import os

for i, file in enumerate(os.listdir("Scripts")):
    os.rename(f"Scripts/{file}", f"Scripts/renamed_{i}.py")