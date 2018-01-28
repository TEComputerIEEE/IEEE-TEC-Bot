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
from telegram.ext.dispatcher import run_async
from connection import getBranchData, getChapterData
import information as info
import activities
import logging
import config
import base64
import telegram #necessary for Keyboards
import os # For TELAPIKEY


#Const keys text
returnKey = u"🔙 Regresar"
branchActivitiesKey = u"Actividades de la Rama "
branchNotificationsKey = u"Notificaciones de la Rama "
branchContactsKey = u"Contactos de la Rama "
#Static Keyboards
#customKeboards[0] = homeKeyboard
#customKeboards[1] = infoScreen
#customKeboards[2] = benefitScreen
#customKeboards[3] = guideScreen
customKeyboards =  [[[u"Actividades"], [u"Información"], [u"Notificaciones"], [u"Contactos"]],
                    [[u"Beneficios Membresía IEEE"], [u"Guías de Inscripción"], [u"Acerca del Bot"], [returnKey]],
                    [[u"Beneficios IEEE"], [u"Beneficios Capítulos Técnicos"], [u"Beneficios Grupos de Afinidad"], [returnKey]],
                    [[u"¿Cómo ser miembro de IEEE?"], [u"¿Cómo afiliarme a un Capítulo Técnico o Grupo de Afinidad?"], [u"Solicitar Asistencia"], [returnKey]]]

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


'''
A hash(it's actually a dictionary but since python implements dictionaries as hash tables... see https://mail.python.org/pipermail/python-list/2000-March/048085.html)
to handle each user reply depending on their state(in which screen they are).
Format hash : [screenNumber, lastValidMessage]
'''
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

#Helper Functions
'''
Function to show a keyboard, it also sends a message if required
'''
def sendMessages(bot, update, keys, messages=[{"text":"Seleccione una Opcion:"}], resize=True):
    for message in messages:
        try:
            if "document" in message.keys():
                with open(message["document"], "rb") as document:
                    bot.send_document(chat_id=update.message.chat_id, document=document)
            if "photo" in message.keys():
                photoData = message["photo"]
                photoName = "../resources/tmp/photo"+str(update.message.chat_id)+".png"
                if(photoData!=""):
                    with open(photoName, "wb") as toSave:
                        toSave.write(base64.b64decode(photoData))
                    with open(photoName, "rb") as photo:
                        bot.send_photo(chat_id=update.message.chat_id, photo=photo)
            if "keyboard" in message.keys():
                inlineKeys = message["keyboard"]
                reply_markup=telegram.ReplyKeyboardMarkup(inlineKeys, resize_keyboard=resize)
                if "reply_markup" in message.keys():
                    reply_markup=message["reply_markup"]
                bot.send_message(parse_mode='HTML',chat_id= update.message.chat_id,text=message["text"],
                    reply_markup=reply_markup)
            else:
                reply_markup=telegram.ReplyKeyboardMarkup(keys, resize_keyboard=resize)
                bot.send_message(parse_mode='HTML',chat_id= update.message.chat_id,text=message["text"],
                    reply_markup=reply_markup)
        except ValueError as e:
            logger.warning('Something went wrong sending document or message. Error "%s"', e)

'''
Function to close a keyboard, it also sends a message if required
'''
def closeKeyboard(bot, update, message=config.closeReply):
    bot.send_message(parse_mode='HTML', chat_id=update.message.chat_id,text=message,
                     reply_markup=telegram.ReplyKeyboardRemove())

'''
Function that gets the keys that a screen has to show
'''
def getKeys(screenNumber, branchName=""):
    keys = []
    if screenNumber == homeScreen or screenNumber == infoScreen or screenNumber == benefitScreen or screenNumber == guideScreen:
        #If is one of the statics just return it
        return customKeyboards[screenNumber]
    elif screenNumber == branchActivities or screenNumber == branchNotifications or screenNumber == branchContacts:
        #if is one of the branches screen get the branches
        keys+=[ [branch] for branch in info.listBranches() ]
    elif screenNumber == chapterActivities or screenNumber == chapterNotifications or screenNumber == chapterContacts:
        try:#Since a API search call will be made and the result is needed in order to continue
            acronym=getBranchData(branchName)["acronym"]
            if screenNumber == chapterActivities:
                keys+=[[branchActivitiesKey+acronym]]
            elif screenNumber == chapterNotifications:
                keys+=[[branchNotificationsKey+acronym]]
            else:
                keys+=[[branchContactsKey+acronym]]
            keys+=[ [chapter] for chapter in info.listChapters(branchName) ]
        except ValueError as e:
            #Log the error
            logger.warning('Something went wrong searching for "%s" branch. Error "%s"', branchName, e)
            return customKeyboards[homeScreen]
    else:
        #Log the error
        logger.warning('Error on getkeys, "%d" inserted.', screenNumber)
    return keys+[[returnKey]]

'''
Since the return and other functions use the same lines to go home 
or other screens this method is implemented, the default screen is the home screen
'''
@run_async
def goToScreen(bot, update, screenNumber=homeScreen, messages=[{"text":"Seleccione una Opcion:"}], branchName=""):
    userState.update({update.message.chat_id : [screenNumber, branchName]})
    sendMessages(bot, update, getKeys(screenNumber, branchName), messages)


