PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'


def read_from_file(filename):
    contents = open(filename, "rb").read()
    if contents[:8] != PNG_SIGNATURE:
        raise ValueError("specified file is not a PNG")
    pos = 8
    chunks = []
    while pos < len(contents):
        chunk_len = int.from_bytes(contents[pos:pos+4], byteorder="big")
        chunk_type = contents[pos+4:pos+8]
        chunk_dat = contents[pos+8:pos+8+chunk_len]
        chunks.append((chunk_type, chunk_dat, chunk_len))
        pos += 12+chunk_len
    # print("\n".join(str([c, l]) for c, _, l in chunks))
    return chunks