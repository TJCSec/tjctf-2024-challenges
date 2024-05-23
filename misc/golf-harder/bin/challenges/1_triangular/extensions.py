import random

def more_matches():
    l = []
    for _ in range(100):
        i = random.randint(1, 1000)
        l.append("x" * (i * (i + 1) // 2))
    return l


def more_nonmatches():
    l = []
    triangular_nums = {i * (i + 1) // 2 for i in range(10000)}
    for _ in range(100):
        i = random.randint(1, 10000)
        if i not in triangular_nums:
            l.append("x" * i)
    return l
