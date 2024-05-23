import base64

lines = open("levels.txt").read().splitlines()
puzzles = []
for i, line in enumerate(lines):
    w, h, raw = line.split(" ")
    with open(f"src/puzzles/{i}_{w}x{h}", "wb") as f:
        f.write(base64.b64decode(raw.encode()))
