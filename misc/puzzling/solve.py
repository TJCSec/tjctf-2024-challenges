import random
from PIL import Image
import matplotlib.pyplot as plt

im = Image.open('shuffled.png')

# print generator code
code = im.info['generator code']
print(code)

r = random.Random()
r.seed(len(code))
dat = list(im.getdata())
blocks = [dat[i:i+15] for i in range(0, len(dat), 15)]

shuffle_list = list(range(len(blocks)))
r.shuffle(shuffle_list)

unshuffle_map = {v: i for i, v in enumerate(shuffle_list)}

# get pos of last original block
last_block_pos = unshuffle_map[len(blocks)-1]

fig, axs = plt.subplots(3, 5)

# find correct shift
for shift in range(15):
    new_blocks = []
    for i in range(len(blocks)):
        if i > last_block_pos:
            new_blocks.append(blocks[i-1][shift:] + blocks[i][:shift])
        elif i == last_block_pos:
            new_blocks.append(blocks[i][:shift])
        else:
            new_blocks.append(blocks[i])

    rejoined = [None for _ in new_blocks]
    for i, j in enumerate(shuffle_list):
        rejoined[j] = new_blocks[i]
    rejoined = [p for q in rejoined for p in q]
    rejoined = rejoined[:len(dat)]

    im2 = Image.new(im.mode, im.size)
    im2.putdata(rejoined)

    axs[shift//5, shift%5].imshow(im2)
    axs[shift//5, shift%5].axis('off')

plt.show()
