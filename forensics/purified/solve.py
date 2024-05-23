from PIL import Image,UnidentifiedImageError
from io import BytesIO

start = Image.open("out.qoi")
data = start.tobytes()
while True:
    try:
        img = Image.open(BytesIO(data))
        data = img.tobytes()
    except UnidentifiedImageError:
        break

img.show()
