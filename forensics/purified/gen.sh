#!/bin/sh

echo converting...
python3 gen_helper.py
convert out.png out.qoi
echo qoi
rm out.png
echo done!