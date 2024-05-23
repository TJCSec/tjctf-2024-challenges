#!/usr/local/bin/python3.8
from PIL import Image
import io
import random
from zlib import crc32, compress

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
im = Image.open("jigsaw.png")
dat = list(im.getdata())
blocks = [dat[i : i + 15] for i in range(0, len(dat), 15)]
r = random.Random()
r.seed(len(open(__file__).read()))
r.shuffle(blocks)
rejoined = []
for block in blocks:
    rejoined += block
im2 = Image.new(im.mode, im.size)
im2.putdata(rejoined)
buffer = io.BytesIO()
im2.save(buffer, format="PNG")
buffer.seek(0)
contents = buffer.read()
if contents[:8] != PNG_SIGNATURE:
    raise ValueError("specified file is not a PNG")
pos = 8
chunks = []
while pos < len(contents):
    chunk_len = int.from_bytes(contents[pos : pos + 4], byteorder="big")
    chunk_type = contents[pos + 4 : pos + 8]
    chunk_dat = contents[pos + 8 : pos + 8 + chunk_len]
    chunks.append((chunk_type, chunk_dat, chunk_len))
    pos += 12 + chunk_len
chunks.insert(
    1,
    (b"zTXt", b"generator code\x00\x00" + compress(open(__file__, "rb").read()), None),
)
with open("shuffled.png", "wb") as f:
    f.write(PNG_SIGNATURE)
    for typ, dat, l in chunks:
        f.write(len(dat).to_bytes(4, "big"))
        f.write(typ)
        f.write(dat)
        f.write(crc32(typ + dat).to_bytes(4, "big"))
