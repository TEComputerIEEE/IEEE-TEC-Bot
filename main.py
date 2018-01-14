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
import information as info
import telegram #necessary for Keyboards


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
def openKeyboard(bot, update, keys, message="Seleccione una Opcion:", resize=True):
    bot.send_message(parse_mode='HTML',chat_id= update.message.chat_id,text=message,
        reply_markup=telegram.ReplyKeyboardMarkup(keys,resize_keyboard=resize))

'''
Function to close a keyboard, it also sends a message if required
'''
def closeKeyboard(bot, update, message="Aquí tiene su información:"):
    bot.send_message(parse_mode='HTML', chat_id= update.message.chat_id,text=message,
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
            abbreviation=info.getBranchAbbreviation(branchName)
            if screenNumber == chapterActivities:
                keys+=[[branchActivitiesKey+abbreviation]]
            elif screenNumber == chapterNotifications:
                keys+=[[branchNotificationsKey+abbreviation]]
            else:
                keys+=[[branchContactsKey+abbreviation]]
            keys+=[ [chapter] for chapter in info.listChapters(branchName) ]
        except Exception, e:
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
def goToScreen(bot, update, screenNumber=homeScreen, message="Seleccione una Opcion:", branchName=""):
    userState.update({update.message.chat_id : [screenNumber, ""]})
    openKeyboard(bot, update, getKeys(screenNumber, branchName),message)


'''
Function to handle the home screen
'''
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
        openKeyboard(bot, update, getKeys(homeScreen), config.unrecognizedReply)

'''
Function to encapsulate the common handler steps so the activities, contacts and notifications handlers don't have so many lines of repeated code
screens is a list with the level 2 and level 3 screen numbers e.g [(branch activities or notifications or contacts), (chapter activities or notifications or contacts)]
customMethods is a list with the methods that will be called to get the required information e.g [info.listBranchContacts, info.listChapterContacts]
'''
def commonHandler(bot, update, screens, customMethods):
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
            goToScreen(bot, update, screenNumber=screens[0], message=config.unrecognizedReply)

    elif userState[update.message.chat_id][0]==screens[1]:
        if update.message.text == returnKey:
            #If return key is pressed then go to the previous screen
            goToScreen(bot, update, screenNumber=screens[0])
        elif update.message.text in info.listChapters(userState[update.message.chat_id][1]):
            #Calls the module to get the info of that chapter (chapter notifications, activities or contacts) with the branch name
            #replyText=customMethods[1](chapterName=update.message.text, branchName=userState[update.message.chat_id][1])
            replyText="Esta es la informacion del capítulo que solicitó"
            goToScreen(bot, update, message=replyText)
        elif branchActivitiesKey in update.message.text:
            #Calls the module to get the info of that chapter (chapter notifications, activities or contacts) with the branch name
            #replyText=customMethods[0](branchName=userState[update.message.chat_id][1])
            replyText="Esta es la informacion de la rama que solicitó"
            goToScreen(bot, update, message=replyText)
        else:
            #If is not any valid option
            openKeyboard(bot, update, getKeys(screens[1]), message=config.unrecognizedReply)
    else:
        #Log the error
        logger.warning('Something went wrong reaching common handler screen code: "%d".', userState[update.message.chat_id][0])
        goToScreen(bot, update, message=config.unrecognizedReply)
'''
Function to handle Activities Screens
'''
def activitiesHandler(bot, update):
    #Set the screens to show for this handler
    screens=[branchActivities, chapterActivities]
    #Set the custom functions/methods to be called if the info is required
    customMethods=["e.g activities.branchActivities without quotes", "e.g activities.chapterActivities without quotes"]
    commonHandler(bot, update, screens, customMethods)

'''
Function to handle Contacts Screens
'''
def contactsHandler(bot, update):
    #Set the screens to show for this handler
    screens=[branchContacts, chapterContacts]
    #Set the custom functions/methods to be called if the info is required
    customMethods=["e.g activities.branchActivities without quotes", "e.g activities.chapterActivities without quotes"]
    commonHandler(bot, update, screens, customMethods)

'''
Function to handle Notifications Screens
'''
def notificationsHandler(bot, update):
    #Set the screens to show for this handler
    screens=[branchNotifications, chapterNotifications]
    #Set the custom functions/methods to be called if the info is required
    customMethods=["e.g activities.branchActivities without quotes", "e.g activities.chapterActivities without quotes"]
    commonHandler(bot, update, screens, customMethods)

'''
Function to handle Info Screens
'''
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
            goToScreen(bot, update, message=info.about())

        elif update.message.text in customKeyboards[infoScreen][3]:
            #If return key is pressed go to home screen
            goToScreen(bot, update)

        else:
            #If is not any valid option
            openKeyboard(bot, update, getKeys(infoScreen), config.unrecognizedReply)


    elif userState[update.message.chat_id][0] == benefitScreen:
        if update.message.text in customKeyboards[benefitScreen][0]:
            #If IEEE benefits selected, get the info from the info module
            #replyText=info.IEEEBenefits()
            replyText ="Mostrando beneficios IEEE"
            goToScreen(bot, update, message=replyText)

        elif update.message.text in customKeyboards[benefitScreen][1]:
            #If Tech Chapters benefits selected, get the info from the info module
            #replyText=info.chaptersBenefits()
            replyText ="Mostrando beneficios Capítulos Técnicos"
            goToScreen(bot, update, message=replyText)

        elif update.message.text in customKeyboards[benefitScreen][2]:
            #If affinity groups benefits selected, get the info from the info module
            #replyText=info.groupsBenefits()
            replyText ="Mostrando beneficios Grupos de Afinidad"
            goToScreen(bot, update, message=replyText)

        elif update.message.text in customKeyboards[benefitScreen][3]:
            #If return key is pressed to info screen
            goToScreen(bot, update, screenNumber=infoScreen)

        else:
            #If is not any valid option
            openKeyboard(bot, update, getKeys(benefitScreen), config.unrecognizedReply)

    elif userState[update.message.chat_id][0] == guideScreen:
        if update.message.text in customKeyboards[guideScreen][0]:
            #If Membership info selected, get the info from the info module
            #replyText=info.membershipSteps()
            replyText ="Mostrando pasos para pertenecer a IEEE"
            goToScreen(bot, update, message=replyText)

        elif update.message.text in customKeyboards[guideScreen][1]:
            #If Tech Chapters benefits selected, get the info from the info module
            #replyText=info.chapterMembershipSteps()
            replyText ="Mostrando pasos para pertenecer a un capítulo."
            goToScreen(bot, update, message=replyText)

        elif update.message.text in customKeyboards[guideScreen][2]:
            #if the help button is pressed move to the contacts screen
            goToScreen(bot, update, screenNumber=branchContacts)

        elif update.message.text in customKeyboards[guideScreen][3]:
            #If return key is pressed to info screen
            goToScreen(bot, update, screenNumber=infoScreen)

        else:
            #If is not any valid option
            openKeyboard(bot, update, getKeys(guideScreen), config.unrecognizedReply)

    else:
        #Log the error and return home 
        logger.warning('Something went wrong reaching information handler screen code: "%d".', userState[update.message.chat_id][0])
        goToScreen(bot, update, message=config.unrecognizedReply)

# Command handlers
'''
Bot start command, will return a welcome message and the home screen keyboard
'''
def start(bot, update):
    #Goes to home screen 
    goToScreen(bot, update, message=config.startReply)

'''
Bot help command, will return a hel message and the home screen keyboard
'''
def help(bot, update):
    pass

'''
Bot help command, will remove the data of the user and stop sending messages to them
'''
def stop(bot, update):
    pass

'''
Function to handle text messages depending on which screen the user is, this will only pre-clasify the queries, but the actual handling will happen on each
helper method that will parse the message and look for the required info
'''
def handleMessage(bot, update):
    if not(update.message.chat_id in userState):
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
def unrecognized(bot, update):
    update.message.reply_text(config.unrecognizedReply)

'''

'''
def error(bot, update, error):
    #Log errors
    logger.warning('Update "%s" caused error "%s"', update, error)



'''
Bot main flow function
'''
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


''' 
If this file is run as main call the main method 
'''
if __name__ == '__main__':
    main()
