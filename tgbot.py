#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
#import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, date, time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Привет! Расскажу тебе актуальные на ' + datetime.today().strftime('%d/%m/%Y') + ' Напиши мне любой текст, а я отвечу тебе ценами :)')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Пришли ссылку на свою статью.')
def echo(bot, update):
    url_to_scrape = 'http://www.benzin-cena.ru/benzin/86-sankt-peterburg-ceni-v-rubljah'

    # Tell requests to retreive the contents our page (it'll be grabbing
    # what you see when you use the View Source feature in your browser)
    r = requests.get(url_to_scrape)

    # We now have the source of the page, let's ask BeaultifulSoup
    # to parse it for us.
    soup = BeautifulSoup(r.text, "lxml")

    # Down below we'll add our inmates to this list
    inmates_list = []

    for table_row in soup.select("table.fuel__table tr"):
        # Each tr (table row) has three td HTML elements (most people 
        # call these table cels) in it (first name, last name, and age)
        cells = table_row.findAll('td')

        # Our table has one exception -- a row without any cells.
        # Let's handle that special case here by making sure we
        # have more than zero cells before processing the cells
        if len(cells) > 0:
            # Our first name seems to appear in the second td element
            # that ends up being the cell called 1, since we start
            # counting at 0
            nameazs = cells[0].text.strip()
            # Our last name is in the first (0 if we start counting 
            # at 0 like we do in Python td element we encounter
            ai92 = cells[2].text.strip()
            # Age seems to be in the last td in our row
            ai95 = cells[3].text.strip()
            ai98 = cells[4].text.strip()

            # Let's add our inmate to our list in case
            # We do this by adding the values we want to a dictionary, and 
            # appending that dictionary to the list we created above
            inmate = {'nameazs': nameazs, 'ai92': ai92, 'ai95': ai95, 'ai98': ai98}
            inmates_list.append(inmate)

            # Let's print our table out.
            update.message.reply_text(text="_{0}_ *92:* {1}р,, *95:* {2}р., *98:* {3} р.".format(nameazs, ai92, ai95, ai98),parse_mode='MARKDOWN')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

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
