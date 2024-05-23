from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key = b'rW>=\x00\xd4\xdf\xd8\xe2wX\xb5\xf7\x0cc\xb9'
iv = b'l\x86,\xa1\n\xbfd\xee4\xfa\xcd\xce\x9bf\xddb'
dat = open("plausibly.deniable", "rb").read()
cipher = AES.new(key, AES.MODE_CBC, iv)
ct = cipher.decrypt((dat))
open("story.txt","wb+").write(unpad(ct, 16))

