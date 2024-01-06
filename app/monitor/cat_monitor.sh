#!/bin/bash

source ../config/config.sh

cd "${HOME_PATH}CatPrinter/app/monitor"
sleep 20
python3 cat_monitor
