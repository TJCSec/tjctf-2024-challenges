from PIL import Image
import random

random.seed(42)

lmao = random.randint(12345678,123456789)

random.seed(lmao)

img = Image.open("skibidi_encoded.png")

troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
inds = [i for i in range(288)]
troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
randnum = random.randint(1,500)

troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))

for i in range(random.randint(0,500), random.randint(500,1000)):
    random.seed(i)
    random.shuffle(inds)
    if i==randnum:
        break
troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
troll = [random.randint(random.randint(-lmao,0),random.randint(0,lmao)) for _ in range(random.randint(1,5000))]
troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))

width, height = img.size

pic_inds = []
while len(pic_inds)!=288:
    troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    pic_inds.append(random.randint(0,width*height))
    troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))

changes = []
for p in range(288):
    trollll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    trollll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    trollll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    trollll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    trollll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    changes.append(random.randint(0,2))
    trollll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    trollll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    trollll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    if(p%randnum==0):
        random.seed(random.randint(random.randint(-lmao,0),random.randint(0,lmao)))
st = ""
for i in range(288):
    cur_ind = pic_inds[i]
    row = cur_ind//height
    col = cur_ind%width
    colors = list(img.getpixel((row,col)))
    st+=bin(colors[changes[i]])[-1]

newst = [[] for _ in range(288)]
for i in range(len(inds)):
    newst[inds[i]] = st[i]

print(bytes(bytearray([int("".join(newst[i:i+8]),2) for i in range(0,len(newst),8)])).decode("utf-8"))
