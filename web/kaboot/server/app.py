from flask import Flask, render_template, redirect, request, url_for
from flask_sock import Sock
import json
from base64 import b64decode, b64encode
from time import time
import os

app = Flask(__name__)
sock = Sock(app)

flag = open('flag.txt').read().strip()

with open('kahoot.json') as f:
    kahoot = json.load(f)


@app.route('/')
def index():
    return render_template('create.jinja')


@app.route('/create', methods=['POST'])
def create():
    return redirect(url_for('room', room_id=os.urandom(4).hex()))


@app.route('/room/<room_id>')
def room(room_id):
    return render_template('room.jinja', room_code=room_id)


'''
1. send question and answer (b64 encoded)
2. receive answer back (b64 encoded id)
'''

all_scores = []


def get_room_scores(room_id):
    scores = []
    for score_data in all_scores:
        if score_data[0] == room_id:
            scores.append(score_data)

    return scores


def edit_score(scores, room_id, uid, new_score):
    for i, score_data in enumerate(scores):
        if score_data[1] == uid:
            scores[i][2] = new_score
            return scores

    all_scores.append([room_id, uid, new_score])
    scores.append(all_scores[-1])
    return scores


def get_score(scores, room_id, uid):
    for score_data in scores:
        if score_data[0] == room_id and score_data[1] == uid:
            return score_data[2]

    return 0


@sock.route('/room/<room_id>')
def room_sock(sock, room_id):
    sock.send(b64encode(kahoot['name'].encode()))
    scores = get_room_scores(room_id)
    for i, q in enumerate(kahoot['questions']):
        sock.send(b64encode(json.dumps({
            'send_time': time(),
            'scores': scores,
            **q,
        }).encode()))

        data = sock.receive()
        data = json.loads(b64decode(data).decode())

        send_time = data['send_time']
        recv_time = time()

        if (scores := get_room_scores(room_id)) is not None and send_time >= time():
            sock.send(b64encode(json.dumps({
                'scores': scores,
                'end': True,
                'message': '???'
            }).encode()))
            return

        if i == 0:
            edit_score(scores, room_id, data['id'], 0)

        if data['answer'] == q['answer']:
            edit_score(scores,
                       room_id,
                       data['id'],
                       get_score(scores, room_id, data['id']) + 1000 + max((send_time - recv_time) * 50, -500))

    sock.send(b64encode(json.dumps({
        'scores': scores,
        'end': True,
        'message': f'omg congrats, swiftie!!! {flag}' if get_score(scores, room_id, data['id']) >= 1000 * len(kahoot['questions']) else 'sucks to suck brooooooooo'
    }).encode()))


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
