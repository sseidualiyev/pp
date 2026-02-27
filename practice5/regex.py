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
