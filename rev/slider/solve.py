from PIL import Image
from struct import unpack, iter_unpack

with open('src/app/save.dat', 'rb') as f:
    data = f.read()

block_width, block_height = unpack('II', data[:8])
puzzle_width, puzzle_height = unpack('II', data[8:16])

correct = [[[] for c in range(puzzle_width)] for r in range(puzzle_height)]

for block in iter_unpack('IIII' + 'B' * (block_width * block_height * 3), data[16:]):
    r, c = block[:2]
    correct_r, correct_c = block[2:4]
    correct[correct_r][correct_c] = list(block[4:])

for r in correct:
    for c in r:
        if c == correct[-1][-1]:
            continue
        correct[-1][-1] = [a ^ b for a, b in zip(c, correct[-1][-1])]

img = Image.new('RGB', (block_width * puzzle_width,
                block_height * puzzle_height))

for r in range(puzzle_height):
    for c in range(puzzle_width):
        img.paste(Image.frombytes('RGB', (block_width, block_height),
                                  bytes(correct[r][c])), (c * block_width,
                                                          r * block_height))

img.show()
