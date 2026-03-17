
file_name = "sample.txt"

with open(file_name, "w") as file:
    file.write("Hello, this is the first line.\n")
    file.write("This is the second line.\n")

print("File created and initial data written.")


with open(file_name, "a") as file:
    file.write("This is an appended line.\n")
    file.write("Another appended line.\n")

print("New lines appended to the file.")