#!/usr/bin/env python3
import logging
import requests
import os
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from qrcode.image.styles.colormasks import SquareGradiantColorMask

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = 'YOURTOKEN'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    os.system("sudo aplay -D hw:0,0 -c 2 -q /home/your/path/Musique/bruitages/catprinterbot/start.wav")
    update.message.reply_text('🏁️ 😻 MeowwWelcome!\n\nYou can send /help to know what I can do')

def help(update, context):
    """Send a message when the command /help is issued."""
    os.system("sudo aplay -D hw:0,0 -c 2 -q /home/your/path/Musique/bruitages/catprinterbot/help.wav")
    update.message.reply_text('📃️ Write me a message.\n\n🖼️ 📷️ Send me a picture.\n\n💻️ Send me an URL to print web page.\n\n🔳️ /qr <text> - to get & print QR-Code.\n\n🌤️ /meteo <city> - to print weather.\n\n🛬️🛫️ /weather <ICAO> - to print METAR weather.\n\n🖥️ /job - to print jobs of the day.\n\n🚀️ /iss - to know peoples in space.\n\n🌌️ /astro <sign> - to print horoscope.\n\n🔢️ /number <1234> - to print some info about it.\n\n🗺️ /geo <45.12345 04.12345> - to print address.\n\nI take care of the 🖨️ 😽️')

def feed(update, context):
    """Roll out some paper of the printer when /feed is issued."""
    os.system("sudo aplay -D hw:0,0 -c 2 -q /home/your/path/Musique/bruitages/catprinterbot/feed.wav")
    update.message.reply_text("⬆️ I roll out some paper... 😺️")
    os.system("curl --location -X POST --form 'feed=\"100\"' 'localhost:5000'")
    update.message.reply_text('✅️ Meow! 😻️ /help')

def weather(update, context):
    """Print the airport weather when the command /weather is issued."""
    update.message.reply_text('🛬️🛫️ I print the airport weather... 😺️')
    os.system("sudo aplay -D hw:0,0 -c 2 -q /home/your/path/Musique/bruitages/catprinterbot/weather.wav")
    weather = update.message.text
    weather = weather.replace("/weather ", "")
    os.system("weather " + weather + " -qmv | sed 's/\;/\,/g' > /home/your/path/Documents/catprinter/app/meteo+/weather.txt")
    os.system("cd /home/your/path/Documents/catprinter/app/meteo+ && ./weather.sh")
    update.message.reply_text('✅️ Meow! 😻️ /help')

def meteo(update, context):
    """Print the city weather when the command /meteo is issued."""
    update.message.reply_text('🌤️ I print the city weather... 😺️')
    os.system("sudo aplay -D hw:0,0 -c 2 -q /home/your/path/Musique/bruitages/catprinterbot/meteo.wav")
    city_name = update.message.text
    city_name = city_name.replace("/meteo ", "")
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+city_name+'&lang=fr&units=metric&appid=API-openweather-TOKEN')

    if r.status_code == 200:

        response = r.json()

        desc = response['weather'][0]['description']
        icon = response['weather'][0]['icon']
        temp = response['main']['temp']
        temp_feels = response['main']['feels_like']
        temp_min = response['main']['temp_min']
        temp_max = response['main']['temp_max']
        pres = response['main']['pressure']
        hum = response['main']['humidity']
        vis = response['visibility']
        wind_speed = response['wind']['speed']
        wind_dir = response['wind']['deg']
        clouds = response['clouds']['all']

        dt = response['dt']
        dt = datetime.fromtimestamp(dt)
        date = dt.strftime("%a %d %b %Y, %H:%M:%S")
        sunrise = response['sys']['sunrise']
        sunrise = datetime.fromtimestamp(sunrise)
        sunrise_date = sunrise.strftime("%H:%M")
        sunset = response['sys']['sunset']
        sunset = datetime.fromtimestamp(sunset)
        sunset_date = sunset.strftime("%H:%M")

        city = response['name']

        f = open("/home/your/path/Documents/catprinter/app/meteo+/meteo.txt", "w")
        f.write(f"Ciel: {desc}\nTempérature: {temp}°c\nRessentie: {temp_feels}°c\nMinimale: {temp_min}°c\nMaximale: {temp_max}°c\nPression: {pres}hPa\nHumidité: {hum}%\nVisibilité: {vis}m\nVent: {wind_speed}m/s, {wind_dir}°\nNuages: {clouds}%\nLevé: {sunrise_date}\nCouché: {sunset_date}\n\nVille: {city}\n{date}")
        f.close()

        os.system('wget -P /home/your/path/Documents/catprinter/app/meteo+ https://openweathermap.org/img/wn/'+icon+'@4x.png')
        os.system('mv /home/your/path/Documents/catprinter/app/meteo+/'+icon+'@4x.png /home/your/path/Documents/catprinter/app/meteo+/icon.png')
        os.system("cd /home/your/path/Documents/catprinter/app/meteo+ && ./meteo.sh")
        os.system("curl --location -X POST --form 'image=@\"/home/your/path/Documents/catprinter/app/meteo+/icon.png\"' --form 'feed=\"100\"' 'localhost:5000'")
        update.message.reply_text('✅️ Meow! 😻️ /help')

    else:
        update.message.reply_text('❌️ Meow? 😼️ /help')

