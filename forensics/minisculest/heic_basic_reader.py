import sys

args = sys.argv[1:]


class Box:
    def __init__(self):
        self.data = b""
        self.nested = []
        self.type = None

    def parse_box(self, input_data, pos=0):
        if len(input_data) < 8:
            return None
        pos_offset = 8
        data_len = int.from_bytes(input_data[pos : pos + 4], "big")
        self.type = input_data[pos + 4 : pos + 8]
        if data_len == 1:
            data_len = int.from_bytes(input_data[pos + 8 : pos + 16], "big")
            pos_offset += 8
        elif data_len == 0:
            data_len = len(input_data) - pos
        self.data = input_data[pos + 8 : pos + data_len]
        return pos + data_len

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return f"Box(type={self.type},data={self.data[:800]})"

    def __repr__(self):
        return str(self)


def main():
    with open(args[0], "rb") as f:
        f_contents = f.read()
    pos = 0
    contents = []
    while pos < len(f_contents):
        next_box = Box()
        pos = next_box.parse_box(f_contents, pos)
        if pos is None:
            break
        contents.append(next_box)
    print("\n".join(map(str, contents)))


if __name__ == "__main__":
    main()
