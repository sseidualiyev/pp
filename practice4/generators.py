def squares_up_to_n(N):
    for i in range(N + 1):
        yield i * i

def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i

def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i