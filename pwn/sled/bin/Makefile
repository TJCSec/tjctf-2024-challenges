.PHONY: all

all:
	gcc -o out -fno-stack-protector -z execstack -Wno-stringop-overflow -no-pie main.c
	cp out ../
