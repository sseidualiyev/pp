def squares_up_to_n(N):
    for i in range(N + 1):
        yield i * i

def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i