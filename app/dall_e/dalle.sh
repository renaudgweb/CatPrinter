#!/bin/bash

source ../config/config.sh

curl --location -X POST --form "image=@${HOME_PATH}CatPrinter/app/dall_e/dalle.png" --form 'feed="100"' 'localhost:5000'
