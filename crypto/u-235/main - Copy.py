from Crypto.Util.number import getPrime, isPrime, bytes_to_long
from Crypto.Random.random import randint
import math
N = 2048
ML = 256

flag = b"tjctf{hay_gato_encerrado28f23}"
#print(len(flag))
#https://www.esat.kuleuven.be/cosic/publications/article-54.pdf

#solve
def get_prime(bits,exclude = []):
    out = getPrime((bits+1))
    while (out in exclude):
        bits += 1
        out = getPrime((bits+1))
    return out

def next_prime(a):
    if (a % 2 == 0):
        a += 1
    while (not isPrime(a)):
        a += 2
    return a

#https://ctftime.org/writeup/32914
def getSmooth(numBits,exclude=[],smoothness = 15):
    out = 2
    outL = [2]	
    ctr = smoothness
    while len(bin(out)) - 2 < numBits:
        r = get_prime(ctr,exclude+outL)
        out *= r
        outL.append(r)
        #ctr += 1	

    bitcnt = (numBits - (len(bin(out)) - 2)) // 2
    #print("done part 1",bitcnt,outL,out)
    i = 0

    prime = 23
    
    while True:
            
        while prime in outL or prime in exclude:
            prime = next_prime(prime+1)
        #print(prime)
        if isPrime(1 + (out * prime)):
            outL.append(prime)
            out = 1+(out * prime)
            break
        prime = next_prime(prime+1)
    outL.sort()
    
    return out, outL

def getSmoothComp(s):
    out = 1
    fac = []
    while (len(bin(out)) - 2 < s):
        cand = getPrime(20)
        if (cand in fac):
            continue
        out *= cand
        fac.append(cand)
    return out, fac

m, mfac = getSmooth(ML)
q = get_prime(N - ML) * 2
p = (q * m) + 1
i = 0
while (not isPrime(p)):
    i += 1
    m, mfac = getSmooth(ML)
    q = randint(0, 2**(N-ML)) * 2 #
    p = (q * m) + 1


g = 3
x = randint(1, p - 1)
print("ElGamal...")
print("p = m * q + 1")
print("m =",m)
print("p =", p)
#print("q =", q)
print("g =",g)


y = pow(g, x, p)

print("y =", y)

def sign(M, k = p - 1):
    while math.gcd(k, p - 1) != 1:
       k = randint(1, p - 1)
    
    r = pow(g, k, p)
    s = ((M - (x * r)) * pow(k, -1, p - 1) ) % (p - 1)
    return (r, s)


def verify(r, s, M):
    if (0 < r and r < p and 0 < s and s < p - 1):
        return pow(g, M, p) == (pow(y, r, p) * pow(r, s, p)) % p
    else:
        return False

def create_covert(M, c):
    k = p - 1
    while math.gcd(k, p - 1) != 1:
        k_p = randint(1, 2**10)
        k = c + k_p * m

    #print("k =",k)
    #print("k_p =",k_p)

    r = pow(g, k, p)
    s = ((M - (x * r)) * pow(k, -1, p - 1) ) % (p - 1)
    
    return r, s

def verify_covert(r, s, M):
    if (0 < r and r < p and 0 < s and s < p - 1):
        base = pow(g, q, p)
        val = pow(r, q, p)
        assert pow(base, m, p) == 1
        print("gq =", base)
        print("rq =", val)
        return pow(g, M, p) == (pow(y, r, p) * pow(r, s, p)) % p
    else:
        return False

for i in range(0, len(flag), 2):
    M = randint(0, 100000)
    print("M"+str(i)+" =", M)
    snip = bytes_to_long(flag[i:i+2])
    r, s = create_covert(M, snip)
    print("r"+str(i)+" =", r)
    print("s"+str(i)+" =", s)
