#!/usr/bin/env python3
import os
import requests
from time import sleep, strftime, localtime
from configparser import ConfigParser

# Load configuration from a file
config = ConfigParser()
config.read('../config/config.ini')

NEXTCLOUD_TALK_CHANNEL_ID = config.get('Nextcloud_Talk_api', 'NEXTCLOUD_TALK_CHANNEL_ID')
HOME_PATH = config.get('Paths', 'HOME_PATH')


def main():
    r = requests.get("http://localhost:5000")
    d = r.json()

    address = d['address']
    ready = d['ready']
    transmit = d['transmit']
    stat_battery = d['status']['battery_low']
    stat_cover = d['status']['cover_open']
    stat_paper = d['status']['no_paper']
    stat_temp = d['status']['over_temp']

    def state():
        if ready and transmit:
            print("CatPrinter 😺️ ✔️ ready - ", strftime("%d-%m-%y %H:%M:%S", localtime()))
        elif not ready:
            if stat_battery:
                os.system(f'php {HOME_PATH}/app/monitor/NCbot.php {NEXTCLOUD_TALK_CHANNEL_ID} "🙀️ ⚡ Batterie faible ! 😿️ rappel dans 15 minutes si batterie non branchée"')
                print("🙀️ ⚡ Batterie faible ! 😿️ rappel dans 15 minutes si batterie non branchée ", strftime("%d-%m-%y %H:%M:%S", localtime()))
                sleep(900)
            if stat_cover:
                os.system(f'php {HOME_PATH}/app/monitor/NCbot.php {NEXTCLOUD_TALK_CHANNEL_ID} "🙀️ 🔓  Capot ouvert ! 😿️ rappel dans 2 minutes si capot non fermé"')
                print("🙀️ 🔓  Capot ouvert ! 😿️ rappel dans 2 minutes si capot non fermé ", strftime("%d-%m-%y %H:%M:%S", localtime()))
                sleep(120)
            if stat_paper:
                os.system(f'php {HOME_PATH}/app/monitor/NCbot.php {NEXTCLOUD_TALK_CHANNEL_ID} "🙀️ 🧻 Plus de papier ! 😿️ rappel dans 15 minutes si rouleau non changé"')
                print("🙀️ 🧻 Plus de papier ! 😿️ rappel dans 15 minutes si rouleau non changé ", strftime("%d-%m-%y %H:%M:%S", localtime()))
                sleep(900)
            if stat_temp:
                os.system(f'php {HOME_PATH}/app/monitor/NCbot.php {NEXTCLOUD_TALK_CHANNEL_ID} "🙀️ 🌡️ Température élevée ! 😿 rappel dans 1 minute si CatPrinter non refroidi"')
                print("🙀️ 🌡️ Température élevée ! 😿 rappel dans 1 minute si CatPrinter non refroidi ", strftime("%d-%m-%y %H:%M:%S", localtime()))
                sleep(60)
        else:
            os.system(f'php {HOME_PATH}/app/monitor/NCbot.php {NEXTCLOUD_TALK_CHANNEL_ID} "😿️ ❌ Erreur 🙀️"')
            print("\nCatPrinter 🙀️ ❌ ERROR - ", strftime("%d-%m-%y %H:%M:%S", localtime()), "\n")
            sleep(900)
            state()


while True:
    main()
    sleep(5)
