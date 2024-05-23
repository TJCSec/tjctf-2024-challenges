from random import randrange
from png_gen import write_png_chunk, PNG_SIGNATURE
from png_readchunks import read_from_file

chunks = read_from_file("pals.png")
with open("pals_solve.png", "wb") as f:
    f.write(PNG_SIGNATURE)
    for typ, dat, L in chunks:
        if typ == b"PLTE":
            dat = bytes([randrange(256) for _ in range(len(dat))])
        write_png_chunk(f, typ, dat)
