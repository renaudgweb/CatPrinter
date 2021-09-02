![image text](catprinter.jpg "Thermal Cat printer")

# CatPrinter
Driver, Telegram bot &amp; apps for the thermal "cat printer"

---
> pip install -r requirements.txt

> apt install wkhtmltopdf
---

## START SCRIPT:
python3 -tt print_server.py



## HTML TO IMAGE:
wkhtmltoimage --width 384 https://mastodon.social/explore /home/your/path/catprinter/test.png

wkhtmltoimage --width 384 --height 500 https://mastodon.social/explore /home/your/path/catprinter/test.png



## SEND IMAGE:
curl --location -X POST --form 'image=@/home/your/path/catprinter/test.png' --form 'feed="100"' 'localhost:5000'



## SEND TEXT:
curl --location -X POST --form 'text="Lorem ipsum."' --form 'feed="100"' 'localhost:5000'



## FEED PAPIER:
curl --location --request POST --form 'feed="100"' 'localhost:5000'

---

### Credits
[amber-sixel gb01print](https://github.com/amber-sixel/gb01print)
[xssfox print_server](https://gist.github.com/xssfox/b911e0781a763d258d21262c5fdd2dec)
