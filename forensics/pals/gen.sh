#!/bin/sh

# force a PLTE chunk w/ 40 colors
convert pals_original.png -colors 40 pals_palette.png
python3 palette_change.py
echo 'done'