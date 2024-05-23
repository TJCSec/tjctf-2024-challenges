from PIL import Image
from io import BytesIO


def factorize(n):
    return [(a, n // a) for a in range(1, int(n**0.5) + 1) if (a * (n // a)) == n]


data = open("pure.png", "rb").read()
# size = factorize(len(data))[-1]
FORMATS = ("bmp", "tiff", "webp", "tga", "sgi", "png", "png") # add one extra to allow QOI encoding

for fmt in FORMATS:
    mode, size = (
        ("RGB", factorize(len(data) // 3)[-1])
        if len(data) % 3 == 0
        else ("L", factorize(len(data))[-1])
    )
    print(fmt)
    new = Image.frombytes(mode, size, data)
    data = BytesIO()
    new.save(data, format=fmt, lossless=True)
    data = data.getvalue()

with open("out.png", "wb") as f:
    f.write(data)
# new.show()
