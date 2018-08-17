#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import traceback
import requests
from tkn import TKN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    try:
        if 'clips.twitch.tv/' in update.message.text:
            print('twitch clip')
            update.message.reply_text('twitch clip!')
        else:
            subprocess.check_call(['/home/wmw/app/youtubeuploader/upload.sh', update.message.text])
    except Exception as e:
        print(e.__doc__)
        print(e)
        logging.error(traceback.format_exc())
        # Logs the error appropriately.
    """Echo the user message."""
#    update.message.reply_text(update.message.text)
#    s.yum("/home/wmw/app/youtubeuploader/upload.sh " + update.message.text).run()
#    subprocess.Popen("source /home/wmw/app/youtubeuploader/upload.sh " + update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TKN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.chat(144149077) & Filters.text, echo))

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
