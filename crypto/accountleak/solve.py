from pwn import *
from math import isqrt
from Crypto.Util.number import inverse

def solve(C, N, L):
    poss = []
    mlim = 2**20
    for x in range(1, mlim):
        a = x
        b = L-N-x**2
        c = x*N
        d = b**2-4*a*c
        # print(d)
        if (d < 0):
            continue
        qform = (-b + isqrt(d))//(2*a)
        p = N//qform
        if ((p-x)*(qform-x) == L):
            poss.append((qform))
            break
    return poss[0], N//poss[0]

IP = "tjc.tf"
PORT = 31601

conn = remote(IP, PORT)
conn.recvline()
cnline = conn.recvline().decode('utf-8').split(" ")
c = int(cnline[7])
n = int(cnline[9])
conn.recvline()
conn.recvline()

# now things get interesting
conn.sendline(b'yea')
conn.recvline()
l = int(conn.recvline().decode('utf-8').replace('<Bobby> ', ''))
conn.recvline()
conn.recvline()

p, q = solve(c, n, l)
phi = (p-1)*(q-1)
d = inverse(65537, phi)
m = pow(c, d, n)
conn.sendline(str(m).encode('utf-8'))
msg = conn.recvline().decode('utf-8').strip()
assert "<Bobby> NANI?? Impossible?!?" in msg
conn.recvline()
flag = conn.recvline()
print(flag.decode('utf-8').replace('<Bobby> ', ''))
