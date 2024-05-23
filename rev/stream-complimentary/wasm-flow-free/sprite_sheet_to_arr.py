from PIL import Image
import numpy as np
from sys import argv
from os import makedirs


def sprite_sheet_to_arr(file_path, sprite_size, sprite_count=None):
    img = Image.open(file_path)
    img_width, img_height = img.size
    sprite_width, sprite_height = sprite_size
    sprites = []
    for y in range(0, img_height, sprite_height):
        for x in range(0, img_width, sprite_width):
            if sprite_count is not None and len(sprites) >= sprite_count:
                break
            # img.crop((x, y, x + sprite_width, y + sprite_height)).show()
            sprite = (
                np.array(
                    img.crop((x, y, x + sprite_width, y + sprite_height)),
                    dtype=np.uint8,
                )
                .flatten()
                .tolist()
            )
            sprites.append(sprite)
    return sprites


def main():
    file_path = argv[1]
    sprite_size = map(int, argv[2].split("x"))
    num_sprites = int(argv[3])
    sprites = sprite_sheet_to_arr(file_path, sprite_size, num_sprites)
    makedirs("src/sprites", exist_ok=True)
    for i, sprite in enumerate(sprites):
        if i >= num_sprites:
            break
        with open(f"src/sprites/{i}", "wb") as f:
            f.write(bytearray(sprite))


if __name__ == "__main__":
    main()
