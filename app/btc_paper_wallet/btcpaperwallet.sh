#!/bin/bash

/usr/local/opt/python-3.9.6/bin/python3.9 btcpaperwallet.py

sed -i 's/.\{30\}/& /g' txt1.txt

sed -i 's/.\{30\}/& /g' txt2.txt

curl --location -X POST --form text="DO NOT LOSE OR SHARE THIS PRIVATE KEY !" 'localhost:5000'

curl --location -X POST --form 'image=@/home/your/path/catprinter/app/btc_paper_wallet/privatekey-qrcode.png' 'localhost:5000'

txt1=$(<txt1.txt)
curl --location -X POST --form text="$txt1" 'localhost:5000'

curl --location -X POST --form text="PRIVATE KEY:" 'localhost:5000'

curl --location -X POST --form text="------------------------------" --form 'feed="100"' 'localhost:5000'

curl --location -X POST --form 'image=@/home/yourpath/Documents/catprinter/app/btc_paper_wallet/balancekey-qrcode.png' 'localhost:5000'

curl --location -X POST --form text="Balance & transactions (blockchain.com) :" --form 'feed="100"' 'localhost:5000'

curl --location -X POST --form text="------------------------------" --form 'feed="100"' 'localhost:5000'

curl --location -X POST --form 'image=@/home/your/path/catprinter/app/btc_paper_wallet/publicwalletqr.png' 'localhost:5000'

txt2=$(<txt2.txt)
curl --location -X POST --form text="$txt2" 'localhost:5000'

curl --location -X POST --form text="PUBLIC KEY:" --form 'feed="100"' 'localhost:5000'

curl --location -X POST --form 'image=@/home/your/path/catprinter/app/btc_paper_wallet/btc_logo.png' --form 'feed="100"' 'localhost:5000'

sudo rm privatekey-qrcode.png
sudo rm balancekey-qrcode.png
sudo rm publicwalletqr.png
echo "" > txt1.txt
echo "" > txt2.txt
