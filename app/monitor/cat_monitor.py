#!/usr/bin/env python3
import os
import json
import requests

import sys
sys.path.append('../config')
from config import HOME_PATH

from time import sleep, strftime, localtime

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
		if ready == True & transmit == True:
			print("CatPrinter 😺️ ready - ", strftime("%d-%m-%y %H:%M:%S", localtime()))
		elif ready == False:
			if stat_battery == True:
				os.system('php ' + HOME_PATH + '/app/monitor/NCbot.php xorg4qem "🙀️ Batterie faible ! 😿️ rappel dans 15 minutes si batterie non branchée"')
				sleep(900)
			if stat_cover == True:
				os.system('php ' + HOME_PATH + '/app/monitor/NCbot.php xorg4qem "🙀️ Capot ouvert ! 😿️ rappel dans 2 minutes si capot non fermé"')
				sleep(120)
			if stat_paper == True:
				os.system('php ' + HOME_PATH + '/app/monitor/NCbot.php xorg4qem "🙀️ Plus de papier ! 😿️ rappel dans 15 minutes si rouleau non changé"')
				sleep(900)
			if stat_temp == True:
				os.system('php ' + HOME_PATH + '/app/monitor/NCbot.php xorg4qem "🙀️ Température élevée ! 😿 rappel dans 1 minute si CatPrinter non refroidi"')
				sleep(60)
		else:
			os.system('php ' + HOME_PATH + '/app/monitor/NCbot.php xorg4qem "😿️ Erreur 🙀️"')
			print("\nCatPrinter 🙀️ ERROR - ", strftime("%d-%m-%y %H:%M:%S", localtime()), "\n")
			sleep(900)
	state()

while True:
	main()
	sleep(5)
