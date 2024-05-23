from random import randrange, sample, shuffle
import json
from uuid import uuid4

qs = [
    {
        'question': 'what is the best taylor swift song?',
        'answers': [
            'daylight (stosp\'s version)',
            'all too well (5 minute version)',
            'cruel summer',
            'all too well (10 minute version)',
        ]
    },
    {
        'question': 'what is the best taylor swift lyric?',
        'answers': [
            'i\'m a mess, but i\'m the mess that you wanted',
            'i\'m standing at the restaurant',
            'you and me, that\'s my whole world',
            'i\'d be a fearless leader',
        ]
    },
    {
        'question': 'when was taylor swift born?',
        'answers': [
            '1989',
            '4321',
            '1987',
            '7776',
        ]
    },
    {
        'question': 'why am I crying right now?',
        'answers': [
            'idk man',
            'I\'m listening to all too well',
            'get help',
            'I just watched the all too well short film',
        ]

    },
    {
        'question': 'what is?',
        'answers': [
            'meow meow meow meow meow',
            'meow meow meow meow',
            'meow meow meow',
            'meow meow meow meow meow meow',
        ]
    },
    {
        'question': 'what is the better version?',
        'answers': [
            'taylor\'s version',
            'the original',
            'both',
            'neither',
        ]
    },
    {
        'question': 'how was the eras tour?',
        'answers': [
            'a fever dream',
            'idk I couldn\'t get tickets',
            'star-struck',
            'I slept through it',
        ]
    },
    {
        'question': 'can I ask you a question???',
        'answers': [
            'did you ever have someone kiss you in a crowded room?',
            'me-hee-hee',
            'por supuesto',
            'what did you do???'
        ]
    },
    {
        'question': 'when did I last listen to taylor swift?',
        'answers': [
            'last week',
            'today',
            'yesterday',
            'last month',
        ]
    },
    {
        'question': 'what was the last song I cried to?',
        'answers': [
            'all too well',
            'all too well',
            'all too well',
            'all too well',
        ]
    }
]

questions = [
    sample([{**qs[i], 'answer': 0} for i in range(len(qs))], len(qs)) for _ in range(1)
]

questions = [q for qs in questions for q in qs]

correct_answers = [q['answers'][0] for q in questions]
for q in questions:
    shuffle(q['answers'])
    q['answer'] = q['answers'].index(correct_answers.pop(0))

    # if correct answer appears in other answers, pick a random one
    if q['answers'][1] == q['answers'][0]:
        q['answer'] = randrange(len(q['answers']))

kahoot = {
    'name': 'swiftie-core',
    'questions': questions,
}


with open('server/kahoot.json', 'w') as f:
    json.dump(kahoot, f)
