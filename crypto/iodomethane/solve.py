alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0192834756{}_!@#$%^&*()"

modulus = 15106021798142166691 #len(alphabet)

enc = [2448432677444740984, 14117192105416470319, 13317229864883053270, 13612023470676517406, 7910523483550047, 9585523703681139772, 10324380377275142076, 896612131946398589, 9362937639349358467, 3474375577388052216, 8327795459807893630, 8590964910570097290, 9614669351132051958, 4420061041041268249, 1260167073148758881, 3177768497911592836, 6803514216696381667, 277887952004838774, 5719842921591812037, 1732716210875923983, 8759230581610806889, 5205256044155043240, 2010537612670256588, 1486315929768842167, 10153710354642909513, 8051597643547882193, 927074323604216973, 13865294929674898585, 7714220271820940011, 10889939340581868344, 5977620349490572274, 6751875053019798196, 2066468701734404566, 8210891405020288986, 3516463044553947090, 4869839183134870451, 10880003320623496834, 771623159293317370, 14555454906681135750, 8143021020931017262, 12305443698638520581, 6528891777437625217]

def dot(a,b):
    return sum([a[i] * b[i] for i in range(len(a))]) % modulus

def mult(key, row):
    return [dot(key[i], row) for i in range(len(key))]

def transposeMatrix(m):
    return list(map(list,zip(*m)))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    divdet = pow(determinant, -1, modulus)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[(m[1][1] * divdet) % modulus, (-1*m[0][1] * divdet) % modulus],
                [(-1*m[1][0] * divdet) % modulus, (m[0][0] * divdet) % modulus]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append((((-1)**(r+c)) * getMatrixDeternminant(minor)) % modulus)
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = (cofactors[r][c] * divdet) % modulus
    return cofactors

def dec(key):
    inv = getMatrixInverse(key)
    rows = list(zip(enc[::3], enc[1::3], enc[2::3]))
    dec = sum([mult(inv, snip) for snip in rows], start = [])
    out = ""
    for i in range(len(dec)):
        if dec[i] >= len(alphabet):
            break
        out += alphabet[dec[i]]

    if (len(dec) - i) >= 3:
        raise Exception
    
        
    return out

def decI(inv):
    rows = list(zip(enc[::3], enc[1::3], enc[2::3]))
    dec = sum([mult(inv, snip) for snip in rows], start = [])
    out = ""
    
    for i in range(len(dec)):
        if dec[i] >= len(alphabet):
            break
        out += alphabet[dec[i]]

    if (len(dec) - i) >= 3:
        raise Exception
    
    return out

#knownk = [[36, 45, 201], [191, 82, 168], [56, 48, 256]]
#invk = getMatrixInverse(knownk)
#print(decI(invk))
# tjctf{
# a * enc[0] + b * enc[1] + c * enc[2] == 't' mod modulus
# a * enc[3] + b * enc[4] + c * enc[5] == 't' mod modulus
# C = pow(enc[0], -1, modulus) * enc[3] 
# a * C * enc[0] + b * C * enc[1] + c * C * enc[2] == C * 't' mod modulus
# a * enc[3] + b * enc[4] + c * enc[5] == 't' mod modulus
# b * (C * enc[1] - enc[4]) + c * (C * enc[2] - enc[5]) == (C - 1) * 't' mod modulus


# a * enc[0] + b * enc[1] + c * enc[2] == 't' mod modulus
# a * enc[3] + b * enc[4] + c * enc[5] == 't' mod modulus
# G = pow(enc[1], -1, modulus) * enc[4]
# a * G * enc[0] + b * G * enc[1] + c * G * enc[2] == G * 't' mod modulus
# a * (G * enc[0] - enc[3]) + c * (G * enc[2] - enc[5]) == (G - 1) * 't' mod modulus

# g * enc[-3] + h * enc[-2] + i * enc[-1] == alphabet.index('}') mod modulus

