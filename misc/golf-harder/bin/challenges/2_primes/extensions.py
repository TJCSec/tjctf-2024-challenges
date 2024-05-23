import random
from string import ascii_lowercase as letters


def more_matches():
    primes = open("primes.txt").read().splitlines()
    prs = map(int, random.sample(primes, 50))
    return ["".join(random.choices(letters, k=p)) for p in prs]


def more_nonmatches():
    nonprimes = [random.randint(2, 50) * random.randint(2, 50) for _ in range(50)]
    return ["".join(random.choices(letters, k=p)) for p in nonprimes]

