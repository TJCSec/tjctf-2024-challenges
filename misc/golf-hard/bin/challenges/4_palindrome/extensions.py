import random
from string import ascii_lowercase as letters


def more_matches():
    l = []
    for _ in range(100):
        s = "".join(random.choices(letters, k=random.randint(1, 20)))
        if random.random() < 0.5:
            s += random.choice(letters)
        s += s[::-1]
        l.append(s)
    return l


def more_nonmatches():
    l = []
    for _ in range(100):
        s = "".join(random.choices(letters, k=random.randint(1, 20)))
        if random.random() < 0.5:
            s += random.choice(letters)
        s += s[::-1]
        s = list(s)
        while s == s[::-1]:
            s.insert(random.randint(0, len(s)), random.choice(letters))
        l.append("".join(s))
    return l
