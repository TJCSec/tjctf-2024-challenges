from heic_basic_reader import Box
from png_gen import PNG_SIGNATURE, write_png_chunk, encode_png_ihdr, create_text_chunk
import zlib


f_contents = open("rowlet.heic", "rb").read()
pos = 0
contents = []
while pos < len(f_contents):
    next_box = Box()
    pos = next_box.parse_box(f_contents, pos)
    if pos is None:
        break
    contents.append(next_box)

print("\n".join(map(str, contents)))
print([(a.type, len(a.data)) for a in contents])
with open("minisculest.png", "wb") as f:
    f.write(PNG_SIGNATURE)
    w, h = 221, 120//3
    write_png_chunk(f, b"IHDR", encode_png_ihdr(w, h))
    write_png_chunk(f, b"tEXt", create_text_chunk(contents[0].type, contents[0].data))
    write_png_chunk(f, b"tEXt", create_text_chunk(contents[1].type, contents[1].data))
    write_png_chunk(f, b"IDAT", zlib.compress(contents[2].type + contents[2].data, level=9))
    write_png_chunk(f, b"IEND", b"")
