import logging
import os
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
    update.message.reply_text('You can:\n- write me a message.\n- Send me a picture.\n- Send /meteo to print actual weather.\n- Send /job to get jobs of the day.\n- Send URL to print web page.\nI take care of the printing 😽️')

def meteo(update, context):
    """Send a message and print the weather when the command /meteo is issued."""
    update.message.reply_text('I print the weather 😺️')
    os.system("cd /home/your/path/catprinter/app/meteo+ && ./meteo.sh")

def job(update, context):
    """Send a message and print the jobs when the command /meteo is issued."""
    update.message.reply_text('I print the jobs 😺️')
    os.system("cd /home/your/path/catprinter/app/job && ./job.sh")

def echo_text(update, context):
    """Echo and print the user message."""
    update.message.reply_text("I print what you wrote 😺️")
    os.system("curl --location -X POST --form 'text=\"" + update.message.text + "\"' --form 'feed=\"100\"' 'localhost:5000'")

def echo_image(update, context):
    """Print the user image."""
    update.message.reply_text("I print it right away 😺️")

    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    obj.download(custom_path="/home/your/path/catprinter/app/telegram_bot/file.jpg")

    os.system("curl --location -X POST --form 'image=@\"/home/your/path/catprinter/app/telegram_bot/file.jpg\"' --form 'feed=\"100\"' 'localhost:5000'")

def regex(update, context):
    """Print the user URL."""
    update.message.reply_text('I print this page right away 😺️')
    os.system("wkhtmltoimage --width 384 " + update.message.text + " /home/your/path/catprinter/app/web_print/test.png")
    os.system("curl --location -X POST --form 'image=@/home/your/path/catprinter/app/web_print/test.png' --form 'feed=\"100\"' 'localhost:5000'")

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

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
    dp.add_handler(CommandHandler("meteo", meteo))
    dp.add_handler(CommandHandler("job", job))

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