def job(update, context):
    """Send a message and print the jobs when the command /meteo is issued."""
    update.message.reply_text('🖥️ I print the jobs... 😺️')
    os.system("sudo aplay -D hw:0,0 -c 2 -q /home/your/path/Musique/bruitages/catprinterbot/job.wav")
    os.system("cd /home/your/path/Documents/catprinter/app/job && ./job.sh")
    update.message.reply_text('✅️ Meow! 😻️ /help')

def text(update, context):
    """Print the user message."""
    update.message.reply_text("📃️ I print what you wrote... 😺️")
    os.system("sudo aplay -D hw:0,0 -c 2 -q /home/your/path/Musique/bruitages/catprinterbot/message.wav")
    f = open("/home/your/path/Documents/catprinter/app/message/message.txt", "w")
    msg = update.message.text
    f.write(msg.replace(";", ","))
    f.close()
    os.system("cd /home/your/path/Documents/catprinter/app/message && ./message.sh")
    update.message.reply_text('✅️ Meow! 😻️ /help')

def image(update, context):
    """Print the user image."""
    update.message.reply_text("🖼️📷️ I print it right away... 😺️")
    os.system("sudo aplay -D hw:0,0 -c 2 -q /home/your/path/Musique/bruitages/catprinterbot/photo.wav")

    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    obj.download(custom_path="/home/your/path/Documents/catprinter/app/telegram_bot/file.jpg")

    os.system("curl --location -X POST --form 'image=@\"/home/your/path/Documents/catprinter/app/telegram_bot/file.jpg\"' --form 'feed=\"100\"' 'localhost:5000'")
    update.message.reply_text('✅️ Meow! 😻️ /help')

def regex(update, context):
    """Print the user URL."""
    update.message.reply_text('💻️ I print this page right away... 😺️')
    os.system("sudo aplay -D hw:0,0 -c 2 -q /home/your/path/Musique/bruitages/catprinterbot/url.wav")
    os.system("wkhtmltoimage --width 384 " + update.message.text + " /home/your/path/Documents/catprinter/app/web_print/test.png")
    os.system("curl --location -X POST --form 'image=@/home/your/path/Documents/catprinter/app/web_print/test.png' --form 'feed=\"100\"' 'localhost:5000'")
    update.message.reply_text('✅️ Meow! 😻️ /help')

def iss(update, context):
    """Return and print the astronauts name when the command /iss is issued."""
    update.message.reply_text('🚀️ I print astronauts names right away... 😺️')
    os.system("sudo aplay -D hw:0,0 -c 2 -q /home/your/path/Musique/bruitages/catprinterbot/iss.wav")
    r = requests.get("http://api.open-notify.org/astros.json")
    astros = r.json()
    people = astros['people']

    people_in_space = []
    for d in people:
        people_in_space.append(d['name']+" (")
        people_in_space.append(d['craft']+")\n")

    iss_info =  f"There are currently {astros['number']} astronauts in orbit:\n{''.join(people_in_space)}."
    os.system("curl --location -X POST --form 'text=\"" + iss_info[:-1] + "\"' --form 'size=\"24\"' --form 'feed=\"100\"' 'localhost:5000'")
    update.message.reply_text('✅️ Meow! 😻️ /help')

def number(update, context):
    """Return and print the number info when the command /number is issued."""
    update.message.reply_text('🔢️ I print number informations right away... 😺️')
    os.system("sudo aplay -D hw:0,0 -c 2 -q /home/your/path/Musique/bruitages/catprinterbot/number.wav")
    number = update.message.text
    number = number.replace("/number ", "")

    r = requests.get('http://numbersapi.com/'+number+'/trivia?json')

    if r.status_code == 200:

        response = r.json()
        number_res = response['text']

        os.system("curl --location -X POST --form 'text=\"" + number_res + "\"' --form 'font=\"ocr_b.ttf\"' --form 'size=\"24\"' --form 'feed=\"100\"' 'localhost:5000'")
        update.message.reply_text('✅️ Meow! 😻️ /help')

    else:
        update.message.reply_text('❌️ Meow? 😼️ /help')

