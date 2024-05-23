import base64

# I took this from levels.txt, but the same thing can be accomplished by patching in
# a "print this board" feature to the html/js in index.html
old_board = base64.b64decode(
    b"AAAAAwAAAAMAB9VAAAVXwAAAjsAAAAAAAAAAAAAAAAAAAI7AAAVXwAAH1UA="
)

# created using generator.html, needs to not have anything in the leading 3 0x00 bytes,
# or in the 14 central 0x00 bytes
new_board = base64.b64decode(
    b"AAAAAwAAAAMAADfAAAR3wAAHycAAAAAAAAAAAAAAAAAAADfAAAR3wAAHycA="
)
print(" ".join(str(i).rjust(2) for i in range(len(old_board))))
print(" ".join(hex(i)[2:].zfill(2) for i in old_board))
print(" ".join(hex(i)[2:].zfill(2) for i in new_board))

contents = bytearray(open("site/pkg/wasm_flow_free_bg.wasm", "rb").read())

old_start, old_end = old_board[3 : 19 + 1], old_board[34:]
start_slice, end_slice = new_board[3 : 19 + 1], new_board[34:]

assert contents.count(old_start) == 1 and contents.count(old_end) == 1
contents[contents.index(old_start) : contents.index(old_start) + len(old_start)] = (
    start_slice
)
contents[contents.index(old_end) : contents.index(old_end) + len(old_end)] = end_slice

with open("site/pkg/wasm_flow_free_bg.wasm", "wb") as f:
    f.write(contents)
print("successfully wrote new puzzle")
# now play through the levels and get to the last one!
# you will likely need to resize the screen to see the flag on the last one
