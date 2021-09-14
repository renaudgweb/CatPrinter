#!/usr/bin/env python3

import sys
import os
import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM0', 9600)
def main():
  while True:
    data = ser.readline()
    if data:
      data = data.decode('ascii')
      #data = data.replace("\n", "")
      sleep(0.5)
      print(data)
      os.system("curl --location -X POST --form 'text=\"" + data + "\"' --form 'size=\"18\"' 'localhost:5000'")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(' -> Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
