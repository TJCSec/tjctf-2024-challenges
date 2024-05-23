import zlib

# code from https://github.com/DavidBuchanan314/hello_png
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def encode_png_uint31(value):
    if value > 2**31 - 1:
        raise ValueError("Too big!")
    return value.to_bytes(4, "big")


def write_png_chunk(stream, chunk_type, chunk_data):
    crc = zlib.crc32(chunk_type + chunk_data)

    stream.write(encode_png_uint31(len(chunk_data)))
    stream.write(chunk_type)
    stream.write(chunk_data)
    stream.write(crc.to_bytes(4, "big"))


def encode_png_ihdr(
    width,
    height,
    bit_depth=8,  # bits per sample
    colour_type=2,  # 2 = "Truecolour" (RGB)
    compression_method=1,  # 0 = zlib, all others invalid
    filter_method=0,  # 0 = "adaptive filtering" (only specified value)
    interlace_method=0,
):  # 0 = no interlacing (1 = Adam7 interlacing)
    ihdr = b""
    ihdr += encode_png_uint31(width)
    ihdr += encode_png_uint31(height)
    ihdr += bytes(
        [bit_depth, colour_type, compression_method, filter_method, interlace_method]
    )

    return ihdr


def read_rgb_subpixel(rgb_data, width, x, y, subpixel):
    return rgb_data[3 * ((width * y) + x) + subpixel]


def apply_png_filters(rgb_data, width, height):
    filtered = []
    for y in range(height):
        filtered.append(0)
        for x in range(width):
            filtered += [
                read_rgb_subpixel(rgb_data, width, x, y, 0),
                read_rgb_subpixel(rgb_data, width, x, y, 1),
                read_rgb_subpixel(rgb_data, width, x, y, 2),
            ]
    return bytes(filtered)


def write_to_file(fname, chunks):
    with open(fname, "wb") as f:
        f.write(PNG_SIGNATURE)
        for typ, dat, l in chunks:
            write_png_chunk(f, typ, dat)


if __name__ == "__main__":
    # These values are hardcoded because the .rgb "format" has no metadata
    INPUT_WIDTH = 800
    INPUT_HEIGHT = 800
    # use imagemagick to convert to .rgb: convert in.png out.rgb
    input_rgb_data = open("pyukumuku.rgb", "rb").read()

    ihdr = encode_png_ihdr(INPUT_WIDTH, INPUT_HEIGHT)

    filtered = apply_png_filters(input_rgb_data, INPUT_WIDTH, INPUT_HEIGHT)

    idat = zlib.compress(filtered, level=19)

    with open("miniscule.png", "wb") as f:
        f.write(PNG_SIGNATURE)
        write_png_chunk(f, b"IHDR", ihdr)
        write_png_chunk(f, b"IDAT", idat)
        write_png_chunk(f, b"IEND", b"")