'''
Function to handle the home screen
'''
@run_async
def homeHandler(bot, update):
    if update.message.text in customKeyboards[homeScreen][0]:
        #If the activities key is selected then go to that screen
        goToScreen(bot, update, screenNumber=branchActivities)

    elif update.message.text in customKeyboards[homeScreen][1]:
        #If the information key is selected then go to that screen
        goToScreen(bot, update, screenNumber=infoScreen)

    elif update.message.text in customKeyboards[homeScreen][2]:
        #If the notifications key is selected then go to that screen
        goToScreen(bot, update, screenNumber=branchNotifications)

    elif update.message.text in customKeyboards[homeScreen][3]:
        #If the information key is selected then go to that screen
        goToScreen(bot, update, screenNumber=branchContacts)

    else:
        #If is not any valid option
        sendMessages(bot, update, getKeys(homeScreen), messages=[{"text":config.unrecognizedReply}])

'''
Function to encapsulate the common handler steps so the activities, contacts and notifications handlers don't have so many lines of repeated code
screens is a list with the level 2 and level 3 screen numbers e.g [(branch activities or notifications or contacts), (chapter activities or notifications or contacts)]
customMethod is a list with the methods that will be called to get the required information e.g [info.listBranchContacts, info.listChapterContacts]
'''
def commonHandler(bot, update, screens, customMethod):
    if userState[update.message.chat_id][0]==screens[0]:
        if update.message.text == returnKey:
            #If return key is pressed then go to home screen
            goToScreen(bot, update)
            return
        elif update.message.text in info.listBranches():
            #if a branch is selected then show the level 3 screen (chapter notifications, activities or contacts)
            goToScreen(bot, update, screenNumber=screens[1], branchName=update.message.text)
        else:
            #If is not any valid option
            goToScreen(bot, update, screenNumber=screens[0], messages=[{"text":config.unrecognizedReply}])

    elif userState[update.message.chat_id][0]==screens[1]:
        if update.message.text == returnKey:
            #If return key is pressed then go to the previous screen
            goToScreen(bot, update, screenNumber=screens[0])
        elif branchActivitiesKey in update.message.text or branchNotificationsKey in update.message.text or branchContactsKey in update.message.text:
            #Calls the module to get the info of that chapter (chapter notifications, activities or contacts) with the branch name
            messages=customMethod(branchName=userState[update.message.chat_id][1])
            goToScreen(bot, update, messages=messages)
        elif update.message.text in info.listChapters(userState[update.message.chat_id][1]):
            #Calls the module to get the info of that chapter (chapter notifications, activities or contacts) with the branch name
            messages=customMethod(chapterName=update.message.text, branchName=userState[update.message.chat_id][1])
            goToScreen(bot, update, messages=messages)
        else:
            #If is not any valid option
            sendMessages(bot, update, getKeys(screens[1], branchName=userState[update.message.chat_id][1]), messages=[{"text":config.unrecognizedReply}])
    else:
        #Log the error
        logger.warning('Something went wrong reaching common handler screen code: "%d".', userState[update.message.chat_id][0])
        goToScreen(bot, update, messages=[{"text":config.unrecognizedReply}])
'''
Function to handle Activities Screens
'''
@run_async
def activitiesHandler(bot, update):
    #Set the screens to show for this handler
    screens=[branchActivities, chapterActivities]
    #Set the custom function/method to be called if the info is required
    customMethod=activities.listActivities
    commonHandler(bot, update, screens, customMethod)

'''
Function to handle Contacts Screens
'''
@run_async
def contactsHandler(bot, update):
    #Set the screens to show for this handler
    screens=[branchContacts, chapterContacts]
    #Set the custom function/method to be called if the info is required
    customMethod=info.listContacts
    commonHandler(bot, update, screens, customMethod)

'''
Function to handle Notifications Screens
'''
@run_async
def notificationsHandler(bot, update):
    #Set the screens to show for this handler
    screens=[branchNotifications, chapterNotifications]
    #Set the custom function/method to be called if the info is required
    customMethod=activities.listActivities#replace with proper call  
    commonHandler(bot, update, screens, customMethod)

