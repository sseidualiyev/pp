# 1
import re

s = input("Task 1: ")
if re.fullmatch(r"ab*", s):
    print("Match")
else:
    print("No match")
