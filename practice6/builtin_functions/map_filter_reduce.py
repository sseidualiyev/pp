
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

squared = list(map(lambda x: x**2, numbers))
print("Squared numbers (map):", squared)

evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers (filter):", evens)

sum_all = reduce(lambda x, y: x + y, numbers)
print("Sum using reduce:", sum_all)

product_all = reduce(lambda x, y: x * y, numbers)
print("Product using reduce:", product_all)