'''
Function to handle Info Screens
'''
@run_async
def informationHandler(bot, update):
    if userState[update.message.chat_id][0] == infoScreen:
        if update.message.text in customKeyboards[infoScreen][0]:
            #If benefits selected, go to the benefits screen
            goToScreen(bot, update, screenNumber=benefitScreen)

        elif update.message.text in customKeyboards[infoScreen][1]:
            #If guides selected, go to the guides screen
            goToScreen(bot, update, screenNumber=guideScreen)

        elif update.message.text in customKeyboards[infoScreen][2]:
            #If about selected, return the info and go to the home screen
            goToScreen(bot, update, messages=[{"text":info.about()}])

        elif update.message.text in customKeyboards[infoScreen][3]:
            #If return key is pressed go to home screen
            goToScreen(bot, update)

        else:
            #If is not any valid option
            sendMessages(bot, update, getKeys(infoScreen), config.unrecognizedReply)


    elif userState[update.message.chat_id][0] == benefitScreen:
        if update.message.text in customKeyboards[benefitScreen][0]:
            #If IEEE benefits selected, get the info from the info module
            replyText =info.IEEEBenefist()
            goToScreen(bot, update, messages=[{"text":replyText}])

        elif update.message.text in customKeyboards[benefitScreen][1]:
            #If Tech Chapters benefits selected, get the info from the info module
            replyText =info.chaptersBenefits()
            goToScreen(bot, update, messages=[{"text":replyText}])

        elif update.message.text in customKeyboards[benefitScreen][2]:
            #If affinity groups benefits selected, get the info from the info module
            #replyText=info.groupsBenefits()
            replyText ="Mostrando beneficios Grupos de Afinidad"
            goToScreen(bot, update, messages=[{"text":replyText}])

        elif update.message.text in customKeyboards[benefitScreen][3]:
            #If return key is pressed to info screen
            goToScreen(bot, update, screenNumber=infoScreen)

        else:
            #If is not any valid option
            sendMessages(bot, update, getKeys(benefitScreen), config.unrecognizedReply)

    elif userState[update.message.chat_id][0] == guideScreen:
        if update.message.text in customKeyboards[guideScreen][0]:
            #If Membership info selected, get the info from the info module
            replyText=info.membershipSteps() 
            goToScreen(bot, update, messages=[{"text":replyText,"document": config.membershipPath}])
            
        elif update.message.text in customKeyboards[guideScreen][1]:
            #If Tech Chapters benefits selected, get the info from the info module
            replyText=info.chapterMembershipSteps()
            goToScreen(bot, update, messages=[{"text":replyText,"document": config.chapterMembershipPath}])

        elif update.message.text in customKeyboards[guideScreen][2]:
            #if the help button is pressed move to the contacts screen
            goToScreen(bot, update, screenNumber=branchContacts)

        elif update.message.text in customKeyboards[guideScreen][3]:
            #If return key is pressed to info screen
            goToScreen(bot, update, screenNumber=infoScreen)

        else:
            #If is not any valid option
            sendMessages(bot, update, getKeys(guideScreen), config.unrecognizedReply)

    else:
        #Log the error and return home 
        logger.warning('Something went wrong reaching information handler screen code: "%d".', userState[update.message.chat_id][0])
        goToScreen(bot, update, messages=[{"text":config.unrecognizedReply}])

# Command handlers
'''
Bot start command, will return a welcome message and the home screen keyboard
'''
@run_async
def start(bot, update):
    #Goes to home screen 
    goToScreen(bot, update, messages=[{"text":config.startReply}])

'''
Bot help command, will return a hel message and the home screen keyboard
'''
@run_async
def help(bot, update):
    pass

'''
Bot help command, will remove the data of the user and stop sending messages to them
'''
@run_async
def stop(bot, update):
    pass

'''
Function to handle text messages depending on which screen the user is, this will only pre-clasify the queries, but the actual handling will happen on each
helper method that will parse the message and look for the required info
'''
@run_async
def handleMessage(bot, update):
    if not(update.message.chat_id in userState.keys()):
        #If the user is not registered then go to home screen
        goToScreen(bot, update)
    if userState[update.message.chat_id][0] == homeScreen:
        homeHandler(bot,update)
    elif userState[update.message.chat_id][0] == infoScreen or userState[update.message.chat_id][0] == benefitScreen or userState[update.message.chat_id][0] == guideScreen:
        informationHandler(bot, update)
    elif userState[update.message.chat_id][0] == branchActivities or userState[update.message.chat_id][0] == chapterActivities:
        activitiesHandler(bot, update)
    elif userState[update.message.chat_id][0] == branchNotifications or userState[update.message.chat_id][0] == chapterNotifications:
        notificationsHandler(bot, update)
    elif userState[update.message.chat_id][0] == branchContacts or userState[update.message.chat_id][0] == chapterContacts:
        contactsHandler(bot, update)
    else:
        #Log the error
        logger.warning('Error on getkeys, "%d" inserted.', screenNumber)
        goToScreen(bot, update)
'''
Unrecognized is a method so when natural language processing
is implemented. will be easier to incorporate to the actual code
'''
@run_async
def unrecognized(bot, update):
    update.message.reply_text(config.unrecognizedReply)

'''

'''
@run_async
def error(bot, update, error):
    #Log errors
    logger.warning('Update "%s" caused error "%s"', update, error)



'''
Bot main flow function
'''
def main():
    # Making the bot work
    # Create the EventHandler and pass it your bot's token.
    TELAPIKEY = os.environ.get("TELEGRAM_API_KEY")
    if(TELAPIKEY == None):
        print("No TELEGRAM_API_KEY variable defined, please type on terminal export TELEGRAM_API_KEY=value(or add it to the ~/.bashrc file).")
        return -1
    updater = Updater(TELAPIKEY)

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


''' 
If this file is run as main call the main method 
'''
if __name__ == '__main__':
    main()
