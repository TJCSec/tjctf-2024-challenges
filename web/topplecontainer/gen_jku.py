import jwt
import json
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from hashlib import sha256

key_data = load_pem_public_key(open("public.pem", "rb").read())
key = json.loads(jwt.algorithms.ECAlgorithm.to_jwk(key_data))
h = sha256()
h.update(json.dumps(key, sort_keys=True).encode("utf-8"))
key["kid"] = h.hexdigest()
print(key)

with open("server/app.py", "r") as f:
    lines = f.read().splitlines()
    for i in range(len(lines)):
        if lines[i][:7] == 'KID = "':
            lines[i] = f'KID = "{key["kid"]}"'

with open("server/app.py", "w") as f:
    f.write("\n".join(lines))

with open("jwks.json", "w") as f:
    json.dump({"keys": [key]}, f, indent=4)

# print(key.as_json())
