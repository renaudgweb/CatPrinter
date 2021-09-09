#!/bin/bash

txt=$(<astro.txt)

curl --location -X POST --form text="$txt" --form 'font="MajorMonoDisplay-Regular.ttf"' --form 'size="24"' --form 'feed="100"' 'localhost:5000'
