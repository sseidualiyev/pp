
names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

print("Using enumerate():")
for index, name in enumerate(names):
    print(f"{index}: {name}")

print("\nUsing zip():")
for name, score in zip(names, scores):
    print(f"{name} scored {score}")

print("\nEnumerate + zip:")
for i, (name, score) in enumerate(zip(names, scores), start=1):
    print(f"{i}. {name} → {score}")

value = "123"

print("\nType checking:")
print("Type of value:", type(value))

num = int(value)
print("Converted to int:", num, "| Type:", type(num))

num_float = float(num)
print("Converted to float:", num_float, "| Type:", type(num_float))

num_str = str(num_float)
print("Converted back to string:", num_str, "| Type:", type(num_str))

print("\nType checks:")
print("Is num an int?", isinstance(num, int))
print("Is num_float a float?", isinstance(num_float, float))
print("Is value a string?", isinstance(value, str))