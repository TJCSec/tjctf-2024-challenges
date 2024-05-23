import sys
from pyrage import passphrase  # type: ignore


def main():
    fname, passname = sys.argv[1:]
    data = open(fname, "rb").read()
    possibles = open(passname).read().splitlines()
    for password in possibles:
        print(password)
        try:
            flag = passphrase.decrypt(data, password)
            print(flag)
        except:
            continue


if __name__ == "__main__":
    main()
