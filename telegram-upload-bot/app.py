#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import json
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


#  Download file to local disk
def dl(url):
    print ("Downloading file:%s" % url)
    try:
        s = url.split("/")
        #print(s[-1])
        filename = s[-1]
        type = s[-1].split('.')
        name = type[-2]
        type = type[-1]

        r = requests.get(url)
        print(r.headers)
        # open method to open a file on your system and write the contents
        #print('/tmp/%s' % filename)
        with open('/tmp/%s' % filename, 'wb') as f:
            f.write(r.content)
        print(r.status_code)
    except Exception as e:
        print(e.__doc__)
        print(e)
        logging.error(traceback.format_exc())
    return filename, type


# def start(bot, update):
#     """Send a message when the command /start is issued."""
#     update.message.reply_text('Hi!')


# def help(bot, update):
#     """Send a message when the command /help is issued."""
#     update.message.reply_text('Help!')


def echo(bot, update):
    try:
        if 'clips.twitch.tv/' in update.message.text:
            update.message.reply_text('twitch clip!')
            s = update.message.text.split("/")
            clipname = s[-1]
            #print(clipname)
            r = "https://clips.twitch.tv/api/v2/clips/{}/status".format(clipname)
            #print(r)
            r = requests.get(r)
            js = json.loads(r.text)
            url = js['quality_options'][0]['source']
            link = 'https://clips.twitch.tv/' + clipname
            filename, type = dl(url)
            command = os.popen('tg -W -e "send_video user#144149077 /tmp/%s %s"' % (filename, link))
            #print(command.read())
            #print(command.close())
        else:
            s = update.message.text.split("/")
            print(s[-1])
            filename = s[-1]
            type = s[-1].split('.')
            name = type[-2]
            type = type[-1]
            #print(type)
            #print(name)
            filename, type = dl(update.message.text)
            #print('print r')
            #print(type)
            print(filename)
            if 'mp4' or 'm4v' or 'mov' in type:
                print('send_video')
                command = os.popen('tg -W -e "send_video user#144149077 /tmp/%s"' % filename)
                #print(command.read())
                #print(command.close())
            if 'jpg' or 'png' or 'jpeg' in type:
                print('send_photo')
                command = os.popen('tg -W -e "send_photo user#144149077 /tmp/%s"' % filename)
                #print(command.read())
                #print(command.close())
                #subprocess.check_call(['wget  -O /tmp/tg.tmp ', update.message.text])
                #subprocess.check_call(['/home/wmw/app/youtubeuploader/upload.sh', update.message.text])

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
    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", help))

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
