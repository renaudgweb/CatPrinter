#!/bin/bash

python3 job.py

txt=$(<job.txt)

curl --location -X POST --form text="$txt" --form 'feed="100"' 'localhost:5000'
