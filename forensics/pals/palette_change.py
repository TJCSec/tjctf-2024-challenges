from png_gen import write_png_chunk
from png_readchunks import read_from_file, PNG_SIGNATURE

chunks = read_from_file("pals_palette.png")

with open("pals.png", "wb") as f:
    f.write(PNG_SIGNATURE)
    for typ, dat, L in chunks:
        if typ not in [b"PLTE", b"IDAT", b"IHDR", b"IEND"]:
            continue
        # replace all colors in the palette with a single color
        if typ == b"PLTE":
            dat = b"\x28\x31\x35"*40
        write_png_chunk(f, typ, dat)
