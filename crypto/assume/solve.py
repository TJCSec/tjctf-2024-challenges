n=35
target_str = ""
with open("log.txt") as log:
    p = int(log.readline())
    for pos in range(35):
        charsSeen = set()
        badChars = set()
        possible = set()
        for iter in range(20):
            ga = int(log.readline().split(" ")[-1])
            b = int(log.readline().split(" ")[-1])
            gb = int(log.readline().split(" ")[-1])
            msg = log.readline().split(" ")[-1]
            gab = int(log.readline().split(" ")[-1])

            log.readline()

            charsSeen.add(msg)
            
            pa = 0 if pow(ga, ((p - 1) // 2), p) == 1 else 1 # 0 if ga is a QR. else 1
            pb = 0 if pow(gb, ((p - 1) // 2), p) == 1 else 1 # 0 if gb is a QR. else 1   
            pab = 0 if pow(gab, ((p - 1) // 2), p) == 1 else 1 # 0 if gab is a QR. else 1

            if pa * pb != pab:
                possible.discard(msg)
                badChars.add(msg)
            else:
                if msg not in badChars:
                    possible.add(msg)
        if not possible:
            target_str += list(charsSeen)[0]
        else:
            target_str += list(possible)[0]

print(target_str.replace("\n",""))
while True:
	pass
 