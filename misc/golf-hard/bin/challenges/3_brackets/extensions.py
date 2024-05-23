import random


def more_matches():
    ms = []
    for _ in range(50):
        c = 0
        s = ""
        for _ in range(random.randrange(10000, 20000, 2)):
            if c == 0:
                s += "<"
                c += 1
            else:
                if random.randint(0, 1):
                    s += "<"
                    c += 1
                else:
                    s += ">"
                    c -= 1
        if c != 0:
            s += ">" * c
        ms.append(s)
    return ms


def more_nonmatches():
    ms = []
    for _ in range(50):
        c = 0
        s = ""
        for _ in range(random.randrange(10000, 20000, 2)):
            if c == 0:
                s += "<"
                c += 1
            else:
                if random.randint(0, 1):
                    s += "<"
                    c += 1
                else:
                    s += ">"
                    c -= 1
        if c != 0:
            s += ">" * c
        ls = list(s)
        if random.random() > 0.7:
            ls = [">"] + ls + ["<"]
        else:
            ls.insert(random.randint(0, len(ls)), random.choice(["<", ">"]))
        ms.append("".join(ls))
    return []
