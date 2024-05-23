from z3 import *


#left shifts for each stage of the shift function
sh_f = Int('sh_f') #r3
sh_s = Int('sh_s') #r4
sh_th = Int('sh_th') #r5
sh_fo = Int('sh_fo') #r6
sh_fi = Int('sh_fi') #r7

#right shifts for rounds 5 and 7 are arbitrary
sh_arb_fifth = Int('sh_arb_fifth')

sh_arb_third = Int('sh_arb_third')

#left shift polynomial coefficients
a = Int('a')
b = Int('b')
c = Int('c')
d = Int('d')
e = Int('e')

#right shift polynomial coefficients
ar = Int('ar')
br = Int('br')
cr = Int('cr')
dr = Int('dr')
er = Int('er')

#variables for rshift at the end of the r345 fxn
m1 = Int('m1')
m2 = Int('m2')
m3 = Int('m3')
dmy_r5_sh = Int('dmy_r5_sh')
dmy_r7_sh = Int('dmy_r7_sh')

max_sh = 32

min_coeff = -512
max_coeff = 512

#solve for r_shift and l_shift polynomial in r345
solve(sh_f > 14, sh_f < max_sh,
      sh_s > 3, sh_s < max_sh,
      sh_th > 3, sh_th < max_sh,
      sh_fo > 3, sh_fo < max_sh,
      sh_fi > 11, sh_fi < max_sh,
      a + b * 3 + c * 9 + d * 27 + e * 81 == sh_f,
      a + b * 4 + c * (4**2) + d * (4**3) + e * (4**4) == sh_s,
      a + b * 5 + c * (5**2) + d * (5**3) + e * (5**4) == sh_th,
      a + b * 6 + c * (6**2) + d * (6**3) + e * (6**4) == sh_fo,
      a + b * 7 + c * (7**2) + d * (7**3) + e * (7**4) == sh_fi,
      a < max_coeff, a > min_coeff,
      b < max_coeff, b > min_coeff,
      c < max_coeff, c > min_coeff,
      d < max_coeff, d > min_coeff,
      e < max_coeff, e > min_coeff,
      a != sh_f,
      sh_arb_third > 1, sh_arb_third < 32,
      sh_arb_fifth > 1, sh_arb_fifth < 32,
      sh_arb_fifth != 32 - sh_fi,
      sh_arb_third != 32 - sh_th,
      ar + br * 3 + cr * 9 + dr * 27 + er * 81 == 32 - sh_f,
      ar + br * 4 + cr * (4**2) + dr * (4**3) + er * (4**4) == 32 - sh_s,
      ar + br * 5 + cr * (5**2) + dr * (5**3) + er * (5**4) == sh_arb_third,
      ar + br * 6 + cr * (6**2) + dr * (6**3) + er * (6**4) == 32 - sh_fo,
      ar + br * 7 + cr * (7**2) + dr * (7**3) + er * (7**4) == sh_arb_fifth,
      ar < max_coeff, ar > min_coeff,
      br < max_coeff, br > min_coeff,
      cr < max_coeff, cr > min_coeff,
      dr < max_coeff, dr > min_coeff,
      er < max_coeff, er > min_coeff,
      ar != sh_f
      )

#solve for rshift polynomial at end of r345
#technically we're not garunteeing that the dummy shifts aren't multiples of 32 but
#however its v. unlikely to occur due to chance and the values I have work fine
solve(sh_f > 14, sh_f < max_sh,
      sh_s > 3, sh_s < max_sh,
      sh_th > 3, sh_th < max_sh,
      sh_fo > 3, sh_fo < max_sh,
      sh_fi > 11, sh_fi < max_sh,
      a + b * 3 + c * 9 + d * 27 + e * 81 == m1 * 32,
      a + b * 4 + c * (4**2) + d * (4**3) + e * (4**4) == m2 * 32,
      a + b * 5 + c * (5**2) + d * (5**3) + e * (5**4) == dmy_r5_sh,
      a + b * 6 + c * (6**2) + d * (6**3) + e * (6**4) == 32 * m3,
      a + b * 7 + c * (7**2) + d * (7**3) + e * (7**4) == dmy_r7_sh,
      a < max_coeff, a > min_coeff,
      b < max_coeff, b > min_coeff,
      c < max_coeff, c > min_coeff,
      d < max_coeff, d > min_coeff,
      e < max_coeff, e > min_coeff,
      a !=0, b != 0
      )

"""
[cr = 12,
 dr = -1,
 b = 439,
 d = 20,
 er = 0,
 sh_s = 13,
 c = -144,
 e = -1,
 br = -43,
 a = -463,
 sh_arb_third = 23,
 sh_fo = 11,
 ar = 63,
 sh_f = 17,
 sh_th = 7,
 sh_arb_fifth = 7,
 sh_fi = 13]
[c = -499,
 sh_fi = 12,
 e = 98,
 sh_th = 4,
 sh_f = 15,
 m3 = 21,
 d = -511,
 sh_fo = 4,
 m2 = -451,
 sh_s = 4,
 m1 = -300,
 b = 418,
 a = -504,
 dmy_r7_sh = 37996,
 dmy_r5_sh = -13514]
 """
