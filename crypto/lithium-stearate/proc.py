


def proc(name):
    lines = open(name,"r").read().split("\n")[:-1]
    pt_ct = [i.replace("Plaintext, ciphertext: ","") for i in lines if "Plaintext, ciphertext: " in i]
    flag = [i.replace("Flag, ciphertext: ","") for i in lines if "Flag, ciphertext: " in i]
    print("falg:\n", [int(i) for i in flag])
    print("{")
    for i in pt_ct:
        print("{",i.replace(" ", ","),"},")
    
proc("output2.txt")