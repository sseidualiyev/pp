students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

nums = [5, 2, 9, 1, 7]

desc = sorted(nums, key=lambda x: -x)
print(desc)
