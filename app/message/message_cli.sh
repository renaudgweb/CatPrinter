#!/bin/bash

TXT=$(whiptail --title "Cat Printer message" --inputbox "Bonjour et bienvenue, veuillez laisser votre message: " 10 60 3>&1 1>&2 2>&3)

exitstatus=$?
if [ $exitstatus = 0 ]; then
    curl --location -X POST --form text="$TXT" --form 'feed="100"' 'localhost:5000'
else
    echo "Message annulé."
fi
