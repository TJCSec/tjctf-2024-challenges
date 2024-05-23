
des = bytes.fromhex("1f23a7bf14a55de3")
old = bytes.fromhex("1f23a7bf14a546e3")
t = open("binfinal","rb").read()
a = t.replace(old, des)
print(t==a)
open("binfinal_final","wb+").write(a)
