#!/bin/bash

txt=$(<acars.txt)

curl --location -X POST --form text="$txt" --form 'feed="100"' 'localhost:5000'