def calc(enc, known_p1, known_p2, known_p3, modulus):
    try:
        # a * enc[0] + b * enc[1] + c * enc[2] == known_p1 mod modulus
        # a * enc[3] + b * enc[4] + c * enc[5] == known_p2 mod modulus
        # a * enc[6] + b * enc[7] + c * enc[8] == known_p3 mod modulus
        # c == (known_p1 - (a * enc[0] + b * enc[1])) * pow(enc[2], -1, modulus) mod modulus
        
        # a * enc[3] + b * enc[4] + (known_p1 - (a * enc[0] + b * enc[1])) * pow(enc[2], -1, modulus) * enc[5] == known_p2 mod modulus
        # a * enc[6] + b * enc[7] + (known_p1 - (a * enc[0] + b * enc[1])) * pow(enc[2], -1, modulus) * enc[8] == known_p3 mod modulus

        # a * enc[3] * enc[6] + b * enc[4] * enc[6] + (known_p1 - (a * enc[0] + b * enc[1])) * pow(enc[2], -1, modulus) * enc[5] * enc[6] == known_p2 * enc[6] mod modulus
        # a * enc[6] * enc[3] + b * enc[7] * enc[3] + (known_p1 - (a * enc[0] + b * enc[1])) * pow(enc[2], -1, modulus) * enc[8] * enc[3] == known_p3 * enc[3] mod modulus

        # a * enc[3] * enc[6] + b * enc[4] * enc[6] + known_p1 * pow(enc[2], -1, modulus) * enc[5] * enc[6] - a * enc[0] * pow(enc[2], -1, modulus) * enc[5] * enc[6] - b * enc[1] * pow(enc[2], -1, modulus) * enc[5] * enc[6] == known_p2 * enc[6] mod modulus
        # a * enc[6] * enc[3] + b * enc[7] * enc[3] + known_p1 * pow(enc[2], -1, modulus) * enc[8] * enc[3] - a * enc[0] * pow(enc[2], -1, modulus) * enc[8] * enc[3] - b * enc[1] * pow(enc[2], -1, modulus) * enc[8] * enc[3] == known_p3 * enc[3] mod modulus

        # a * (enc[3] * enc[6] - enc[0] * pow(enc[2], -1, modulus) * enc[5] * enc[6]) + b * (enc[4] * enc[6] - enc[1] * pow(enc[2], -1, modulus) * enc[5] * enc[6]) + known_p1 * pow(enc[2], -1, modulus) * enc[5] * enc[6] == known_p2 * enc[6] mod modulus
        # a * (enc[6] * enc[3] - enc[0] * pow(enc[2], -1, modulus) * enc[8] * enc[3]) + b * (enc[7] * enc[3] - enc[1] * pow(enc[2], -1, modulus) * enc[8] * enc[3]) + known_p1 * pow(enc[2], -1, modulus) * enc[8] * enc[3] == known_p3 * enc[3] mod modulus

        # a * (enc[3] * enc[6] - enc[0] * pow(enc[2], -1, modulus) * enc[5] * enc[6]) + b * (enc[4] * enc[6] - enc[1] * pow(enc[2], -1, modulus) * enc[5] * enc[6]) + known_p1 * pow(enc[2], -1, modulus) * enc[5] * enc[6] == known_p2 * enc[6] mod modulus
        # a * (enc[6] * enc[3] - enc[0] * pow(enc[2], -1, modulus) * enc[8] * enc[3]) + b * (enc[7] * enc[3] - enc[1] * pow(enc[2], -1, modulus) * enc[8] * enc[3]) + known_p1 * pow(enc[2], -1, modulus) * enc[8] * enc[3] == known_p3 * enc[3] mod modulus

        a_mult1 = ((enc[3] * enc[6] - enc[0] * pow(enc[2], -1, modulus) * enc[5] * enc[6])) % modulus
        a_mult2 = ((enc[6] * enc[3] - enc[0] * pow(enc[2], -1, modulus) * enc[8] * enc[3])) % modulus
        b_mult1 = ((enc[4] * enc[6] - enc[1] * pow(enc[2], -1, modulus) * enc[5] * enc[6])) % modulus
        b_mult2 = ((enc[7] * enc[3] - enc[1] * pow(enc[2], -1, modulus) * enc[8] * enc[3])) % modulus
        eq1 = (known_p2 * enc[6] - (known_p1 * pow(enc[2], -1, modulus) * enc[5] * enc[6])) % modulus
        eq2 = (known_p3 * enc[3] - (known_p1 * pow(enc[2], -1, modulus) * enc[8] * enc[3])) % modulus


        # a * a_mult1 + b * b_mult1 == eq1 mod modulus
        # a * a_mult2 + b * b_mult2 == eq2 mod modulus

        # a * a_mult1 * a_mult2 + b * b_mult1 * a_mult2 == eq1 * a_mult2 mod modulus
        # a * a_mult2 * a_mult1 + b * b_mult2 * a_mult1 == eq2 * a_mult1 mod modulus

        #b * (b_mult1 * a_mult2 - b_mult2 * a_mult1) == eq1 * a_mult2 - eq2 * a_mult1 mod modulus

        b = (pow((b_mult1 * a_mult2 - b_mult2 * a_mult1), -1, modulus) * (eq1 * a_mult2 - eq2 * a_mult1)) % modulus

        # a * enc[0] * enc[3] + c * enc[2] * enc[3] == (known_p1 - b * enc[1]) * enc[3] mod modulus
        # a * enc[3] * enc[0] + c * enc[5] * enc[0] == (known_p2 - b * enc[4]) * enc[0] mod modulus

        # c * (enc[2] * enc[3] - enc[5] * enc[0]) == ((known_p1 - b * enc[1]) * enc[3] - (known_p2 - b * enc[4]) * enc[0]) mod modulus

        c = (pow((enc[2] * enc[3] - enc[5] * enc[0]), -1, modulus) * ((known_p1 - b * enc[1]) * enc[3] - (known_p2 - b * enc[4]) * enc[0])) % modulus

        # a * enc[0] + b * enc[1] + c * enc[2] == known_p1 mod modulus

        a = (pow(enc[0], -1, modulus) * (known_p1 - (b * enc[1] + c * enc[2]))) % modulus
        
        return a, b, c
    except:
        return None

