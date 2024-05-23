import secrets
from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *
#BEGIN SOLVE


p0s = []
c0s = []
c1s = []

rem = remote("tjc.tf", 31234)

def encrypt(p):
    rem.recvuntil("p: ")
    rem.sendline(str(bytes_to_long(p)))
    re = rem.recvline()
    a = re.replace(b"c: ", b"")
    a = a.replace(b"\n", b"")
    a = str(a)[2:-1]
    a = int(a)
    return long_to_bytes(a)    

for i in range(512):
    p0 = secrets.token_bytes(8)
    
    #~~~~~~~~~~~~~~~~~~~Oracle query here~~~~~~~~~~~~~~~~~~~
    c0 = encrypt(p0)
    p1 = (long_to_bytes(bytes_to_long(p0) ^ (1 << 31) ^ (1 << 63)))

    c1 = encrypt(p1)
    #~~~~~~~~~~~~~~~~~~~End oracle query~~~~~~~~~~~~~~~~~~~~

    if (((bytes_to_long(c0) ^ bytes_to_long(c1)) >> 32) ^ (bytes_to_long(c0) ^ bytes_to_long(c1)) & 0xffffffff == (1 << 31) ):
        #encryptvis(p0, p1, seecrit)
        #print(encrypt(p0, seecrit, True))
        #encrypt(p0, seecrit, True)
        #encrypt(p1, seecrit, True)
        
        print(bytes_to_long(p0), bytes_to_long(p1), bytes_to_long(c0), bytes_to_long(c1))
        #if output exhibits proper differential charasterisztics,
        p0s.append(bytes_to_long(p0))
        c0s.append(bytes_to_long(c0))
        c1s.append(bytes_to_long(c1))
#paste into corresponding arrays on solve.h
header = open("solve.h","w+")
header.write("#include <vector>\n#include <cinttypes>\n")
header.write("std::vector<uint64_t> p0s = { "+ (",".join([str(i)+"ULL" for i in p0s]))[:-1]+"};\n")
header.write("std::vector<uint64_t> c0s = { "+ (",".join([str(i)+"ULL" for i in c0s]))[:-1]+"};\n")
header.write("std::vector<uint64_t> c1s = { "+ (",".join([str(i)+"ULL" for i in c1s]))[:-1]+"};\n")
header.close()

rem.interactive()
#print(c0s,"\n", c1s)
#print(p0s)
