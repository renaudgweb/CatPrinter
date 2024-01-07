#!/bin/bash

sudo systemctl stop openwebrx && sudo systemctl disable openwebrx

current_path=$(pwd)

sudo aplay -Dhw:0,0 -q "$current_path/Sound/start.wav"
