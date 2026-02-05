students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

nums = [5, 2, 9, 1, 7]

desc = sorted(nums, key=lambda x: -x)
print(desc)

words = ["apple", "kiwi", "banana", "fig"]

by_length = sorted(words, key=lambda w: len(w))
print(by_length)


pairs = [(1, 3), (4, 1), (2, 2)]

sorted_pairs = sorted(pairs, key=lambda x: x[1])
print(sorted_pairs)
