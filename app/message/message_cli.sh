#!/bin/bash

TXT=$(whiptail --title "Cat Printer message" --inputbox "Bonjour et bienvenue, veuillez laisser votre message: " 10 60 3>&1 1>&2 2>&3)

exitstatus=$?
if [ $exitstatus = 0 ]; then
    curl --location -X POST --form text="$TXT" --form 'font="VG5000-Regular_web.ttf"' --form 'size="26"' --form 'feed="100"' 'localhost:5000'
else
    echo "Message annulé."
fi
