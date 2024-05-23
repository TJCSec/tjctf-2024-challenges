FROM python:3.8.5-slim-buster

RUN pip install flask gunicorn requests lxml

COPY . /app

WORKDIR /app

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "-w", "4"]
