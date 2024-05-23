FROM pwn.red/jail:0.3.0
#20220421 20240212
COPY --from=ubuntu:kinetic / /srv
#:jammy-20211029 / /srv

WORKDIR /srv/app/

# COPY libc.so.6 /lib/x86_64-linux-gnu/libc.so.6

COPY out run
COPY ./flag.txt .
COPY ./oom.txt .

