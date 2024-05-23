# Code is adapted from https://github.com/TomasGlgg/LCGHack/blob/master/main.py


from functools import reduce
from math import gcd


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x


def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0] * multiplier) % modulus
    return increment


def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * \
        modinv(states[1] - states[0], modulus) % modulus
    return multiplier


def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2 * t0 - t1 * t1 for t0, t1,
              t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return modulus


def lcghack(knowns):
    modulus = crack_unknown_modulus(knowns)
    multiplier = crack_unknown_multiplier(knowns, modulus)
    increment = crack_unknown_increment(knowns, modulus, multiplier)
    return (multiplier, increment, modulus)
