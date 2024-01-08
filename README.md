![image text](catprinter.jpg "Thermal Cat printer")

# CatPrinter
Driver, Telegram bot &amp; apps for the thermal "cat printer"


## Install script:
> `sudo chmod +x install.sh && sudo ./install.sh`

Choose the Default install : "D" for normal installation

After, you can choose the Web install : "W" for the PHP web log file
(installed in /var/www/html/cat/index.php)

Reboot after the execution of this script

> `sudo reboot`


---
Update the configuration files with your API keys:

> app > config > config.py

> app > config > config.php
---
Be sure to replace the fonts with your own in the code, the fonts must be in the root folder. Like "Lucida_Console_Regular.ttf".


## HTML to image:
> `wkhtmltoimage --width 384 https://example.com /home/your/path/catprinter/test.png`

> `wkhtmltoimage --width 384 --height 500 https://example.com /home/your/path/catprinter/test.png`

## Send image:
> `curl --location -X POST --form 'image=@/home/your/path/catprinter/test.png' --form 'feed="100"' 'localhost:5000'`

## Send text:
> `curl --location -X POST --form 'text="Lorem ipsum."' --form 'feed="100"' 'localhost:5000'`

## Feed paper:
> `curl --location --request POST --form 'feed="100"' 'localhost:5000'`
---
### Credits
[amber-sixel gb01print](https://github.com/amber-sixel/gb01print)

[xssfox print_server](https://gist.github.com/xssfox/b911e0781a763d258d21262c5fdd2dec)
