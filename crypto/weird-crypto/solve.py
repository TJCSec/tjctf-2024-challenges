from Crypto.Util.number import isPrime

with open('bin/output.txt', 'r') as f:
    data = f.read().splitlines()
    discord_mod, hehe_secret, secret_number = map(lambda x: int(x.split(' = ')[1]), data)

tot = 0
for i in range(1<<32):
    if not isPrime(i):
        continue
    cur = pow(hehe_secret, i, discord_mod)
    cur = cur.to_bytes(128, byteorder='big')
    tot+=1
    if(tot%20000==0):
        print(i)
        print("HI")
    if b"tjctf" in cur:
        print(cur.decode())
        exit(0)
