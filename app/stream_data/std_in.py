#!/usr/bin/env python3

# from sys import stdin
#
# my_input2 = stdin.readline()
# print("Input = {}".format(my_input2))

import sys
import fileinput
import os
from time import sleep

while True:
    for line in fileinput.input():
        #line = line.replace("\n", "")
        sleep(0.5)
        print(line)
        os.system("curl --location -X POST --form 'text=\"" + line + "\"' --form 'size=\"18\"' 'localhost:5000'")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(' -> Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
