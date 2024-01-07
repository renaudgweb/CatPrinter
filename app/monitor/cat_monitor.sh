#!/bin/bash

source ../config/config.sh

cd "${HOME_PATH}/app/monitor"
sleep 20
python3 cat_monitor
