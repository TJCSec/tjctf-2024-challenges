#!/bin/sh

openssl ecparam -name prime256v1 -genkey -noout -out private.ec.key
openssl ec -in private.ec.key -pubout -out public.pem

cp server/app.py server/app.py.bak
python3 gen_jku.py

rm public.pem
mv jwks.json server/static/
mv private.ec.key server/