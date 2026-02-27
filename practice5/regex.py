# 1
import re

s = input("Task 1: ")
if re.fullmatch(r"ab*", s):
    print("Match")
else:
    print("No match")

# 2
s = input("Task 2: ")
if re.fullmatch(r"ab{2,3}", s):
    print("Match")
else:
    print("No match")

# 3
s = input("Task 3: ")
matches = re.findall(r"[a-z]+_[a-z]+", s)
print(matches)

# 4
s = input("Task 4: ")
matches = re.findall(r"[A-Z][a-z]+", s)
print(matches)

# 5
s = input("Task 5: ")
if re.fullmatch(r"a.*b", s):
    print("Match")
else:
    print("No match")

# 6
s = input("Task 6: ")
result = re.sub(r"[ ,\.]", ":", s)
print(result)

# 7
s = input("Task 7: ")
parts = s.split("_")
camel_case = parts[0] + "".join(word.capitalize() for word in parts[1:])
print(camel_case)

# 8
s = input("Task 8: ")
split_upper = re.findall(r"[A-Z][a-z]*", s)
print(split_upper)
