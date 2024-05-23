import secrets

half_S = [2, 6, 1, 13, 0, 5, 8, 7, 14, 10, 15, 11, 4, 9, 3, 12]


def s_full(i):
    left = i >> 4
    right = i & 0xf
    left = half_S[left]
    right = half_S[right]
    return right | (left << 4)

S = [s_full(i) for i in range(256)]

invS = [S.index(i) for i in range(256)]

assert all([invS[S[i]] == i for i in range(256)])

def r(i, k):
    return S[i ^ k]

def encrypt(p, k):
    for i in range(100):
        p = r(p, k[i % 2])
    return p

def dR(i, k):
    return r(r(i, k[0]), k[1])

def get_keys(i, o):
    keys = []
    for k0 in range(256):
        s0 = i ^ k0
        r1 = S[s0]
        s1 = invS[o]
        k1 = s1 ^ r1
        keys.append((k0, k1))
    return keys

def brute(oracle):
    pairs = []
    for i in range(10):
        c = secrets.randbelow(256)
        pairs.append((c, oracle(c)))

    for k0 in range(256):
        for k1 in range(256):
            k = k0.to_bytes(1, "little") + k1.to_bytes(1, "little") 
            if all([encrypt(pair[0], k) == pair[1] for pair in pairs]):
                return k

def crack(oracle):
    pairs = []
    for i in range(30):
        c = secrets.randbelow(256)
        pairs.append((c, oracle(c)))

    ctr = 0

    for pr0 in pairs:
        for pr1 in pairs:
            ctr += 1
            p0, c0 = pr0
            p1, c1 = pr1
            keys = get_keys(c0, c1)
            #check keys
            for k in keys:
                if (dR(p0, k) == p1):
                    #test key
                    if all([encrypt(pair[0], k) == pair[1] for pair in pairs]):
                        print(ctr,"pairs tried.")
                        return k

import time

itr = 1

st = time.time()
for i in range(itr):
    key = secrets.token_bytes(2)
    #print("Key:",key, [a for a in key])

    crack(lambda x: encrypt(x, key))
print("Slide:",(time.time() - st) / itr)

st = time.time()
for i in range(itr):
    key = secrets.token_bytes(2)
    #print("Key:",key, [a for a in key])

    brute(lambda x: encrypt(x, key))
print("Brute:",(time.time() - st) / itr)
