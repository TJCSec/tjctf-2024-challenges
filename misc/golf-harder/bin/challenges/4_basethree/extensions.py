import random
import numpy as np


def more_matches():
    start = 2**50
    end = 2**100
    return [np.base_repr(random.randrange(start, end, 2), 3) for _ in range(100)]


def more_nonmatches():
    start = 2**50
    end = 2**100
    l = [random.randrange(start+1, end+1, 2) for _ in range(200)]
    return list(map(np.base_repr, filter(lambda x: x % 2, l), [3] * len(l)))
