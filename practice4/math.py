import math
degree = float(input("Input degree: "))
radian = degree * (math.pi / 180)
print("Output radian:", round(radian, 6))

height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
area_trapezoid = 0.5 * (base1 + base2) * height
print("Expected Output:", area_trapezoid)