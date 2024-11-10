![image text](catprinter.jpg "Thermal Cat printer")

# CatPrinter
Driver, Telegram bot &amp; apps for the thermal "cat printer"


## Install script:

### Before start:
**You need API keys from : Telegram Bot, OpenWeather and OpenAI**

> `sudo chmod +x install.sh && sudo ./install.sh`

Choose the Default install : [D] for normal installation

After, you can choose the Web install : [W] for the PHP web log file
(installed in /var/www/html/catlog/index.php)

(Start install or [S] is for my personal use case)

Reboot after the execution of this script

> `sudo reboot`


---
You can, if you have Nextcloud Talk app, add a *channel_id* to have a monitoring bot for the status of the catprinter, to be specified in the configuration files.
For this, opens the discussion where you want your bot to send you notifications via the Nextcloud Talk web application.
Retrieve the channel ID at the end of the discussion URL.
For example, in the following link:

> https://your-nextcloud-instance/index.php/call/ybz3dgu#/

The channel ID is: *ybz3dgu*

---
Be sure to replace the fonts with your own in the code, the fonts must be in the root folder. Like "Lucida_Console_Regular.ttf".


## HTML to image:
> `wkhtmltoimage --width 384 https://example.com /home/your/path/catprinter/test.png`

> `wkhtmltoimage --width 384 --height 500 https://example.com /home/your/path/catprinter/test.png`

## Send image:
> `curl --location -X POST --form 'image=@/home/your/path/catprinter/test.png' --form 'feed="100"' 'localhost:5000'`

## Send text:
> `curl --location -X POST --form 'text="Lorem ipsum."' --form 'font="Peignot.ttf"' --form 'size="48"' --form 'feed="100"' 'localhost:5000'`

## Feed paper:
> `curl --location --request POST --form 'feed="100"' 'localhost:5000'`
---
You can use in Telegram app the following commands:

> `\feed` (to roll out paper)

> `\reboot` (to reboot the system)

> `\shutdown` (to shutdown the system)
---
### Credits
[amber-sixel gb01print](https://github.com/amber-sixel/gb01print)

[xssfox print_server](https://gist.github.com/xssfox/b911e0781a763d258d21262c5fdd2dec)
