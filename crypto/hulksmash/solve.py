from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from itertools import permutations, product
from tqdm import tqdm

with open('keysmashes.txt', 'r') as f:
    keysmashes = f.read().splitlines()

possible_chars = list(keysmashes[0])
possible_chars = [possible_chars[:len(
    possible_chars)//2:2], possible_chars[1:len(possible_chars)//2:2]]

with open('output.txt', 'r') as f:
    output = f.read().strip()

output = bytes.fromhex(output)

for key in tqdm(product(*[permutations(poss) for poss in (possible_chars * 2)])):
    key = ''.join(''.join(a + b for a, b in zip(*key[i:i+2]))
                  for i in range(0, len(key), 2)).encode()
    cipher = AES.new(key, AES.MODE_ECB)
    flag = cipher.decrypt(output)
    if b'tjctf' in flag:
        print(key)
        print(unpad(flag, 16).decode())
        exit(0)
