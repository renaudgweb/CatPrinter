#!/usr/bin/env python3
import logging
import os
from datetime import datetime
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from qrcode.image.styles.colormasks import SquareGradiantColorMask
from configparser import ConfigParser

# Load configuration from a file
config = ConfigParser()
config.read('../config/config.ini')

TOKEN = config.get('Telegram_api', 'TELEGRAM_BOT_TOKEN')
HOME_PATH = config.get('Paths', 'HOME_PATH')
OPENWEATHER_API_KEY = config.get('Openweather_api', 'OPENWEATHER_API_KEY')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def play_sound(sound_path):
    """Play sound using aplay."""
    os.system(f"sudo aplay -D hw:0,0 -c 2 -q {sound_path}")


def make_api_request(url):
    """Make API request and return the JSON response."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed. URL: {url}. Error: {e}")
        return None


def save_text_to_file(file_path, content):
    """Save text content to a file."""
    with open(file_path, 'w') as file:
        file.write(content)


def send_image_to_printer(image_path):
    """Send image to the printer using curl."""
    try:
        os.system(f"curl --location -X POST --form 'image=@\"{image_path}\"' 'localhost:5000'")
        print('Image successfully sent to the printer!')

    except Exception as e:
        print(f"An error occurred: {e}")
        print('Failed to send image to the printer.')


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    play_sound(f"{HOME_PATH}/Sound/start.wav")
    update.message.reply_text('🏁️ 😻 MeowwWelcome!\n\nYou can send /help to know what I can do')


def help(update, context):
    """Send a message when the command /help is issued."""
    play_sound(f"{HOME_PATH}/Sound/help.wav")
    update.message.reply_text(
        '📃️ Write me a message.\n\n'
        '🖼️ 📷️ Send me a picture.\n\n'
        '💻️ Send me an URL to print web page.\n\n'
        '\u20BF /btc - to print a Bitcoin paper wallet.\n\n'
        'Ξ /eth - to print a Ethereum paper wallet.\n\n'
        '📉️📈️ /crypto - to print current prices.\n\n'
        '🖥️ /job - to print jobs of the day.\n\n'
        '🚀️ /iss - to know peoples in space.\n\n'
        '🔳️ /qr <text> - to get & print QR-Code.\n\n'
        '🌤️ /meteo <city> - to print weather.\n\n'
        '🛬️🛫️ /weather <ICAO> - to print METAR weather.\n\n'
        '🌌️ /astro <sign> - to print horoscope.\n\n'
        '🔢️ /number <1234> - to print some info about it.\n\n'
        '🗺️ /geo <45.12345 04.12345> - to print address.\n\n'
        '🤖️ /gpt <prompt> - to have a response from OpenAI GPT-3.5 to the given prompt.\n\n'
        '🤖️ /dalle <prompt> - to have an image from OpenAI Dall-e to the given prompt.\n\n'
        'I take care of the 🖨️ 😽️'
    )


def reboot(update, context):
    """Reboot the system"""
    update.message.reply_text('🔃 I reboot the system... 🐈')
    os.system("sudo reboot")


def shutdown(update, context):
    """Shutdown the system"""
    update.message.reply_text('🔌 I shutdown the system... 😿')
    os.system("sudo halt")


def feed(update, context):
    """Roll out some paper of the printer when /feed is issued."""
    play_sound(f"{HOME_PATH}/Sound/feed.wav")
    update.message.reply_text("⬆️ I roll out some paper... 😺️")
    os.system("curl --location -X POST --form 'feed=\"100\"' 'localhost:5000'")
    update.message.reply_text('✅️ Meow! 😻️ /help')


def weather(update, context):
    """Print the airport weather when the command /weather is issued."""
    update.message.reply_text('🛬️🛫️ I print the airport weather... 😺️')
    play_sound(f"{HOME_PATH}/Sound/weather.wav")
    weather = update.message.text
    weather = weather.replace("/weather ", "")
    os.system(f'weather {weather} -qmv | sed "s/;/,/g" > "{HOME_PATH}/app/meteo+/weather.txt"')
    os.system(f"cd {HOME_PATH}/app/meteo+ && ./weather.sh")
    update.message.reply_text('✅️ Meow! 😻️ /help')


def meteo(update, context):
    """Print the city weather when the command /meteo is issued."""
    update.message.reply_text('🌤️ I print the city weather... 😺️')
    play_sound(f"{HOME_PATH}/Sound/meteo.wav")
    city_name = update.message.text
    city_name = city_name.replace("/meteo ", "")
    r = make_api_request(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=fr&units=metric&appid={OPENWEATHER_API_KEY}')

    if r is not None:
        response = r

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

        save_text_to_file(
            f"{HOME_PATH}/app/meteo+/meteo.txt",
            f"Ciel: {desc}\n"
            f"Température: {temp}°c\n"
            f"Ressentie: {temp_feels}°c\n"
            f"Minimale: {temp_min}°c\n"
            f"Maximale: {temp_max}°c\n"
            f"Pression: {pres}hPa\n"
            f"Humidité: {hum}%\n"
            f"Visibilité: {vis}m\n"
            f"Vent: {wind_speed}m/s, {wind_dir}°\n"
            f"Nuages: {clouds}%\n"
            f"Levé: {sunrise_date}\n"
            f"Couché: {sunset_date}\n\n"
            f"Ville: {city}\n"
            f"{date}"
        )

        os.system(f'wget -P {HOME_PATH}/app/meteo+ https://openweathermap.org/img/wn/{icon}@4x.png')
        os.system(f'mv {HOME_PATH}/app/meteo+/{icon}@4x.png {HOME_PATH}/app/meteo+/icon.png')
        os.system(f"cd {HOME_PATH}/app/meteo+ && ./meteo.sh")
        send_image_to_printer(f"{HOME_PATH}/app/meteo+/icon.png")
        update.message.reply_text('✅️ Meow! 😻️ /help')
    else:
        update.message.reply_text('❌️ Meow? 😼️ /help')


def job(update, context):
    """Send a message and print the jobs when the command /meteo is issued."""
    update.message.reply_text('🖥️ I print the jobs... 😺️')
    play_sound(f"{HOME_PATH}/Sound/job.wav")
    os.system(f"cd {HOME_PATH}/app/job && ./job.sh")
    update.message.reply_text('✅️ Meow! 😻️ /help')


def text(update, context):
    """Print the user message."""
    update.message.reply_text("📃️ I print what you wrote... 😺️")
    play_sound(f"{HOME_PATH}/Sound/message.wav")
    f = open(f"{HOME_PATH}/app/message/message.txt", "w")
    msg = update.message.text
    f.write(msg.replace(";", ","))
    f.close()
    os.system(f"cd {HOME_PATH}/app/message && ./message.sh")
    update.message.reply_text('✅️ Meow! 😻️ /help')


def image(update, context):
    """Print the user image."""
    update.message.reply_text("🖼️📷️ I print it right away... 😺️")
    play_sound(f"{HOME_PATH}/Sound/photo.wav")

    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    obj.download(custom_path=f'{HOME_PATH}/app/telegram_bot/file.jpg')

    send_image_to_printer(f"{HOME_PATH}/app/telegram_bot/file.jpg")
    update.message.reply_text('✅️ Meow! 😻️ /help')


def regex(update, context):
    """Print the user URL."""
    update.message.reply_text('💻️ I print this page right away... 😺️')
    play_sound(f"{HOME_PATH}/Sound/url.wav")
    os.system(f'wkhtmltoimage --width 384 "{update.message.text}" "{HOME_PATH}/app/web_print/test.png"')
    send_image_to_printer(f"{HOME_PATH}/app/web_print/test.png")
    update.message.reply_text('✅️ Meow! 😻️ /help')


def iss(update, context):
    """Return and print the astronauts name when the command /iss is issued."""
    update.message.reply_text('🚀️ I print astronauts names right away... 😺️')
    play_sound(f"{HOME_PATH}/Sound/iss.wav")
    r = make_api_request("http://api.open-notify.org/astros.json")
    if r is not None:
        astros = r
        people = astros['people']

        people_in_space = []
        for d in people:
            people_in_space.append(f'{d["name"]} ({d["craft"]})\n')

        iss_info = "There are currently {} astronauts in orbit:\n{}.".format(astros['number'], ''.join(people_in_space))
        payload = {'text': iss_info[:-1], 'size': '24', 'feed': '100'}
        requests.post('http://localhost:5000', data=payload)
        update.message.reply_text('✅️ Meow! 😻️ /help')
    else:
        update.message.reply_text('❌️ Meow? 😼️ /help')


def number(update, context):
    """Return and print the number info when the command /number is issued."""
    update.message.reply_text('🔢️ I print number informations right away... 😺️')
    play_sound(f"{HOME_PATH}/Sound/number.wav")
    number = update.message.text
    number = number.replace("/number ", "")

    r = make_api_request(f'http://numbersapi.com/{number}/trivia?json')

    if r is not None:
        number_res = r['text']

        os.system(f'curl --location -X POST --form \'text="{number_res}"\' --form \'feed="100"\' \'localhost:5000\'')
        update.message.reply_text('✅️ Meow! 😻️ /help')
    else:
        update.message.reply_text('❌️ Meow? 😼️ /help')


def geo(update, context):
    """Return and print the address of coordonates when the command /geo is issued."""
    update.message.reply_text('🗺️ I print the address right away... 😺️')
    play_sound(f"{HOME_PATH}/Sound/geo.wav")
    geo = update.message.text
    geo = geo.replace("/geo ", "")
    lat = geo[0:8]
    lon = geo[9:21]

    r = make_api_request(f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json')

    if r is not None:
        location = r['display_name']

        os.system(f'curl --location -X POST --form \'text="{location}"\' --form \'size="24"\' --form \'feed="100"\' \'localhost:5000\'')
        update.message.reply_text('✅️ Meow! 😻️ /help')
    else:
        update.message.reply_text('❌️ Meow? 😼️ /help')


def qr(update, context):
    """Return and print the QR Code when the command /qr is issued."""
    update.message.reply_text('🔳️ I print the QR-Code right away... 😺️')
    play_sound(f"{HOME_PATH}/Sound/qrcode.wav")
    code = update.message.text
    code = code.replace("/qr ", "")
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(code)

    img_1 = qr.make_image(
        back_color=(255, 195, 235),
        fill_color=(55, 95, 35),
        image_factory=StyledPilImage,
        module_drawer=CircleModuleDrawer(),
        color_mask=SquareGradiantColorMask()
    )
    img_2 = qr.make_image(image_factory=StyledPilImage)
    type(img_1)
    type(img_2)
    img_1.save(f'{HOME_PATH}/app/telegram_bot/qrcode1.png')
    img_2.save(f'{HOME_PATH}/app/telegram_bot/qrcode.png')
    send_image_to_printer(f"{HOME_PATH}/app/telegram_bot/qrcode.png")
    os.system(f'curl --location -X POST --form "text={code}" --form "size=24" --form "feed=100" "localhost:5000"')
    update.message.reply_photo(open(f'{HOME_PATH}/app/telegram_bot/qrcode1.png', 'rb'))
    update.message.reply_text('✅️ Meow! 😻️ /help')


def astro(update, context):
    """Print the astro when the command /astro is issued."""
    update.message.reply_text('🌌️ I print the horoscope right away... 😺️')
    play_sound(f"{HOME_PATH}/Sound/astro.wav")
    sign = update.message.text
    sign = sign.replace("/astro ", "")
    r = requests.post(f'https://aztro.sameerkumar.website/?sign={sign}&day=today')

    if r is not None:
        response = r

        dt = response['current_date']
        compat = response['compatibility']
        lucky_time = response['lucky_time']
        lucky_num = response['lucky_number']
        color = response['color']
        dt_range = response['date_range']
        mood = response['mood']
        desc = response['description']

        save_text_to_file(
            f'{HOME_PATH}/app/astro/astro.txt',
            (f'{dt}\n\n"{desc}"\n\n{dt_range}\nCompatibility: {compat}\n'
             f'Lucky time: {lucky_time}\nLucky number: {lucky_num}\n'
             f'Color: {color}\nMood: {mood}')
        )

        os.system(f'cd {HOME_PATH}/app/astro && ./astro.sh')
        update.message.reply_text('✅️ Meow! 😻️ /help')

    else:
        update.message.reply_text('❌️ Meow? 😼️ /help')


def crypto(update, context):
    """Return and print the crypto prices when the command /crypto is issued."""
    update.message.reply_text('📉️📈️ I print current prices right away... 😺️')
    play_sound(f"{HOME_PATH}/Sound/btc.wav")
    r = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={
            'ids': 'bitcoin,ethereum,basic-attention-token,solana,cardano,terra-luna,avalanche-2,polkadot,aave,swissborg',
            'vs_currencies': 'eur,usd',
            'include_last_updated_at': 'true'
        }
    )

    if r.status_code == 200:
        cryptos = r.json()

        btc = cryptos['bitcoin']
        btc_eur = btc['eur']
        btc_usd = btc['usd']
        btc_stp = btc['last_updated_at']
        btc_dt = datetime.fromtimestamp(btc_stp)
        btc_time = btc_dt.strftime("%H:%M:%S")

        eth = cryptos['ethereum']
        eth_eur = eth['eur']
        eth_usd = eth['usd']
        eth_stp = eth['last_updated_at']
        eth_dt = datetime.fromtimestamp(eth_stp)
        eth_time = eth_dt.strftime("%H:%M:%S")

        bat = cryptos['basic-attention-token']
        bat_eur = bat['eur']
        bat_usd = bat['usd']
        bat_stp = bat['last_updated_at']
        bat_dt = datetime.fromtimestamp(bat_stp)
        bat_time = bat_dt.strftime("%H:%M:%S")

        sol = cryptos['solana']
        sol_eur = sol['eur']
        sol_usd = sol['usd']
        sol_stp = sol['last_updated_at']
        sol_dt = datetime.fromtimestamp(sol_stp)
        sol_time = sol_dt.strftime("%H:%M:%S")

        ada = cryptos['cardano']
        ada_eur = ada['eur']
        ada_usd = ada['usd']
        ada_stp = ada['last_updated_at']
        ada_dt = datetime.fromtimestamp(ada_stp)
        ada_time = ada_dt.strftime("%H:%M:%S")

        luna = cryptos['terra-luna']
        luna_eur = luna['eur']
        luna_usd = luna['usd']
        luna_stp = luna['last_updated_at']
        luna_dt = datetime.fromtimestamp(luna_stp)
        luna_time = luna_dt.strftime("%H:%M:%S")

        avax = cryptos['avalanche-2']
        avax_eur = avax['eur']
        avax_usd = avax['usd']
        avax_stp = avax['last_updated_at']
        avax_dt = datetime.fromtimestamp(avax_stp)
        avax_time = avax_dt.strftime("%H:%M:%S")

        dot = cryptos['polkadot']
        dot_eur = dot['eur']
        dot_usd = dot['usd']
        dot_stp = dot['last_updated_at']
        dot_dt = datetime.fromtimestamp(dot_stp)
        dot_time = dot_dt.strftime("%H:%M:%S")

        aave = cryptos['aave']
        aave_eur = aave['eur']
        aave_usd = aave['usd']
        aave_stp = aave['last_updated_at']
        aave_dt = datetime.fromtimestamp(aave_stp)
        aave_time = aave_dt.strftime("%H:%M:%S")

        chsb = cryptos['swissborg']
        chsb_eur = chsb['eur']
        chsb_usd = chsb['usd']
        chsb_stp = chsb['last_updated_at']
        chsb_dt = datetime.fromtimestamp(chsb_stp)
        chsb_time = chsb_dt.strftime("%H:%M:%S")

        dt = datetime.fromtimestamp(btc_stp)
        date = dt.strftime("%d/%m/%y")
        crypto_info = (
            f"Coingecko.com {date}\n\n--------------------\n"
            f"Bitcoin (BTC):\n{btc_eur} EUR\n{btc_usd} USD\n{btc_time}\n"
            f"--------------------\n"
            f"Ethereum (ETH):\n{eth_eur} EUR\n{eth_usd} USD\n{eth_time}\n"
            f"--------------------\n"
            f"Basic Attention Token (BAT):\n{bat_eur} EUR\n{bat_usd} USD\n{bat_time}\n"
            f"--------------------\n"
            f"Solana (SOL):\n{sol_eur} EUR\n{sol_usd} USD\n{sol_time}\n"
            f"--------------------\n"
            f"Cardano (ADA):\n{ada_eur} EUR\n{ada_usd} USD\n{ada_time}\n"
            f"--------------------\n"
            f"Terra-Luna (LUNA):\n{luna_eur} EUR\n{luna_usd} USD\n{luna_time}\n"
            f"--------------------\n"
            f"Avalanche (AVAX):\n{avax_eur} EUR\n{avax_usd} USD\n{avax_time}\n"
            f"--------------------\n"
            f"Polkadot (DOT):\n{dot_eur} EUR\n{dot_usd} USD\n{dot_time}\n"
            f"--------------------\n"
            f"Aave (AAVE):\n{aave_eur} EUR\n{aave_usd} USD\n{aave_time}\n"
            f"--------------------\n"
            f"SwissBorg (CHSB):\n{chsb_eur} EUR\n{chsb_usd} USD\n{chsb_time}\n"
            f"--------------------"
        )

        os.system(f'curl --location -X POST --form \'text="{crypto_info}"\' --form \'size="24"\' --form \'feed="100"\' \'localhost:5000\'')
        update.message.reply_text('✅️ Meow! 😻️ /help')
        update.message.reply_text('🚀️🌙️ TO THE MOON ! 😻️')
    else:
        update.message.reply_text('❌️ Meow? 😼️ /help')


def BTC_paper_wallet(update, context):
    """Print a new Bitcoin paper wallet when the command /btc is issued"""
    update.message.reply_text('I print the \u20BF paper wallet right away... 😺️')
    play_sound(f"{HOME_PATH}/Sound/btc.wav")
    os.system(f"cd {HOME_PATH}/app/btc_paper_wallet && ./btcpaperwallet.sh")
    update.message.reply_text('✅️ Meow! 😻️ /help')
    update.message.reply_text('⚠️⚠️ DO NOT LOSE OR SHARE YOUR PRIVATE KEY ! ⚠️⚠️')


def ETH_paper_wallet(update, context):
    """Print a new Ethereum paper wallet when the command /eth is issued"""
    update.message.reply_text('I print the Ξ paper wallet right away... 😺️')
    play_sound(f"{HOME_PATH}/Sound/btc.wav")
    os.system(f"cd {HOME_PATH}/app/eth_paper_wallet && ./ethpaperwallet.sh")
    update.message.reply_text('✅️ Meow! 😻️ /help')
    update.message.reply_text('⚠️⚠️ DO NOT LOSE OR SHARE YOUR PRIVATE KEY ! ⚠️⚠️')


def GPT(update, context):
    """Print the response from GPT-3.5 to the given prompt"""
    update.message.reply_text('🤖️💬️ I print the response... 😺️')
    play_sound(f"{HOME_PATH}/Sound/message.wav")
    gpt = update.message.text
    gpt = gpt.replace("/gpt ", "")
    os.system(f'cd "{HOME_PATH}/app/gpt" && python3 gpt.py "{gpt}"')
    os.system(f'cd "{HOME_PATH}/app/gpt" && ./gpt.sh')
    update.message.reply_text('✅️ Meow! 😻️ /help')


def Dall_e(update, context):
    """Print the image from Dall-e to the given prompt"""
    update.message.reply_text('🤖️🖼️ I print the image... 😺️')
    play_sound(f"{HOME_PATH}/Sound/photo.wav")
    dalle = update.message.text
    dalle = dalle.replace("/dalle ", "")
    os.system(f'cd "{HOME_PATH}/app/dall_e" && python3 dalle.py "{dalle}"')
    os.system(f'cd "{HOME_PATH}/app/dall_e" && ./dalle.sh')
    update.message.reply_photo(open(HOME_PATH + "/app/dall_e/dalle.png", "rb"))
    update.message.reply_text('✅️ Meow! 😻️ /help')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning(f'Erreur lors de la mise à jour de "{update}". Erreur rencontrée : "{context.error}"')
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
    dp.add_handler(CommandHandler("reboot", reboot))
    dp.add_handler(CommandHandler("shutdown", shutdown))
    dp.add_handler(CommandHandler("weather", weather))
    dp.add_handler(CommandHandler("meteo", meteo))
    dp.add_handler(CommandHandler("job", job))
    dp.add_handler(CommandHandler("iss", iss))
    dp.add_handler(CommandHandler("number", number))
    dp.add_handler(CommandHandler("geo", geo))
    dp.add_handler(CommandHandler("qr", qr))
    dp.add_handler(CommandHandler("astro", astro))
    dp.add_handler(CommandHandler("btc", BTC_paper_wallet))
    dp.add_handler(CommandHandler("eth", ETH_paper_wallet))
    dp.add_handler(CommandHandler("crypto", crypto))
    dp.add_handler(CommandHandler("gpt", GPT))
    dp.add_handler(CommandHandler("dalle", Dall_e))

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
