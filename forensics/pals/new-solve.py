from PIL import Image

im = Image.open('pals.png')

NUM_COLORS = 40
palette = [(i, i, i) for i in range(0, 256, 256 // NUM_COLORS)][:NUM_COLORS]
palette = [c for rgb in palette for c in rgb]

im.putpalette(palette)

im.show()
