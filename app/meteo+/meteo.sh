#!/bin/bash

txt=$(<meteo.txt)

curl --location -X POST --form text="$txt" --form 'font="Lucida_Console_Regular.ttf"' --form 'size="22"' 'localhost:5000'
