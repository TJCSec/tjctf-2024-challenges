from zlib import crc32

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def parse_ihdr(dat):
    print(dat)
    width = int.from_bytes(dat[0:4], byteorder="big")
    height = int.from_bytes(dat[4:8], byteorder="big")
    depth = int.from_bytes(dat[8:9], byteorder="big")
    color = int.from_bytes(dat[9:10], byteorder="big")
    compression = int.from_bytes(dat[10:11], byteorder="big")
    filter_method = int.from_bytes(dat[11:12], byteorder="big")
    interlace_method = int.from_bytes(dat[12:13], byteorder="big")
    return {
        "width": width,
        "height": height,
        "depth": depth,
        "color": color,
        "compression": compression,
        "filter": filter_method,
        "interlace": interlace_method,
    }


def read_from_bytes(contents):
    if contents[:8] != PNG_SIGNATURE:
        raise ValueError("specified file is not a PNG")
    pos = 8
    chunks = []
    while pos < len(contents):
        chunk_len = int.from_bytes(contents[pos : pos + 4], byteorder="big")
        chunk_type = contents[pos + 4 : pos + 8]
        chunk_dat = contents[pos + 8 : pos + 8 + chunk_len]
        chunk_crc = contents[pos + 8 + chunk_len : pos + chunk_len + 12]
        expected_crc = crc32(contents[pos + 4 : pos + 8 + chunk_len]).to_bytes(
            length=4, byteorder="big"
        )
        if chunk_crc != expected_crc:
            raise ValueError(
                f"crc failure (claims {chunk_crc}, should be {expected_crc})"
            )
        chunks.append((chunk_type, chunk_dat, chunk_len))
        pos += 12 + chunk_len
    return chunks


def read_from_file(filename):
    return read_from_bytes(open(filename, "rb").read())
