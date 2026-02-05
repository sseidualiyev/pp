numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

nums = [1, 2, 3, 4, 5]

squared = list(map(lambda x: x**2, nums))
print(squared)


celsius = [0, 10, 20, 30]

fahrenheit = list(map(lambda c: c * 9/5 + 32, celsius))
print(fahrenheit)


a = [1, 2, 3]
b = [4, 5, 6]

sum_list = list(map(lambda x, y: x + y, a, b))
print(sum_list)
