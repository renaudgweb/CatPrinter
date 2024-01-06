#!/bin/bash

source ../config/config.sh

URL=$(whiptail --title "Cat Printer Web Print" --inputbox "Bonjour et bienvenue, veuillez entrer une URL: " 10 60 3>&1 1>&2 2>&3)

wkhtmltoimage --width 384 $URL "${HOME_PATH}CatPrinter/app/web_print/test.png"

exitstatus=$?
if [ $exitstatus = 0 ]; then
    curl --location -X POST --form "image=@${HOME_PATH}CatPrinter/app/web_print/test.png" --form 'feed="100"' 'localhost:5000'
else
    echo "Message annulé."
fi
