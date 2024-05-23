from websocket import create_connection
import requests
import base64
import json
import os
from time import time

DELAY = 0.0058
BASE_URL = 'https://kaboot-81851f9a0bdd0f85.tjc.tf'


def recv(ws):
    return base64.b64decode(ws.recv()).decode()


def recv_json(ws):
    return json.loads(recv(ws))


def send(ws, data):
    ws.send(base64.b64encode(data.encode()))


def send_json(ws, data):
    send(ws, json.dumps(data))


for i in range(1):
    res = requests.post(f'{BASE_URL}/create')
    res_url = res.url.split('//')[1]

    for i in range(100):
        ws = create_connection(f'wss://{res_url}')

        recv(ws)

        while True:
            d = recv_json(ws)

            if 'end' in d:
                print(d)
                break

            send_json(ws, {
                'id': os.urandom(4).hex(),
                'answer': d['answer'],
                'send_time': time()
            })

res = requests.post(f'{BASE_URL}/create')
res_url = res.url.split('//')[1]

for i in range(100):
    ws = create_connection(f'wss://{res_url}')

    print(recv(ws))
    uuid = os.urandom(4).hex()

    while True:
        d = recv_json(ws)

        if 'end' in d:
            print(d)
            break

        send_json(ws, {
            'id': uuid,
            'answer': d['answer'],
            'send_time': time() + DELAY + i / 10000
        })
