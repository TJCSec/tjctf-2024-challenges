from pwn import process
import os

# clf3 is patched binary, run
p = process('./clf3')
lines = p.recvall().decode().split('\n')

# convert decimal output to binary
output = []
for line in lines[1:-1]:
    output.append(int(line.replace(',', '')))

# output to file
with open('solve', 'wb') as f:
    f.write(bytes(output))

os.system('chmod +x solve')

# run solve
p = process('./solve')
enc = p.recvall().decode()

flag = [chr(ord(c) - 4) if i < 35 else c for i, c in enumerate(enc)]

print(''.join(flag))
