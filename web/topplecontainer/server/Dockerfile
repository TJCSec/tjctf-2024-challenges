FROM python:3.8-slim-buster

WORKDIR /app

RUN python -m pip install flask gunicorn pyjwt cryptography

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
