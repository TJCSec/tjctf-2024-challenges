import random


def more_matches():
    l = []
    for _ in range(100):
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        l.append(f"{'x' * (x*y)}/{'x' * x}={'x' * (y)}")
    return l


def more_nonmatches():
    l = []
    for _ in range(100):
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        z = (x * y) + (random.randrange(-1, 2, 2) * random.choice([x, y]))
        l.append(f"{'x' * z}/{'x' * x}={'x' * (y)}")
    return l
