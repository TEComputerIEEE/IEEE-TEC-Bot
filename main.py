#!/usr/bin/env python
# -*- coding: utf-8 -*-
# IEEE Computer TEC Telegram Bot
"""
This bot show you branch and chapters information, activities and notify you.

Usage:
Send /start to initiate a conversation.
Send /help to see available commands.
Send /info to see diferent information.
Send /contact to see contact information.
Send /activity to see different activities info.
Send /subs to subscribe to a activity
Send /notify to activate notifications
"""
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import config

# Enable logging if defined on config
def log():
    if(config.Logging):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        return logging.getLogger(__name__)
    else:
        return None
logger = log()


# Command handlers
def start(bot, update):
    #Start reply
    update.message.reply_text(config.startReply)

def help(bot, update):
    pass

def info(bot, update):
    pass

def contact(bot, update):
    pass

def subs(bot, update):
    pass

def notify(bot, update):
    pass

"""
Unrecognized is a method so when natural language processing
is implemented. will be easier to incorporate to the actual code
"""
def unrecognized(bot, update):
    update.message.reply_text(config.ungrecognizedReply)

def error(bot, update, error):
    #Log errors
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Making the bot work
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config.TELAPIKEY)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("contact", contact))
    dp.add_handler(CommandHandler("subs", subs))
    dp.add_handler(CommandHandler("notify", notify))

    # on noncommand i.e message - return error
    dp.add_handler(MessageHandler(Filters.text, unrecognized))

    # log errors if enabled
    if(config.Logging):
        dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Loop 'till the end of the world(or interrupted)
    updater.idle()



if __name__ == '__main__':
    main()
