
file_name = "sample.txt"

try:
    with open(file_name, "r") as file:
        content = file.read()
        print("File contents:\n")
        print(content)
except FileNotFoundError:
    print("File not found. Please run write_files.py first.")