from pwn import remote

r = remote('localhost', 5000)

r.recvuntil(b'thinking\n')
r.sendline(b'nuh uh pls nolfjdl')
r.recvuntil(b':\n')
r.sendline(b'21')

r.recvuntil(b'!\n')
print(r.recvall().decode())
