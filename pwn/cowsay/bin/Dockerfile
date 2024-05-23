FROM pwn.red/jail:0.3.0
COPY --from=ubuntu@sha256:2af372c1e2645779643284c7dc38775e3dbbc417b2d784a27c5a9eb784014fb8 / /srv

COPY chall /srv/app/run

COPY flag.txt /srv/app/
