#!/bin/bash

/usr/local/opt/python-3.9.6/bin/python3.9 btcpaperwallet.py

curl --location -X POST --form text="DO NOT LOSE OR SHARE THIS PRIVATE KEY !" 'localhost:5000'

curl --location -X POST --form 'image=@/home/rengweb/Documents/catprinter/app/btc_paper_wallet/privatekey-qrcode.png' 'localhost:5000'

txt1=$(<txt1.txt)
curl --location -X POST --form text="$txt1" 'localhost:5000'

curl --location -X POST --form text="PRIVATE KEY:" --form 'feed="100"' 'localhost:5000'

curl --location -X POST --form text="------------------------------" 'localhost:5000'

curl --location -X POST --form 'image=@/home/rengweb/Documents/catprinter/app/btc_paper_wallet/publicwalletqr.png' 'localhost:5000'

txt2=$(<txt2.txt)
curl --location -X POST --form text="$txt2" 'localhost:5000'

curl --location -X POST --form text="PUBLIC KEY:" --form 'feed="100"' 'localhost:5000'

curl --location -X POST --form 'image=@/home/rengweb/Documents/catprinter/app/btc_paper_wallet/btc_logo.png' --form 'feed="100"' 'localhost:5000'

sudo rm privatekey-qrcode.png
sudo rm publicwalletqr.png
