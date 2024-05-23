from z3 import *


def rrot(word, i):
    i %= 32
    word = word & ((1 << 32) - 1)
    return ((word >> i) | (word << (32 - i)))

def lrot(word, i):
    i %= 32
    word = word & ((1 << 32) - 1)
    return ((word << i) | (word >> (32 - i))) & ((1 << 32) - 1)

def r345(word, k, rnum):
    word ^= rrot(word, -463 + 439 * rnum + -144 * rnum**2 + 20 * rnum**3 - rnum**4) ^ lrot(word, 63 + -43 * rnum + 12 * rnum**2 + -rnum**3)

    word = (4124669716 + word * (k)) * (4124669716 + word * (k)) * (4124669716 + word * (k))

    word ^= word << 5
    word ^= word << 5

    word ^= rrot(word, -463 + 439 * rnum + -144 * rnum**2 + 20 * rnum**3 - rnum**4) ^ lrot(word, 63 + -43 * rnum + 12 * rnum**2 + -rnum**3)

    return rrot(word, -504 + 418 * rnum -499 * rnum**2 + -511 * rnum**3 + 98 * rnum**4) & 0xffffffff

def test_last_rnd(c0, c1, k):
    l0 = c0 >> 32
    l1 = c1 >> 32
    r0 = c0 & 0xffffffff
    r1 = c1 & 0xffffffff
    r1 ^= l1
    r0 ^= l0
    return r345(r0, k, 7) ^ r345(r1, k, 7) ^ l0 ^ l1

left_0_c0 = 719717807
right_0_c0 = 85951696
right_0_c0 ^= left_0_c0 
left_0_c1 = 3396988717
right_0_c1 = 1702915666
right_0_c1 ^= left_0_c1
left_1_c0 = 3267452233
right_1_c0 = 3119934832
right_1_c0 ^= left_1_c0 
left_1_c1 = 1492253385
right_1_c1 = 2747714288
right_1_c1 ^= left_1_c1
left_2_c0 = 406984048
right_2_c0 = 1408998343
right_2_c0 ^= left_2_c0 
left_2_c1 = 196074476
right_2_c1 = 3222689115
right_2_c1 ^= left_2_c1
left_3_c0 = 2576449906
right_3_c0 = 3585241623
right_3_c0 ^= left_3_c0 
left_3_c1 = 562955477
right_3_c1 = 3987601328
right_3_c1 ^= left_3_c1
left_4_c0 = 877065771
right_4_c0 = 1609431466
right_4_c0 ^= left_4_c0 
left_4_c1 = 1118523597
right_4_c1 = 2835373900
right_4_c1 ^= left_4_c1
left_5_c0 = 2436201303
right_5_c0 = 335087514
right_5_c0 ^= left_5_c0 
left_5_c1 = 3259698196
right_5_c1 = 3230101721
right_5_c1 ^= left_5_c1
left_6_c0 = 1556032514
right_6_c0 = 2966907381
right_6_c0 ^= left_6_c0 
left_6_c1 = 245221379
right_6_c1 = 1660259828
right_6_c1 ^= left_6_c1
left_7_c0 = 2347388310
right_7_c0 = 2658324535
right_7_c0 ^= left_7_c0 
left_7_c1 = 2819322204
right_7_c1 = 1033104637
right_7_c1 ^= left_7_c1
left_8_c0 = 3646728457
right_8_c0 = 1351817274
right_8_c0 ^= left_8_c0 
left_8_c1 = 4267978425
right_8_c1 = 4155219850
right_8_c1 ^= left_8_c1
left_9_c0 = 4125285622
right_9_c0 = 4092373801
right_9_c0 ^= left_9_c0 
left_9_c1 = 2707567410
right_9_c1 = 661406957
right_9_c1 ^= left_9_c1
left_10_c0 = 50037503
right_10_c0 = 1044987892
right_10_c0 ^= left_10_c0 
left_10_c1 = 3532568006
right_10_c1 = 1849428173
right_10_c1 ^= left_10_c1
left_11_c0 = 853392800
right_11_c0 = 492189507
right_11_c0 ^= left_11_c0 
left_11_c1 = 1803103614
right_11_c1 = 3304236957
right_11_c1 ^= left_11_c1
left_12_c0 = 3296421331
right_12_c0 = 3429062134
right_12_c0 ^= left_12_c0 
left_12_c1 = 3100420279
right_12_c1 = 819239058
right_12_c1 ^= left_12_c1
left_13_c0 = 3659292846
right_13_c0 = 2671888991
right_13_c0 ^= left_13_c0 
left_13_c1 = 1553454427
right_13_c1 = 2580185002
right_13_c1 ^= left_13_c1
left_14_c0 = 1436206606
right_14_c0 = 1252312827
right_14_c0 ^= left_14_c0 
left_14_c1 = 568239073
right_14_c1 = 3202392852
right_14_c1 ^= left_14_c1
left_15_c0 = 2254650743
right_15_c0 = 106090060
right_15_c0 ^= left_15_c0 
left_15_c1 = 2537597422
right_15_c1 = 2540788437
right_15_c1 ^= left_15_c1
left_16_c0 = 953717959
right_16_c0 = 975675922
right_16_c0 ^= left_16_c0 
left_16_c1 = 4168408769
right_16_c1 = 2055989268
right_16_c1 ^= left_16_c1
left_17_c0 = 327551375
right_17_c0 = 2614560080
right_17_c0 ^= left_17_c0 
left_17_c1 = 2715215172
right_17_c1 = 2844256667
right_17_c1 ^= left_17_c1
left_18_c0 = 1039636013
right_18_c0 = 3553382860
right_18_c0 ^= left_18_c0 
left_18_c1 = 2975147034
right_18_c1 = 3748586491
right_18_c1 ^= left_18_c1


