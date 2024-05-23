FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install flask flask_sock gunicorn

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