mat = [[5882698740607461964, 6513775297662865481, 14215731151392670661], [3345074597440569669, 1695267570677006040, 12969748703402796197], [12897795408630100499, 1544685608328151724, 5579658597187306010]]
print(getMatrixInverse(mat))

print(calc(enc, alphabet.index("t"), alphabet.index("t"), alphabet.index("a"), modulus))
    
C = pow(enc[0], -1, modulus) * enc[3]

accabc = []
accdef = []
accghi = []

def judgeKey(k, enc, modulus):

    out = 0
    hasalpha = True
    for i in range(0,len(enc),3):
        dec = (k[0] * enc[i] + k[1] * enc[i+1] + k[2] * enc[i+2]) % modulus
        hasalpha = hasalpha and (dec < len(alphabet))
        out += dec #lower dec is favored; we prefer lowercase letters to all else
    return hasalpha, out

for guess_p3 in range(len(alphabet)):
    known_p1 = alphabet.index("t")
    known_p2 = alphabet.index("t")
    k_guess = calc(enc, known_p1, known_p2, guess_p3, modulus)
    if (k_guess):
        judgement = judgeKey(k_guess, enc, modulus)
        if (judgement[0]):
            accabc.append(k_guess)

print(accabc)


known_p1 = alphabet.index("j")
known_p2 = alphabet.index("f")
guess_p3 = alphabet.index("}")
enc2 = enc[:6] + enc[-3:]
k_guess = calc(enc2, known_p1, known_p2, guess_p3, modulus)
if (k_guess):
    judgement = judgeKey(k_guess, enc, modulus)
    if (judgement[0]):
        accdef.append(k_guess)

print(accdef)

for guess_p3 in range(len(alphabet)):
    known_p1 = alphabet.index("c")
    known_p2 = alphabet.index("{")
    k_guess = calc(enc, known_p1, known_p2, guess_p3, modulus)
    if (k_guess):
        accghi.append(k_guess)

print(len(accabc), len(accdef), len(accghi))

for ghi in accghi:
    try:    
        print(decI([accabc[0],accdef[0],ghi]))
    except:
        pass
