#!/bin/bash

curl --location -X POST --form 'image=@/home/rengweb/Documents/catprinter/app/dall_e/dalle.png' 'localhost:5000'

curl --location -X POST --form 'feed=\"100\"' 'localhost:5000'
