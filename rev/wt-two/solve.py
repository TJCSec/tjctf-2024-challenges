local = '''
    flagEnc[0] = 0x75;
    flagEnc[1] = 0x6b;
    flagEnc[2] = 0x61;
    flagEnc[3] = 0x77;
    flagEnc[4] = 99;
    flagEnc[5] = 0x73;
    flagEnc[6] = 0x7a;
    flagEnc[7] = 0x61;
    flagEnc[8] = 0xf;
    flagEnc[9] = 0x43;
    flagEnc[10] = 0x31;
    flagEnc[11] = 0xf5;
    flagEnc[12] = 0xc4;
    flagEnc[13] = 0x10d;
    flagEnc[14] = 0x215;
    flagEnc[15] = 0x3b4;
    flagEnc[16] = 0x652;
    flagEnc[17] = 0xa77;
    flagEnc[18] = 0x103a;
    flagEnc[19] = 0x1a02;
    flagEnc[20] = 0x2aa3;
    flagEnc[21] = 0x455c;
    flagEnc[22] = 0x6fc5;
    flagEnc[23] = 0xb518;
    flagEnc[24] = 0x12534;
    flagEnc[25] = 0x1da71;
    flagEnc[26] = 0x2ff26;
    flagEnc[27] = 0x4d915;
    flagEnc[28] = 0x7d8c6;
    flagEnc[29] = 0xcb255;
'''


def recur(arr):
    if arr[0] == 0 or arr[0] == 1:
        return 1
    char_enc = arr[0]
    arr[0] -= 1
    x = recur(arr)
    arr[0] = char_enc - 2
    char_enc = recur(arr)
    return x + char_enc


key = [recur([i]) for i in range(0x1e)]

local = local.strip().split('\n')

local = [int(num_str, 16) if (num_str := x.strip().split(' ')[2]
                              [:-1]).startswith('0x') else int(num_str) for x in local]

for a, b in zip(local, key):
    print(chr(a ^ b), end='')

print()
