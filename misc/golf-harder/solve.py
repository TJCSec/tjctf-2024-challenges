import glob
from pwn import remote

r = remote('localhost', 5000)
# r = remote('tjc.tf', 31627)

challs = glob.glob('bin/challenges/*')

challs.sort()

for chall in challs:
    with open(chall + '/master.txt', 'rb') as f:
        r.sendline(f.readline().strip())

r.recvuntil(b'tjctf{')

print((b'tjctf{' + r.recvline().strip()).decode())
