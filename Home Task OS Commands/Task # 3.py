import os

os.mkdir("Projects")
for i in range(1, 6):
    os.makedirs(f"Projects/Project {i}")
    open(f"Projects/Project {i}/main.py", "w")