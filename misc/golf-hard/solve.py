import glob
from pwn import remote

r = remote('tjc.tf', 31627)

challs = glob.glob('bin/challenges/*')

challs.sort()

for chall in challs:
    with open(chall + '/master.txt', 'rb') as f:
        r.sendline(f.read().strip())

r.recvuntil(b'tjctf{')

print((b'tjctf{' + r.recvline().strip()).decode())
