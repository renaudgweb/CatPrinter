#!/bin/bash

sudo systemctl stop openwebrx && sudo systemctl disable openwebrx

sudo aplay -Dhw:0,0 -q Sound/start.wav
