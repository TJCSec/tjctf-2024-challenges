from PIL import Image
import numpy as np
import base64


img = Image.open("flag_bw.png")
width, height = img.size
img = np.array(img).astype(np.uint8).flatten()
data = []
data.extend(width.to_bytes(4, byteorder="big"))
data.extend(height.to_bytes(4, byteorder="big"))

for px in img:
    if px != 0:
        # dot flow, white color, no connections
        data.extend(b"\x00\x07\xff\xc0")
    else:
        # empty flow
        data.extend(b"\x00\x00\x00\x00")


data_bytes = bytes(data)
# print(width, height, img.shape)
# from matplotlib import pyplot as plt  # noqa: E402

# plt.imshow(img.reshape((height, width)), cmap="gray")
# plt.show()
print(base64.b64encode(data_bytes).decode())
