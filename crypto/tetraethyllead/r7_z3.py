from z3 import *


def rrot(word, i):
    i %= 32
    word = word & ((1 << 32) - 1)
    return ((word >> i) | (word << (32 - i)))

def lrot(word, i):
    i %= 32
    word = word & ((1 << 32) - 1)
    return ((word << i) | (word >> (32 - i))) & ((1 << 32) - 1)

def r345(word, k, rnum):
    word ^= rrot(word, -463 + 439 * rnum + -144 * rnum**2 + 20 * rnum**3 - rnum**4) ^ lrot(word, 63 + -43 * rnum + 12 * rnum**2 + -rnum**3)

    word = (4124669716 + word * (k)) * (4124669716 + word * (k)) * (4124669716 + word * (k))

    word ^= word << 5
    word ^= word << 5

    word ^= rrot(word, -463 + 439 * rnum + -144 * rnum**2 + 20 * rnum**3 - rnum**4) ^ lrot(word, 63 + -43 * rnum + 12 * rnum**2 + -rnum**3)

    return rrot(word, -504 + 418 * rnum -499 * rnum**2 + -511 * rnum**3 + 98 * rnum**4) & 0xffffffff

def test_last_rnd(c0, c1, k):
    l0 = c0 >> 32
    l1 = c1 >> 32
    r0 = c0 & 0xffffffff
    r1 = c1 & 0xffffffff
    r1 ^= l1
    r0 ^= l0
    return r345(r0, k, 7) ^ r345(r1, k, 7) ^ l0 ^ l1

[COND]

k = BitVec('k', 33)

solve(
   [CONSTR]
)