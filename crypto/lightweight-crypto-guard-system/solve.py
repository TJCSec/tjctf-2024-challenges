# Solve script may generate few false positives; must run multiple times to get correct answer

# Copy everything from netcat output into a file called "out.txt"

from sympy.ntheory.residue_ntheory import nthroot_mod
from lcghack import lcghack

nums = []
with open("out.txt") as rfile:
    for line in rfile:
        nums.append(line)
    flag = [int(i) for i in nums.pop().split()]
    n = int(nums.pop()[4:])  # pop the n= value
    nums = [int(i) for i in nums]


a2, c2, m = lcghack(nums)
a = nthroot_mod(a2, n, m)
print(a, m)
assert type(a) == int
assert type(m) == int


class Random():
    global m, a

    def __init__(self, x0, c):
        self.x0 = x0
        self.c = c

    def random(self):
        self.x0 = (a*self.x0+self.c) % m
        return self.x0


second = nums[1]
first = nums[0]

poss = []
for i in range(2**15):
    r = Random(first, i)
    for _ in range(0, n-1):
        r.random()
    nxt = r.random()
    if (nxt == second):
        poss.append(i)


print(poss)
c = poss[0]

lcg = Random(first, c)
flag = list(flag)
for ind in range(len(flag)):
    for __ in range(n-1):
        flag[ind] ^= lcg.random()
    lcg.random()
print("".join([chr(i) for i in flag]))
