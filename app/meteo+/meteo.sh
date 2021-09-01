#!/bin/bash

txt=$(<meteo.txt)

curl --location -X POST --form text="$txt" --form 'font="ocr_b.ttf"' --form 'size="24"' --form 'feed="100"' 'localhost:5000'
