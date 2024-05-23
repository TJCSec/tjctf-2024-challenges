##http://theamazingking.com/crypto-multi.php

import secrets

S = [3, 14, 1, 10, 4, 9, 5, 6, 8, 11, 15, 2, 13, 12, 0, 7]
invS = [14, 2, 11, 0, 4, 6, 7, 15, 8, 5, 3, 9, 13, 12, 1, 10]
P = [1, 6, 0, 7, 2, 3, 5, 4]
invP = [2, 0, 4, 5, 7, 6, 1, 3]

def spBox(i):
    left = i >> 4
    right = i & 0xf
    left = S[left]
    right = S[right]
    comb = right | (left << 4)
    total = 0
    #swap bits according to p box
    for c in range(8):
         inBit = comb % (pow(2, c + 1));
         inBit = inBit // (pow(2, c));
         total += inBit * pow(2, P[c]);
    #print(total)
    return total

def invspBox(i):
    for j in range(256):
        if (spBox(j) == i):
            return j

SP = [spBox(i) for i in range(256)]

assert SP == [78,205,14,204,13,142,15,77,140,206,207,76,143,141,12,79,122,249,58,248,57,186,59,121,184,250,251,120,187,185,56,123,70,197,6,196,5,134,7,69,132,198,199,68,135,133,4,71,90,217,26,216,25,154,27,89,152,218,219,88,155,153,24,91,98,225,34,224,33,162,35,97,160,226,227,96,163,161,32,99,86,213,22,212,21,150,23,85,148,214,215,84,151,149,20,87,102,229,38,228,37,166,39,101,164,230,231,100,167,165,36,103,106,233,42,232,41,170,43,105,168,234,235,104,171,169,40,107,82,209,18,208,17,146,19,81,144,210,211,80,147,145,16,83,94,221,30,220,29,158,31,93,156,222,223,92,159,157,28,95,126,253,62,252,61,190,63,125,188,254,255,124,191,189,60,127,74,201,10,200,9,138,11,73,136,202,203,72,139,137,8,75,118,245,54,244,53,182,55,117,180,246,247,116,183,181,52,119,114,241,50,240,49,178,51,113,176,242,243,112,179,177,48,115,66,193,2,192,1,130,3,65,128,194,195,64,131,129,0,67,110,237,46,236,45,174,47,109,172,238,239,108,175,173,44,111]

invSP = [invspBox(i) for i in range(256)]

assert all([invSP[SP[i]] == i for i in range(256)])

key = secrets.token_bytes(4)

oracle_calls = 0

def r(i,k):
    return SP[i^k]

def enc(i, k0, k1, k2, k3):
    r0 = r(i, k0)
    r1 = r(r0, k1)
    r2 = r(r1, k2)
    return r(r2, k3)

def encrypt(i, keys):
    global oracle_calls
    if (keys == key):
        oracle_calls += 1
    return enc(i, keys[0], keys[1], keys[2], keys[3])

def rec_chains(curr_chain, linkages, depth):

    #if (3 - depth != len(curr_chain)):
        #print("SMACK", depth, curr_chain)
    
    if (depth == 0):
        #print(len(curr_chain))
        #print(curr_chain)
        return (curr_chain,)

    recs = []
    
    for pos_next in linkages:
        if (curr_chain):
            last = curr_chain[-1] 
            if (last[2] == pos_next[1]):
                #possible connection
                new = [i for i in curr_chain]
                new.append(pos_next)
                rec = rec_chains(tuple(new), linkages, depth - 1)
                #print("New",depth,new)
                if (rec):
                    [recs.append(r) for r in rec]
        else:
            rec = rec_chains([pos_next], linkages, depth - 1)
            if (rec): 
                [recs.append(r) for r in rec]
    if (recs):
        return tuple(list(set(recs)))
    return ()

def msum(l):
    a = 1
    for i in l:
        a *= i
    return a

