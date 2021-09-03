import logging
import requests
import os
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = 'YOURTOKEN'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('😻️ Meow!\nyou can send /help to get some functions')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('You can:\n- write me a message.\n- Send me a picture.\n- Send me an URL to print web page.\n- Send /meteo city to get weather.\n- Send /weather ICAO to get METAR weather.\n- Send /job to get jobs of the day.\n- Send /iss to know peoples in space.\n- Send /number 1234 to get some info about it.\n- Send /geo 45.12345 04.12345 to get adresse.\nI take care of the printing 😽️')

def feed(update, context):
    """Roll out some paper of the printer when /feed is issued."""
    update.message.reply_text("I roll out some paper 😺️")
    os.system("curl --location -X POST --form 'feed=\"100\"' 'localhost:5000'")

def weather(update, context):
    """Print the airport weather when the command /weather is issued."""
    update.message.reply_text('I print the airport weather 😺️')
    weather = update.message.text
    weather = weather.replace("/weather ", "")
    os.system("weather " + weather + " -qmv | sed 's/\;/\,/g' > /home/your/path/catprinter/app/meteo+/weather.txt")
    os.system("cd /home/your/path/catprinter/app/meteo+ && ./weather.sh")
    update.message.reply_text('done! 😻️ /help')

def meteo(update, context):
    """Print the city weather when the command /meteo is issued."""
    update.message.reply_text('I print the city weather 😺️')
    city_name = update.message.text
    city_name = city_name.replace("/meteo ", "")
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+city_name+'&lang=fr&units=metric&appid=API-openweather-TOKEN')
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

    f = open("/home/your/path/catprinter/app/meteo+/meteo.txt", "w")
    f.write(f"Ciel: {desc}\nTempérature: {temp}°c\nRessentie: {temp_feels}°c\nMinimale: {temp_min}°c\nMaximale: {temp_max}°c\nPression: {pres}hPa\nHumidité: {hum}%\nVisibilité: {vis}m\nVent: {wind_speed}m/s, {wind_dir}°\nNuages: {clouds}%\nLevé: {sunrise_date}\nCouché: {sunset_date}\n\nVille: {city}\n{date}")
    f.close()

    os.system('wget -P /home/your/path/catprinter/app/meteo+ https://openweathermap.org/img/wn/'+icon+'@2x.png')
    os.system('mv /home/your/path/catprinter/app/meteo+/'+icon+'@2x.png /home/your/path/catprinter/app/meteo+/icon.png')
    os.system("cd /home/your/path/catprinter/app/meteo+ && ./meteo.sh")
    os.system("curl --location -X POST --form 'image=@\"/home/your/path/catprinter/app/meteo+/icon.png\"' --form 'feed=\"100\"' 'localhost:5000'")
    update.message.reply_text('done! 😻️ /help')

def job(update, context):
    """Send a message and print the jobs when the command /meteo is issued."""
    update.message.reply_text('I print the jobs 😺️')
    os.system("cd /home/your/path/catprinter/app/job && ./job.sh")
    update.message.reply_text('done! 😻️ /help')

def echo_text(update, context):
    """Echo and print the user message."""
    update.message.reply_text("I print what you wrote 😺️")
    f = open("/home/your/path/catprinter/app/message/message.txt", "w")
    msg = update.message.text
    f.write(msg.replace(";", ","))
    f.close()
    os.system("cd /home/your/path/catprinter/app/message && ./message.sh")
    update.message.reply_text('done! 😻️ /help')

def echo_image(update, context):
    """Print the user image."""
    update.message.reply_text("I print it right away 😺️")

    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    obj.download(custom_path="/home/your/path/catprinter/app/telegram_bot/file.jpg")

    os.system("curl --location -X POST --form 'image=@\"/home/your/path/catprinter/app/telegram_bot/file.jpg\"' --form 'feed=\"100\"' 'localhost:5000'")
    update.message.reply_text('done! 😻️ /help')

def regex(update, context):
    """Print the user URL."""
    update.message.reply_text('I print this page right away 😺️')
    os.system("wkhtmltoimage --width 384 " + update.message.text + " /home/your/path/catprinter/app/web_print/test.png")
    os.system("curl --location -X POST --form 'image=@/home/your/path/catprinter/app/web_print/test.png' --form 'feed=\"100\"' 'localhost:5000'")
    update.message.reply_text('done! 😻️ /help')

def iss(update, context):
    """Return and print the astronauts name when the command /iss is issued."""
    update.message.reply_text('I print astronaut names right away 😺️')
    r = requests.get("http://api.open-notify.org/astros.json")
    astros = r.json()
    people = astros['people']

    people_in_space = []
    for d in people:
        people_in_space.append(d['name'])

    iss_info =  f"Il y a {astros['number']} astronautes en orbite: {', '.join(people_in_space)}."
    os.system("curl --location -X POST --form 'text=\"" + iss_info + "\"' --form 'size=\"24\"' --form 'feed=\"100\"' 'localhost:5000'")
    update.message.reply_text('done! 😻️ /help')

def number(update, context):
    """Return and print the number info when the command /number is issued."""
    update.message.reply_text('I print number informations right away 😺️')
    number = update.message.text
    number = number.replace("/number ", "")

    r = requests.get('http://numbersapi.com/'+number+'/trivia?json')
    response = r.json()
    number_res = response['text']

    os.system("curl --location -X POST --form 'text=\"" + number_res + "\"' --form 'font=\"ocr_b.ttf\"' --form 'size=\"24\"' --form 'feed=\"100\"' 'localhost:5000'")
    update.message.reply_text('done! 😻️ /help')

def geo(update, context):
    """Return and print the adresse of coordonates when the command /geo is issued."""
    update.message.reply_text('I print the adresse right away 😺️')
    geo = update.message.text
    geo = geo.replace("/geo ", "")
    lat = geo[0:8]
    lon = geo[9:21]

    r = requests.get('https://nominatim.openstreetmap.org/reverse?lat='+lat+'&lon='+lon+'&format=json')
    response = r.json()
    location = response['display_name']

    os.system("curl --location -X POST --form 'text=\"" + location + "\"' --form 'size=\"24\"' --form 'feed=\"100\"' 'localhost:5000'")
    update.message.reply_text('done! 😻️ /help')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text('meow? /help')

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

    dp.add_handler(MessageHandler(Filters.regex('https://') | Filters.regex('http://'), regex))
    dp.add_handler(MessageHandler(Filters.text, echo_text))
    dp.add_handler(MessageHandler(Filters.photo, echo_image))

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
