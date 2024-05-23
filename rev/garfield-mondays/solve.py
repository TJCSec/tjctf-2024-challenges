from hashlib import sha256
import requests

BASE_URL = 'https://garfield-mondays.tjc.tf'

correct = 'cf4627b3786c8bad8cb855567bda362d8eca1809ea8839423682715cdf3aadad'

enc = None

for h in range(24):
    for m in range(60):
        time = f'{h:02d}:{m:02d}'
        if sha256(time.encode()).hexdigest() == correct:
            enc = time
            break

if enc is None:
    print('Failed to find the correct time')
    exit()

mapped = {
    '(': "46",
    '*': "!",
    '0': "4",
    '1': "g",
    '2': "i",
    '3': "l",
    '4': "f",
    '5': "e",
    '6': "d",
    '7': "1",
    '8': "2",
    '9': "3",
    'a': "j",
    'b': "c",
    'j': "k",
    'n': "v",
    'o': "w",
    'q': "w",
    'z': "2",
    '}': "{"
}

def encode_time(time):
    return ''.join(mapped[c] if c in mapped else '' for c in time)

modified_time = enc.replace(':', '')
time_as_int = int(modified_time)
calculated_value = (time_as_int * 100) + 225390
res = modified_time + str(calculated_value)
password = encode_time(res)

print(requests.post(f'{BASE_URL}/form_handler',
              data={
                  'username': 'garfield',
                  'password': password
              }).json()['message'])