k = BitVec('k', 33)

solve(
   r345(right_0_c0, k, 7) ^ left_0_c0 ^ left_0_c1 ^ r345(right_0_c1, k, 7) == 0x80000000,
r345(right_1_c0, k, 7) ^ left_1_c0 ^ left_1_c1 ^ r345(right_1_c1, k, 7) == 0x80000000,
r345(right_2_c0, k, 7) ^ left_2_c0 ^ left_2_c1 ^ r345(right_2_c1, k, 7) == 0x80000000,
r345(right_3_c0, k, 7) ^ left_3_c0 ^ left_3_c1 ^ r345(right_3_c1, k, 7) == 0x80000000,
r345(right_4_c0, k, 7) ^ left_4_c0 ^ left_4_c1 ^ r345(right_4_c1, k, 7) == 0x80000000,
r345(right_5_c0, k, 7) ^ left_5_c0 ^ left_5_c1 ^ r345(right_5_c1, k, 7) == 0x80000000,
r345(right_6_c0, k, 7) ^ left_6_c0 ^ left_6_c1 ^ r345(right_6_c1, k, 7) == 0x80000000,
r345(right_7_c0, k, 7) ^ left_7_c0 ^ left_7_c1 ^ r345(right_7_c1, k, 7) == 0x80000000,
r345(right_8_c0, k, 7) ^ left_8_c0 ^ left_8_c1 ^ r345(right_8_c1, k, 7) == 0x80000000,
r345(right_9_c0, k, 7) ^ left_9_c0 ^ left_9_c1 ^ r345(right_9_c1, k, 7) == 0x80000000,
r345(right_10_c0, k, 7) ^ left_10_c0 ^ left_10_c1 ^ r345(right_10_c1, k, 7) == 0x80000000,
r345(right_11_c0, k, 7) ^ left_11_c0 ^ left_11_c1 ^ r345(right_11_c1, k, 7) == 0x80000000,
r345(right_12_c0, k, 7) ^ left_12_c0 ^ left_12_c1 ^ r345(right_12_c1, k, 7) == 0x80000000,
r345(right_13_c0, k, 7) ^ left_13_c0 ^ left_13_c1 ^ r345(right_13_c1, k, 7) == 0x80000000,
r345(right_14_c0, k, 7) ^ left_14_c0 ^ left_14_c1 ^ r345(right_14_c1, k, 7) == 0x80000000,
r345(right_15_c0, k, 7) ^ left_15_c0 ^ left_15_c1 ^ r345(right_15_c1, k, 7) == 0x80000000,
r345(right_16_c0, k, 7) ^ left_16_c0 ^ left_16_c1 ^ r345(right_16_c1, k, 7) == 0x80000000,
r345(right_17_c0, k, 7) ^ left_17_c0 ^ left_17_c1 ^ r345(right_17_c1, k, 7) == 0x80000000,
r345(right_18_c0, k, 7) ^ left_18_c0 ^ left_18_c1 ^ r345(right_18_c1, k, 7) == 0x80000000,

)