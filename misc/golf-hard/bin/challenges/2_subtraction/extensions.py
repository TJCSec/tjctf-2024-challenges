import random


def more_matches():
    a = [random.randint(100, 1000) for _ in range(100)]
    b = [random.randint(0, i) for i in a]
    l = [f"{'x'*i}-{'x'*j}={'x'*(i-j)}" for i, j in zip(a, b)]
    return l


def more_nonmatches():
    a = [random.randint(100, 1000) for _ in range(100)]
    b = [random.randint(0, i) for i in a]
    l = [
        f"{'x'*x}-{'x'*y}={'x'*(random.choice(list({*range(0,x-y)} | {*range(x-y+1, 1000)})))}"
        for x, y in zip(a, b)
    ]
    return l