def make_chains(tab, conf = 63):
    chains = []
    known_in = set()
    known_out = set()
    for in_diff in range(1, 256):
        for out_diff in range(256):
            if (tab[in_diff][out_diff] > conf):
                chains.append((tab[in_diff][out_diff], in_diff, out_diff))
                known_in.add(in_diff)
                known_out.add(out_diff)
    clean_links = []


    
    #print(known_in, known_out)
    for i in chains:
        if not ((i[2] not in known_out) and (i[3] not in known_in)):
            clean_links.append(i)
    print("Differential characteristics:",clean_links)
    #print(clean_links)
    clean_links = sorted(clean_links, key = lambda x: -x[0])
    #print(clean_links)

    good_chains = [list(a) for a in rec_chains([], clean_links, 3)]
    #print(good_chains)

    good_chains = [[msum([link[0] / 256. for link in chain]), chain] for chain in good_chains]    

    return [i for i in sorted(good_chains, key = lambda x: -x[0])]
    
def make_cnxns():
    tab = [[0 for i in range(256)] for j in range(256)]
    print("Table is:",len(tab), len(tab[0]))
    for in_diff in range(256):
        for byte in range(256):
            out_diff = spBox(byte) ^ spBox(byte^in_diff)
            tab[in_diff][out_diff] += 1

    chains = make_chains(tab)
    #for chain in chains:
        #print(chain)

                
    return tab, chains

def get_good_pair(dif_i, dif_o, oracle):
    while True:
        p0 = secrets.randbelow(256)
        p1 = p0 ^ dif_i
        c0 = invSP[oracle(p0)]
        c1 = invSP[oracle(p1)]
        if (dif_o == c0 ^ c1):
            return (p0, c0)

def get_options(in_diff, out_diff):
    poss = []
    for byte in range(256):
        obs_out_diff = SP[byte] ^ SP[byte ^ in_diff]
        if (obs_out_diff == out_diff):
            poss.append(byte)
    return poss

def recover_key(oracle = lambda i: encrypt(i, key)):
    
    tab, chains = make_cnxns()

    #validation pairs
    known_pairs = []
    for i in range(16):
        p = secrets.randbelow(256)
        known_pairs.append((p, oracle(p)))
        
    curr_chain = chains[1][1]
    #curr_chain = [(0, 176, 4), (0, 4, 3), (0, 3, 192)]
    diff_i = curr_chain[0][1]
    diff_o = curr_chain[-1][2]
    print("Input/output differentials",diff_i, diff_o)
    print(curr_chain)

    old_gp = []
    for i in range(4):
        good_pair = get_good_pair(diff_i, diff_o, oracle)
        while (good_pair in old_gp):
            good_pair = get_good_pair(diff_i, diff_o, oracle)
        old_gp.append(good_pair)
        
        #good_pair = (222, oracle(222))
        #print("201 and 121",oracle(201), oracle(121))
        print("Good pair:",good_pair)

        assert invSP[oracle(good_pair[0])] ^ invSP[oracle(good_pair[0] ^ diff_i)] == diff_o

        #found keys
        found_keys = []

        # get options for SPbox 1
        s0_op = get_options(curr_chain[0][1],curr_chain[0][2])
        s1_op = get_options(curr_chain[1][1],curr_chain[1][2])
        s2_op = get_options(curr_chain[2][1],curr_chain[2][2])

        ctr = 0

        #print(s0_op)
        #print(s1_op)
        #print(s2_op)

        for s0_guess in s0_op:
            for s1_guess in s1_op:
                for s2_guess in s2_op:
                    p = good_pair[0]
                    c = good_pair[1]

                    k0_guess = s0_guess ^ p
                    
                    r1_guess = SP[s0_guess]
                    k1_guess = s1_guess ^ r1_guess
                    
                    r2_guess = SP[s1_guess]
                    k2_guess = s2_guess ^ r2_guess

                    r3_guess = SP[s2_guess]
                    k3_guess = r3_guess ^ c

                    k_guess = k0_guess.to_bytes(1,"little") + k1_guess.to_bytes(1,"little") + k2_guess.to_bytes(1,"little") + k3_guess.to_bytes(1,"little")               

                    ctr += 1

                    if (ctr % 10000 == 0):
                        print("\rKeys tested:",ctr)
                
                    #validate
                    if (all([encrypt(pair[0], k_guess) == pair[1] for pair in known_pairs])):
                        print("Found a key:", k_guess)
                        if (k_guess == key):
                            print("This is THE key...")
                        return k_guess

print("real key =",[a for a in key], key)
print(encrypt(120, key))
print(encrypt(200, key))

recover_key()
print(oracle_calls,"oracle calls used.")
