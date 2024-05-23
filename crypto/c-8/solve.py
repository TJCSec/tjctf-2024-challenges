from os import listdir
from os.path import isfile, join

def bytes_to_int(b):
    h = b.hex()
    return int(h, 16)

def int_to_bytes(i):
    h = hex(i)[2:]
    if (len(h) % 2):
        h = "0"+h
    return bytes.fromhex(h)

path = "bin/enc"

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

pt = open(join(path, "re_plaus.py"),"rb").read() #b"".join([open(join(path, f),"rb").read() for f in onlyfiles])

#print(pt)
words = [bytes_to_int(pt[i:i+9]) for i in range(0, len(pt), 9)]

n = 18446744073709551629 #we must get 8 bytes of data, and its the next prime after 2**64

def decrypt(words, a, b):
    inv_a = pow(a, -1, n)
    out = b""
    for i in words:
        nu = (((i - b) % n) * inv_a) % n
        nu = int_to_bytes(nu)
        while (len(nu) != 8):
            nu = b"\x00" + nu
        out += nu
    return out

def pot_decrypt(words, a, b):
    inv_a = pow(a, -1, n)
    out = decrypt(words, a, b)
    return out.count(b" ") > 50 and out.count(b"open(") != 0

def score(part):
    acc = b"abcdefghijklmnopqrstuvwxyzQPWOE%!_IRUTYLAKSJDFHMNXCB,ZVG./*+-() \'\"\n\r[]#:=0198234756\\"
    score = 0
    for i in range(256):
        b = int_to_bytes(i)
        if b in acc:
            continue
        score += part.count(b)
    return score

def expand_cribs(pres):
    cribs = []
    for option in pres:
        for i in range(len(option)-7):
            cribs.append(option[i:i+8])
    return cribs

print(max(words))
print(len(words))
words = list(set(words))
print(len(words))

a = 1871049807465198074
b = 1776200568629335123
print(decrypt(words, a, b), score(decrypt(words, a, b)))

#print(pot_decrypt(words, a, b))

#pre_cribs = [b"for i in ", b" = open(", b", \"rb\")\n", b"        for", b"        while"]
pre_cribs = [b"    return ", b"        ", b"        while"]
#pre_cribs = [b"from os ", b"import l"]

cribs = expand_cribs(pre_cribs)

cribs = [bytes_to_int(c) for c in cribs]

print(cribs)
print(len(cribs))
ctr = 0
keys = []

foundkey = (1871049807465198074, 1776200568629335123)

for word1 in words:
    if foundkey:
        continue
    for word2 in words:
        if word1 == word2:
            continue
        for crib1 in cribs:
            for crib2 in cribs:
                if crib1 == crib2: #uninvertible
                    continue
                a_p_c1mc2_p = (word1 - word2) % n
                c1mc2 = (crib1 - crib2) % n
                inv_c1mc2 = pow(c1mc2, -1, n)
                a_test = (inv_c1mc2 * a_p_c1mc2_p) % n
                b_test = (word1 - (crib1 * a_test)) % n
                if (pot_decrypt(words, a_test, b_test)):
                    print("\nSolved potentially:", a_test, b_test,"\n")
                    keys.append((a_test, b_test))
                ctr += 1
                if (ctr % 10000 == 0):
                    print("\r",ctr / (111*111.*len(cribs)*len(cribs)),end="")
stack = []
keys = list(set(keys))
for key in keys:
    stack.append((score(decrypt(words, key[0], key[1])),key[0], key[1]))
a = sorted(stack, key = lambda x: x[0])
print(a)
for key in a:
    print(decrypt(words, key[1],key[2]))


onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

for f in onlyfiles:
    pt = open(join(path, f),"rb").read() #b"".join([open(join(path, f),"rb").read() for f in onlyfiles])

    #print(pt)
    words = [bytes_to_int(pt[i:i+9]) for i in range(0, len(pt), 9)]
    b = decrypt(words, foundkey[0], foundkey[1])
    open(join("solve",f),"wb+").write(b)
