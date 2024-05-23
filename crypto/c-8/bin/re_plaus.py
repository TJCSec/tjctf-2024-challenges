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


n = 18446744073709551629
a = 1871049807465198074
b = 1776200568629335123

def unenc(file, out):
    fo = open(file,"rb")
    out = open(out, "wb+")
    op = b""
    while (i := fo.read(8)):
        while (len(i) != 8):
            i += b"\x00"
        print(i)
        i = bytes_to_int(i)
        i = ((a * i) + b) % n
        i = int_to_bytes(i)
        while (len(i) != 9):
            i = b"\x00" + i
        op += i
        out.write(i)
    #print(op)

#print(bytes_to_int(b"\x01"))

#print(int_to_bytes(23334))
        
onlyfiles = [f for f in listdir("./") if isfile(join("./", f))]
[unenc(f, join("enc/", f)) for f in onlyfiles]
