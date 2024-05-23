import tqdm
import re
import random
import time
from pyrage import passphrase

max_len = 7
word_buckets = []


def get_word_list(letters):
    with open("amontillado.txt") as f:
        text = f.read()
    wordlst = list(set(re.sub("[^a-z]", " ", text.lower()).split()))
    return [
        word
        for word in wordlst
        if all(letters.count(ch) >= word.count(ch) for ch in word)
    ]


def read_hint(fname):
    contents = open(fname).read()
    letters = re.findall(r"\d+ \[(\w)\];", contents)
    return letters


def get_passwords(letters, depth):
    if depth <= 0:
        return
    for i in range(len(letters), 1, -1):
        for word in word_buckets[i]:
            if all(letters.count(ch) >= word.count(ch) for ch in word):
                remaining_letters = letters.copy()
                for ch in word:
                    if ch in remaining_letters:
                        remaining_letters.remove(ch)
                if len(remaining_letters) == 0:
                    yield word
                else:
                    for string in get_passwords(remaining_letters, depth - 1):
                        if string:
                            yield word + string


def main():
    global word_buckets
    letters = read_hint("hint.txt")
    words = get_word_list(letters)

    word_buckets = [[] for _ in range(len(letters) + 1)]
    for word in words:
        word_buckets[len(word)].append(word)

    print(f"Found {len(words)} words for {len(letters)} letters")

    st = time.time()
    i = 0
    info = open("secret.txt", "rb").read()
    for pwd in get_passwords(letters, max_len):
        print(i, end="\r")
        i += 1
        try:
            data = passphrase.decrypt(info, pwd)
            print(pwd)
            print(data)
            print(f"Found in {time.time()-st:.5g}s")
            print()
        except:
            continue

    print(f"Bruteforced possibilities in {time.time()-st:.5g}s")


if __name__ == "__main__":
    main()
