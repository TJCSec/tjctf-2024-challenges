import base64
import zlib

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_from_file(filename):
    contents = open(filename, "rb").read()
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
    return chunks


def encode_heif_chunk(chunk_type, data, *, last=False):
    assert len(chunk_type) == 4
    length = len(data) + 8
    if last:
        return (0).to_bytes(4, "big") + chunk_type + data
    elif length >= (1 << 32):
        return (
            (1).to_bytes(4, "big") + chunk_type + (length + 8).to_bytes(8, "big") + data
        )
    else:
        return length.to_bytes(4, "big") + chunk_type + data


chunks = read_from_file("minisculest.png")
print([(a, c) for a, b, c in chunks])
_, ftyp, meta, mdat, _ = [b for a, b, c in chunks]

ftyp_name, ftyp_data = ftyp.split(b"\x00")
ftyp_data = base64.b64decode(ftyp_data)
print(len(ftyp_data))
meta_name, meta_data = meta.split(b"\x00")
meta_data = base64.b64decode(meta_data)
print(len(meta_data))
mdat = zlib.decompress(mdat)
mdat_name, mdat_data = mdat[:4], mdat[4:]
print(ftyp_name, meta_name, mdat_name)
with open("solved.heic", "wb") as f:
    f.write(encode_heif_chunk(ftyp_name, ftyp_data))
    f.write(encode_heif_chunk(meta_name, meta_data))
    f.write(encode_heif_chunk(mdat_name, mdat_data))
