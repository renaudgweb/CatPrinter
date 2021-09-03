#!/bin/bash

TXT=$(<message.txt)

curl --location -X POST --form text="$TXT" --form 'font="VG5000-Regular_web.ttf"' --form 'size="26"' --form 'feed="100"' 'localhost:5000'
