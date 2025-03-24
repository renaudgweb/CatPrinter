#!/usr/bin/env python3

## Read from standard input (stdin) :
# cat file.txt | python3 std_in.py
# echo "Hello World" | python3 std_in.py

## Read an input file :
# python3 std_in.py file.txt

## Interactive mode (keyboard input) :
# python3 std_in.py
## The script waits for you to type a line on the keyboard, then it will
## send it as a POST after Enter. If you want to quit, use Ctrl+C.


# from sys import stdin
#
# my_input2 = stdin.readline()
# print("Input = {}".format(my_input2))

import sys
import fileinput
import os
from time import sleep

try:
    while True:
        for line in fileinput.input():
            # line = line.replace("\n", "")
            sleep(0.5)
            print(line)
            os.system(f"curl --location -X POST --form 'text=\"{line}\"' --form 'size=\"18\"' 'localhost:5000'")
except KeyboardInterrupt:
    print(" -> Interrupted")
    sys.exit(0)
