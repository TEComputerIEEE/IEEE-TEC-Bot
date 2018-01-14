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
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler,Filters
import logging
import config
import telegram #necessary for Keyboards


#Keyboards
#customKeboards[0] = homeKeyboard
#customKeboards[1] = infoScreen
#customKeboards[2] = benefitScreen
#customKeboards[3] = guideScreen
customKeyboards =  [[["Actividades"], ["Informacion"], ["Notificaciones"], ["Contactos"]],
                    [["Beneficios Membresía IEEE"], ["Guías de Inscripción"], ["Acerca del Bot"], ["🔙 Regresar"]],
                    [["Beneficios IEEE"], ["Beneficios Capítulos Técnicos"], ["Beneficios Grupos de Afinidad"], ["🔙 Regresar"]],
                    [["¿Cómo ser miembro de IEEE?"], ["¿Cómo afiliarme a un Capítulo Técnico o Grupo de Afinidad?"], ["Solicitar Asistencia"], ["🔙 Regresar"]]]

#Constant Values do not Change them
homeScreen = 0
infoScreen = 1
benefitScreen = 2
guideScreen = 3
branchActivities = 4
chapterActivities = 5
branchNotifications = 6
chapterNotifications = 7
branchContacts = 8
chapterContacts = 9

#A hash(it's actually a dictionary but since python implements dictionaries as hash tables... see https://mail.python.org/pipermail/python-list/2000-March/048085.html)
#to handle each user reply depending on their state(in which screen they are).
userState = {}


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

def stop(bot, update):
    pass

def membershipInfoMenu(bot,update):
    bot.send_message(chat_id= update.message.chat_id,text='Seleccione la opción correspondiente',
                     reply_markup=telegram.ReplyKeyboardMarkup(customKeyboards[guideScreen],resize_keyboard=True))

def sentIEEEMembershipInfo(bot,update):
    membership_info= open("MembresíaIEEE.pdf","rb")
    bot.send_document(chat_id= update.message.chat_id, document= membership_info)
    membership_info.close()
    bot.send_message(chat_id= update.message.chat_id,
                     text='También puede encontrar la guía en la siguiente'+
                     'dirección:\n bit.ly/IEEE-Guia-Inscripcion')

def sentChapterMembershipInfo(bot,update):
    membership_info= open("MembresíaIEEE.pdf","rb")
    bot.send_document(chat_id= update.message.chat_id, document= membership_info)
    membership_info.close()
    bot.send_message(chat_id= update.message.chat_id,
                     text='También puede encontrar la guía en la siguiente'+
                     'dirección:\n bit.ly/IEEE-Guia-Inscripcion')

def requestAssistance(bot,update):
    pass

def closeKeyboard(bot,update):
    bot.send_message(chat_id= update.message.chat_id,text='Listo',
                     reply_markup=telegram.ReplyKeyboardRemove())

def handleMessage(bot, update):
    #If the user is registered
    if not(update.message.chat_id in userState):
        userState.update({update.message.chat_id : 0})
    #If not then

"""
Unrecognized is a method so when natural language processing
is implemented. will be easier to incorporate to the actual code
"""
def unrecognized(bot, update):
    update.message.reply_text(config.unrecognizedReply)

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
    dp.add_handler(CommandHandler("stop", stop))
    # inline commands to be implemented later on
    #("info", info)
    #("contact", contact))
    #("activities", activities))

    # on noncommand i.e message - return error
    dp.add_handler(MessageHandler(Filters.text, handleMessage))

    # log errors if enabled
    if(config.Logging):
        dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Loop 'till the end of the world(or interrupted)
    updater.idle()



if __name__ == '__main__':
    main()