def geo(update, context):
    """Return and print the address of coordonates when the command /geo is issued."""
    update.message.reply_text('🗺️ I print the address right away... 😺️')
    os.system("sudo aplay -D hw:0,0 -c 2 -q /home/your/path/Musique/bruitages/catprinterbot/geo.wav")
    geo = update.message.text
    geo = geo.replace("/geo ", "")
    lat = geo[0:8]
    lon = geo[9:21]

    r = requests.get('https://nominatim.openstreetmap.org/reverse?lat='+lat+'&lon='+lon+'&format=json')

    if r.status_code == 200:

        response = r.json()
        location = response['display_name']

        os.system("curl --location -X POST --form 'text=\"" + location + "\"' --form 'size=\"24\"' --form 'feed=\"100\"' 'localhost:5000'")
        update.message.reply_text('✅️ Meow! 😻️ /help')

    else:
        update.message.reply_text('❌️ Meow? 😼️ /help')

def qr(update, context):
    """Return and print the QR Code when the command /qr is issued."""
    update.message.reply_text('🔳️ I print the QR-Code right away... 😺️')
    os.system("sudo aplay -D hw:0,0 -c 2 -q /home/your/path/Musique/bruitages/catprinterbot/qrcode.wav")
    code = update.message.text
    code = code.replace("/qr ", "")
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(code)

    img_1 = qr.make_image(back_color=(255, 195, 235), fill_color=(55, 95, 35), image_factory=StyledPilImage, module_drawer=CircleModuleDrawer(), color_mask=SquareGradiantColorMask())
    img_2 = qr.make_image(image_factory=StyledPilImage)
    type(img_1)
    type(img_2)
    img_1.save("/home/your/path/Documents/catprinter/app/telegram_bot/qrcode1.png")
    img_2.save("/home/your/path/Documents/catprinter/app/telegram_bot/qrcode.png")
    os.system("curl --location -X POST --form 'image=@\"/home/your/path/Documents/catprinter/app/telegram_bot/qrcode.png\"' 'localhost:5000'")
    os.system("curl --location -X POST --form 'text=\"" + code + "\"' --form 'size=\"24\"' --form 'feed=\"100\"' 'localhost:5000'")
    update.message.reply_photo(open("/home/your/path/Documents/catprinter/app/telegram_bot/qrcode1.png", "rb"))
    update.message.reply_text('✅️ Meow! 😻️ /help')

def astro(update, context):
    """Print the astro when the command /astro is issued."""
    update.message.reply_text('🌌️ I print the horoscope right away... 😺️')
    os.system("sudo aplay -D hw:0,0 -c 2 -q /home/your/path/Musique/bruitages/catprinterbot/astro.wav")
    sign = update.message.text
    sign = sign.replace("/astro ", "")
    r = requests.post('https://aztro.sameerkumar.website/?sign='+sign+'&day=today')

    if r.status_code == 200:

        response = r.json()

        dt = response['current_date']
        compat = response['compatibility']
        lucky_time = response['lucky_time']
        lucky_num = response['lucky_number']
        color = response['color']
        dt_range = response['date_range']
        mood = response['mood']
        desc = response['description']

        f = open("/home/your/path/Documents/catprinter/app/astro/astro.txt", "w")
        f.write(f'{dt}\n\n"{desc}"\n\n{dt_range}\nCompatibility: {compat}\nLucky time: {lucky_time}\nLucky number: {lucky_num}\nColor: {color}\nMood: {mood}')
        f.close()

        os.system("cd /home/your/path/Documents/catprinter/app/astro && ./astro.sh")
        update.message.reply_text('✅️ Meow! 😻️ /help')

    else:
        update.message.reply_text('❌️ Meow? 😼️ /help')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text('❌️ Meow? 😼️ /help')

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("feed", feed))
    dp.add_handler(CommandHandler("weather", weather))
    dp.add_handler(CommandHandler("meteo", meteo))
    dp.add_handler(CommandHandler("job", job))
    dp.add_handler(CommandHandler("iss", iss))
    dp.add_handler(CommandHandler("number", number))
    dp.add_handler(CommandHandler("geo", geo))
    dp.add_handler(CommandHandler("qr", qr))
    dp.add_handler(CommandHandler("astro", astro))

    dp.add_handler(MessageHandler(Filters.regex('https://') | Filters.regex('http://'), regex))
    dp.add_handler(MessageHandler(Filters.text, text))
    dp.add_handler(MessageHandler(Filters.photo, image))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
