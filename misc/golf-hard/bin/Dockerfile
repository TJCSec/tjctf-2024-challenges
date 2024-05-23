FROM python:3.11-slim-buster AS app

RUN python -u -m pip install numpy regex tabulate

FROM pwn.red/jail:0.3.0

COPY --from=app / /srv
COPY golf.py /srv/app/run
COPY flag.txt /srv/app/
COPY challenges/ /srv/app/challenges/
RUN chmod +x /srv/app/run

ENV JAIL_MEM=40M
ENV JAIL_CPU=1000
ENV JAIL_TIME=60
