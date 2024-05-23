const socket = location.protocol === 'http:' ? new WebSocket(`ws://${location.href.split('//', 2)[1]}`) : new WebSocket(`wss://${location.href.split('//', 2)[1]}`);

const id = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'.replace(/x/g, c => {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);

    return v.toString(16);
});

let nameReceived = false;

socket.addEventListener('message', async e => {
    const text = await e.data.text();
    const options = document.querySelectorAll('.option');

    if (!nameReceived) {
        const name = atob(text);
        document.getElementById('name').innerText = name;
        nameReceived = true;
        return;
    }

    const data = JSON.parse(atob(text));

    if (data.end) {
        document.getElementById('question').innerText = data.message;
        options.forEach(o => {
            o.querySelector('h2').innerText = '';
            o.disabled = true;
        });
        return;
    }

    const { question, answers, answer, scores, send_time } = data;

    console.log(scores);

    const score = scores.find(s => s[1] === id);

    document.getElementById('score').innerText = score ? Math.floor(score[2]) : 0;

    document.getElementById('question').innerText = question;

    answers.forEach((a, i) => {
        const o = options[i];
        o.querySelector('h2').innerText = a;

        o.addEventListener('click', () => {
            if (i === answer) {
                o.classList.add('correct');

                setTimeout(() => {
                    o.classList.remove('correct');
                }, 100);
            }

            options.forEach((o, _) => {
                const oNew = o.cloneNode(true);
                o.parentNode.replaceChild(oNew, o);
            })

            socket.send(btoa(JSON.stringify({
                id: id,
                answer: i,
                send_time: send_time
            })));
        });
    });
});
