![image text](catprinter.jpg "Thermal Cat printer")

# CatPrinter
Driver, Telegram bot &amp; apps for the thermal "cat printer"

---
> `pip install -r requirements.txt`

> `apt install wkhtmltopdf`
---
Be sure to replace the fonts with your own in the code, the fonts must be in the root folder. Like "Lucida_Console_Regular.ttf".

## Start printer driver & server:
> `cd /home/your/path/to/this/folder && python3 -tt print_server.py`
## Start Bot Script:
> `cd /home/your/path/to/app/telegram_bot && python3 bot.py`
## Start Cat_Monitor Script:
> `cd /home/your/path/to/app/monitor && python3 cat_monitor.py`
## Crontab:
> `@reboot cd /home/your/path/catprinter && python3 -tt print_server.py >> /home/your/path/catprinter/app/monitor/start.txt 2>&1`

> `@reboot sh /home/your/path/catprinter/app/monitor/cat_monitor.sh >> /home/your/path/catprinter/app/monitor/cat_monitor.txt 2>&1`

> `@reboot cd /home/your/path/catprinter/app/telegram_bot && sleep 15 && python3 bot.py >> /home/your/path/catprinter/app/monitor/start.txt 2>&1`

> `* * * * * truncate -s 10M  /home/your/path/catprinter/app/monitor/start.txt`

> `* * * * * truncate -s 10M  /home/your/path/catprinter/app/monitor/cat_monitor.txt`
### Sudo Crontab:
> `@reboot cd /home/yourpath/ && ./start_catprinterbot.sh`

### To have a log server in PHP, you can add this code in a .php file to install later for Apache or Nginx:
```
<?php

$log = file_get_contents('/chemin/vers/fichier.log');
$lines = explode("\n", $log);

echo '<!DOCTYPE html>
	<html>
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="height=device-height, width=device-width, initial-scale=1.0, shrink-to-fit=no, user-scalable=no">
		<link rel="icon" type="image/png" href="#">
		<script src="https://cdn.tailwindcss.com"></script>
		<title>Cat Printer Logs</title>
	</head>
	<body style="background-color:lightgrey;">
		<h1 class="text-center text-3xl font-bold underline font-mono">Cat Printer Logs</h1>
		<div style="margin:2%;">
			<pre style="white-space:pre-wrap;">
				<code class="font-mono" style="font-size:12px;background:greenyellow;word-wrap:break-word;">';

foreach ($lines as $line) {
    echo $line.'<br>';
}

echo '			</code>
			</pre>
		</div>
	</body>
</html>';

?>
```

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
