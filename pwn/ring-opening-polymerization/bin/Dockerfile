FROM pwn.red/jail:0.3.0
COPY --from=ubuntu@sha256:3f85b7caad41a95462cf5b787d8a04604c8262cdcdf9a472b8c52ef83375fe15 / /srv

COPY out /srv/app/run
COPY flag.txt /srv/app/flag.txt
