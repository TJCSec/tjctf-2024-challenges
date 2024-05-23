from PIL import Image
import sys
import struct

resolution = 512

img = Image.open(sys.argv[1])
puzzle_size = int(sys.argv[2])
output = sys.argv[3]

img = img.resize((resolution // puzzle_size * puzzle_size,
                 resolution // puzzle_size * puzzle_size))

width, height = img.size

# read all pixels into a list
blocks = [[[] for c in range(puzzle_size)] for r in range(puzzle_size)]

for r in range(height):
    for c in range(width):
        blocks[r * puzzle_size // height][c * puzzle_size //
                                          width].append(img.getpixel((c, r)))


with open(output, 'wb') as f:
    # block resolution
    f.write(struct.pack('I', width // puzzle_size))
    f.write(struct.pack('I', height // puzzle_size))

    # puzzle size
    f.write(struct.pack('I', puzzle_size))
    f.write(struct.pack('I', puzzle_size))

    last_block = blocks[-1][-1]

    # write all pixels in puzzle order
    for r, row in enumerate(blocks):
        for c, block in enumerate(row):
            if block == last_block:
                continue

            # convert into bytes
            block_bytes = b''.join([struct.pack('BBB', *pixel[:3])
                                   for pixel in block])
            for i, b in enumerate(last_block):
                last_block[i] = (b[0] ^ block[i][0], b[1] ^
                                 block[i][1], b[2] ^ block[i][2])

            # current spot
            f.write(struct.pack('I', r))
            f.write(struct.pack('I', c))

            # correct spot
            f.write(struct.pack('I', r))
            f.write(struct.pack('I', c))

            # write block
            f.write(block_bytes)

    # write last block
    f.write(struct.pack('I', puzzle_size - 1))
    f.write(struct.pack('I', puzzle_size - 1))
    f.write(struct.pack('I', puzzle_size - 1))
    f.write(struct.pack('I', puzzle_size - 1))
    f.write(b''.join([struct.pack('BBB', *pixel) for pixel in last_block]))
