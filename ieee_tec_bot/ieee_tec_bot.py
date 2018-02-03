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
from telegram.ext.dispatcher import run_async
from connection import getBranchData
import information as info
import activities
import logging
import config
import base64       # Image parse
import telegram     # Necessary for Keyboards
import os           # For TELAPIKEY


# Const keys text
_RETURN_KEY = u"🔙 Regresar"
_BRANCH_ACTIVITIES_KEY = u"Actividades de la Rama "
_BRANCH_NOTIFICATIONS_KEY = u"Notificaciones de la Rama "
_BRANCH_CONTACTS_KEY = u"Contactos de la Rama "
# Static Keyboards
# customKeboards[0] = homeKeyboard
# customKeboards[1] = _INFORMATION_SCREEN_NUMBER
# customKeboards[2] = _BENEFITS_SCREEN_NUMBER
# customKeboards[3] = _GUIDES_SCREEN_NUMBER
_CUSTOM_KEYBOARDS = [[[u"Actividades"], [u"Información"],
                      [u"Notificaciones"], [u"Contactos"]],
                     [[u"Beneficios Membresía IEEE"], [u"Guías de \
Inscripción"], [u"Acerca del Bot"], [_RETURN_KEY]],
                     [[u"Beneficios IEEE"], [u"Beneficios Capítulos Técnicos"],
                      [u"Beneficios Grupos de Afinidad"], [_RETURN_KEY]],
                     [[u"¿Cómo ser miembro de IEEE?"],
                      [u"¿Cómo afiliarme a un Capítulo Técnico o Grupo de \
Afinidad?"], [u"Solicitar Asistencia"], [_RETURN_KEY]]]

# Constant Values do not Change them
_HOME_SCREEN_NUMBER = 0
_INFORMATION_SCREEN_NUMBER = 1
_BENEFITS_SCREEN_NUMBER = 2
_GUIDES_SCREEN_NUMBER = 3
_BRANCH_ACTIVITIES_SCREEN_NUMBER = 4
_CHAPTER_ACTIVITIES_SCREEN_NUMBER = 5
_BRANCH_NOTIFICATION_SCREEN_NUMBER = 6
_CHAPTER_NOTIFICATION_SCREEN_NUMBER = 7
_BRANCH_CONTACTS_SCREEN_NUMBER = 8
_CHAPTER_CONTACTS_SCREEN_NUMBER = 9


'''
A hash(it's actually a dictionary but since python implements dictionaries as
hash tables... see
https://mail.python.org/pipermail/python-list/2000-March/048085.html)
to handle each user reply depending on their state(in which screen they are).
Format hash : [screenNumber, lastValidMessage]
'''
_userState = {}


def log():
    """Enable logging if defined on config"""
    if(config.Logging):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - \
%(message)s', level=logging.INFO)
        return logging.getLogger(__name__)
    else:
        return None


_logger = log()


# Helper Functions
def sendMessages(bot, update, keys,
                 messages=[{"text": "Seleccione una Opcion:"}], resize=True):
    '''
    Function to show a keyboard, it also sends a message if required
    keys is a keyboard to send to the user(screen keyboards only)
    A list of messages can received to send them to the user
    Each message is a dict of the form message:{"text": "Text to send",
    "keyboard":(inline keyboard object), "reply_markup":(reply markup object),
    "photo":"base64 string photo data", "document":"file_address.extension"}
    set resize false if the keyboard cannot be resized to fit
    '''
    for message in messages:
        try:
            if "document" in message.keys():
                with open(message["document"], "rb") as document:
                    bot.send_document(chat_id=update.message.chat_id,
                                      document=document)
            if "photo" in message.keys():
                photoData = message["photo"]
                photoName = "".join(["../resources/tmp/photo",
                                    str(update.message.chat_id), ".png"])
                if(photoData != ""):
                    with open(photoName, "wb") as toSave:
                        toSave.write(base64.b64decode(photoData))
                    with open(photoName, "rb") as photo:
                        bot.send_photo(chat_id=update.message.chat_id,
                                       photo=photo)
            if "keyboard" in message.keys():
                inlineKeys = message["keyboard"]
                r_markup = telegram.ReplyKeyboardMarkup(inlineKeys,
                                                        resize_keyboard=resize)
                if "reply_markup" in message.keys():
                    r_markup = message["reply_markup"]
                bot.send_message(parse_mode='HTML',
                                 chat_id=update.message.chat_id,
                                 text=message["text"], reply_markup=r_markup)
            else:
                r_markup = telegram.ReplyKeyboardMarkup(keys,
                                                        resize_keyboard=resize)
                bot.send_message(parse_mode='HTML',
                                 chat_id=update.message.chat_id,
                                 text=message["text"], reply_markup=r_markup)
        except ValueError as e:
            _logger.warning('Something went wrong sending document or message. \
Error "%s"', e)


def closeKeyboard(bot, update, message=config.closeReply):
    '''
    Function to close a keyboard, it also sends a message if required
    '''
    bot.send_message(parse_mode='HTML', chat_id=update.message.chat_id,
                     text=message,
                     reply_markup=telegram.ReplyKeyboardRemove())


def getKeys(screenNumber, branchName=""):
    '''
    Function that gets the keys that a screen has to show
    screenNumber is the constant number of the string
    branchName required only for chapters screens the branch name
    '''
    keys = []
    if(screenNumber == _HOME_SCREEN_NUMBER or
       screenNumber == _INFORMATION_SCREEN_NUMBER or
       screenNumber == _BENEFITS_SCREEN_NUMBER or
       screenNumber == _GUIDES_SCREEN_NUMBER):
        # If is one of the statics just return it
        return _CUSTOM_KEYBOARDS[screenNumber]

    elif (screenNumber == _BRANCH_ACTIVITIES_SCREEN_NUMBER or
          screenNumber == _BRANCH_NOTIFICATION_SCREEN_NUMBER or
          screenNumber == _BRANCH_CONTACTS_SCREEN_NUMBER):
        # If is one of the branches screen get the branches
        keys += [[branch] for branch in info.listBranches()]
    elif (screenNumber == _CHAPTER_ACTIVITIES_SCREEN_NUMBER or
          screenNumber == _CHAPTER_NOTIFICATION_SCREEN_NUMBER or
          screenNumber == _CHAPTER_CONTACTS_SCREEN_NUMBER):
        try:  # Sensitive API call
            acronym = getBranchData(branchName)["acronym"]
            if screenNumber == _CHAPTER_ACTIVITIES_SCREEN_NUMBER:
                keys += [[_BRANCH_ACTIVITIES_KEY+acronym]]

            elif screenNumber == _CHAPTER_NOTIFICATION_SCREEN_NUMBER:
                keys += [[_BRANCH_NOTIFICATIONS_KEY+acronym]]

            else:
                keys += [[_BRANCH_CONTACTS_KEY+acronym]]

            keys += [[chapter] for chapter in info.listChapters(branchName)]
        except ValueError as e:
            # Log the error
            _logger.warning('Something went wrong searching for "%s" branch. \
Error "%s"', branchName, e)
            return _CUSTOM_KEYBOARDS[_HOME_SCREEN_NUMBER]
    else:
        # Log the error
        _logger.warning('Error on getkeys, "%d" inserted.', screenNumber)
    return keys+[[_RETURN_KEY]]


def goToScreen(bot, update, screenNumber=_HOME_SCREEN_NUMBER,
               messages=[{"text": "Seleccione una Opcion:"}], branchName=""):
    '''
    Since the return and other functions use the same lines to go home
    or other screens this method is implemented, the default screen is the home
    screen a list of messages is received to send them to the user.
    screenNumber is the constant number of the string
    Each message is a dict of the form message:{"text": "Text to send",
    "keyboard":(inline keyboard object), "reply_markup":(reply markup object),
    "photo":"base64 string photo data", "document":"file_address.extension"}
    "branchName":"for chapters screens the branch name"
    '''
    _userState.update({update.message.chat_id: [screenNumber, branchName]})
    sendMessages(bot, update, getKeys(screenNumber, branchName), messages)


@run_async
def homeHandler(bot, update):
    '''
    Function to handle the home screen
    '''
    if update.message.text in _CUSTOM_KEYBOARDS[_HOME_SCREEN_NUMBER][0]:
        # If the activities key is selected then go to that screen
        goToScreen(bot, update, screenNumber=_BRANCH_ACTIVITIES_SCREEN_NUMBER)

    elif update.message.text in _CUSTOM_KEYBOARDS[_HOME_SCREEN_NUMBER][1]:
        # If the information key is selected then go to that screen
        goToScreen(bot, update, screenNumber=_INFORMATION_SCREEN_NUMBER)

    elif update.message.text in _CUSTOM_KEYBOARDS[_HOME_SCREEN_NUMBER][2]:
        # If the notifications key is selected then go to that screen
        goToScreen(bot, update,
                   screenNumber=_BRANCH_NOTIFICATION_SCREEN_NUMBER)

    elif update.message.text in _CUSTOM_KEYBOARDS[_HOME_SCREEN_NUMBER][3]:
        # If the information key is selected then go to that screen
        goToScreen(bot, update, screenNumber=_BRANCH_CONTACTS_SCREEN_NUMBER)

    else:
        # If is not any valid option
        sendMessages(bot, update, getKeys(_HOME_SCREEN_NUMBER),
                     messages=[{"text": config.unrecognizedReply}])


def commonHandler(bot, update, screens, customMethod):
    '''
    Function to encapsulate the common handler steps so the activities,
    contacts and notifications handlers don't have so many lines of repeated
    code screens is a list with the level 2 and level 3 screen numbers e.g:
    [(branch activities or notifications or contacts),
    (chapter activities or notifications or contacts)]
    customMethod is a the custom Method that will be called in order to get
    the required information e.g: info.listContacts
    '''
    chat_id = update.message.chat_id
    if _userState[chat_id][0] == screens[0]:
        if update.message.text == _RETURN_KEY:
            # If return key is pressed then go to home screen
            goToScreen(bot, update)

        elif update.message.text in info.listBranches():
            # if a branch is selected then show the level 3 screen
            # (chapter notifications, activities or contacts)
            goToScreen(bot, update, screenNumber=screens[1],
                       branchName=update.message.text)

        else:
            # If is not any valid option
            goToScreen(bot, update, screenNumber=screens[0],
                       messages=[{"text": config.unrecognizedReply}])

    elif _userState[chat_id][0] == screens[1]:
        if update.message.text == _RETURN_KEY:
            # If return key is pressed then go to the previous screen
            goToScreen(bot, update, screenNumber=screens[0])

        elif (_BRANCH_ACTIVITIES_KEY in update.message.text or
              _BRANCH_NOTIFICATIONS_KEY in update.message.text or
              _BRANCH_CONTACTS_KEY in update.message.text):
            # Calls the custom method with the branch name to get the info
            messages = customMethod(branchName=_userState[chat_id][1])
            goToScreen(bot, update, messages=messages)

        elif update.message.text in info.listChapters(_userState[chat_id][1]):
            # Calls the custom method with the branch and chapter names
            # to get the required the info
            messages = customMethod(chapterName=update.message.text,
                                    branchName=_userState[chat_id][1])
            goToScreen(bot, update, messages=messages)

        else:
            # If is not any valid option
            sendMessages(bot, update, getKeys(screens[1],
                         branchName=_userState[update.message.chat_id][1]),
                         messages=[{"text": config.unrecognizedReply}])
    else:
        # Log the error
        _logger.warning('Something went wrong reaching common handler screen \
                        code: "%d".', _userState[update.message.chat_id][0])
        goToScreen(bot, update, messages=[{"text": config.unrecognizedReply}])


@run_async
def activitiesHandler(bot, update):
    '''
    Function to handle Activities Screens
    Just calls the common handler with his data
    '''
    # Set the screens to show for this handler
    screens = [_BRANCH_ACTIVITIES_SCREEN_NUMBER,
               _CHAPTER_ACTIVITIES_SCREEN_NUMBER]
    # Set the custom function/method to be called if the info is required
    customMethod = activities.listActivities
    commonHandler(bot, update, screens, customMethod)


@run_async
def contactsHandler(bot, update):
    '''
    Function to handle Contacts Screens
    Just calls the common handler with his data
    '''
    # Set the screens to show for this handler
    screens = [_BRANCH_CONTACTS_SCREEN_NUMBER,
               _CHAPTER_CONTACTS_SCREEN_NUMBER]
    # Set the custom function/method to be called if the info is required
    customMethod = info.listContacts
    commonHandler(bot, update, screens, customMethod)


@run_async
def notificationsHandler(bot, update):
    '''
    Function to handle Notifications Screens
    Just calls the common handler with his data
    '''
    # Set the screens to show for this handler
    screens = [_BRANCH_NOTIFICATION_SCREEN_NUMBER,
               _CHAPTER_NOTIFICATION_SCREEN_NUMBER]
    # Set the custom function/method to be called if the info is required
    customMethod = activities.listActivities  # Replace with proper call
    commonHandler(bot, update, screens, customMethod)


@run_async
def informationHandler(bot, update):
    '''
    Function to handle Info Screens
    Depending on the user state redirects
    '''
    chat_id = update.message.chat_id
    chat_text = update.message.text
    if _userState[chat_id][0] == _INFORMATION_SCREEN_NUMBER:
        if chat_text in _CUSTOM_KEYBOARDS[_INFORMATION_SCREEN_NUMBER][0]:
            # If benefits selected, go to the benefits screen
            goToScreen(bot, update, screenNumber=_BENEFITS_SCREEN_NUMBER)

        elif chat_text in _CUSTOM_KEYBOARDS[_INFORMATION_SCREEN_NUMBER][1]:
            # If guides selected, go to the guides screen
            goToScreen(bot, update, screenNumber=_GUIDES_SCREEN_NUMBER)

        elif chat_text in _CUSTOM_KEYBOARDS[_INFORMATION_SCREEN_NUMBER][2]:
            # If about selected, return the info and go to the home screen
            goToScreen(bot, update, messages=[{"text": info.about()}])

        elif chat_text in _CUSTOM_KEYBOARDS[_INFORMATION_SCREEN_NUMBER][3]:
            # If return key is pressed go to home screen
            goToScreen(bot, update)

        else:
            # If is not any valid option
            sendMessages(bot, update, getKeys(_INFORMATION_SCREEN_NUMBER),
                         config.unrecognizedReply)

    elif _userState[chat_id][0] == _BENEFITS_SCREEN_NUMBER:
        if chat_text in _CUSTOM_KEYBOARDS[_BENEFITS_SCREEN_NUMBER][0]:
            # If IEEE benefits selected, show the info
            replyText = info.IEEEBenefist()
            goToScreen(bot, update, messages=[{"text": replyText}])

        elif chat_text in _CUSTOM_KEYBOARDS[_BENEFITS_SCREEN_NUMBER][1]:
            # If Tech Chapters benefits selected, show the info
            replyText = info.chaptersBenefits()
            goToScreen(bot, update, messages=[{"text": replyText}])

        elif chat_text in _CUSTOM_KEYBOARDS[_BENEFITS_SCREEN_NUMBER][2]:
            # If affinity groups benefits selected, get the info from the info
            # module replyText=info.groupsBenefits()
            replyText = info.groupsBenefits()
            goToScreen(bot, update, messages=[{"text": replyText}])

        elif chat_text in _CUSTOM_KEYBOARDS[_BENEFITS_SCREEN_NUMBER][3]:
            # If return key is pressed to info screen
            goToScreen(bot, update, screenNumber=_INFORMATION_SCREEN_NUMBER)

        else:
            # If is not any valid option
            sendMessages(bot, update, getKeys(_BENEFITS_SCREEN_NUMBER),
                         config.unrecognizedReply)

    elif _userState[chat_id][0] == _GUIDES_SCREEN_NUMBER:
        if chat_text in _CUSTOM_KEYBOARDS[_GUIDES_SCREEN_NUMBER][0]:
            # If Membership info selected, get the info from the info module
            replyText = info.membershipSteps()
            goToScreen(bot, update,
                       messages=[{"text": replyText,
                                  "document": config.membershipPath}])

        elif chat_text in _CUSTOM_KEYBOARDS[_GUIDES_SCREEN_NUMBER][1]:
            # If Tech Chapters benefits selected, shows the info
            replyText = info.chapterMembershipSteps()
            goToScreen(bot, update,
                       messages=[{"text": replyText,
                                  "document": config.chapterMembershipPath}])

        elif chat_text in _CUSTOM_KEYBOARDS[_GUIDES_SCREEN_NUMBER][2]:
            # if the help button is pressed move to the contacts screen
            goToScreen(bot, update,
                       screenNumber=_BRANCH_CONTACTS_SCREEN_NUMBER)

        elif chat_text in _CUSTOM_KEYBOARDS[_GUIDES_SCREEN_NUMBER][3]:
            # If return key is pressed to info screen
            goToScreen(bot, update, screenNumber=_INFORMATION_SCREEN_NUMBER)

        else:
            # If is not any valid option
            sendMessages(bot, update, getKeys(_GUIDES_SCREEN_NUMBER),
                         config.unrecognizedReply)

    else:
        # Log the error and return home
        _logger.warning('Something went wrong reaching information handler \
screen code: "%d".', _userState[chat_id][0])
        goToScreen(bot, update, messages=[{"text": config.unrecognizedReply}])


#  Command handlers
@run_async
def start(bot, update):
    '''
    Bot start command, will return a welcome message and the home screen
    keyboard
    '''
    # Goes to home screen
    goToScreen(bot, update, messages=[{"text": config.startReply}])


@run_async
def help(bot, update):
    '''
    Bot help command, will return a help message and the home screen keyboard
    '''
    pass


@run_async
def stop(bot, update):
    '''
    Bot help command, will remove the data of the user and stop sending
    messages to they
    '''
    pass


@run_async
def handleMessage(bot, update):
    '''
    Function to handle text messages depending on which screen the user is,
    this will only pre-clasify the queries, but the actual handling will happen
    on each helper method that will parse the message and look for the required
    info
    '''
    chat_id = update.message.chat_id
    if not(chat_id in _userState.keys()):
        # If the user is not registered then go to home screen
        goToScreen(bot, update)

    if _userState[chat_id][0] == _HOME_SCREEN_NUMBER:
        homeHandler(bot, update)

    elif (_userState[chat_id][0] == _INFORMATION_SCREEN_NUMBER or
          _userState[chat_id][0] == _BENEFITS_SCREEN_NUMBER or
          _userState[chat_id][0] == _GUIDES_SCREEN_NUMBER):
        informationHandler(bot, update)

    elif (_userState[chat_id][0] == _BRANCH_ACTIVITIES_SCREEN_NUMBER or
          _userState[chat_id][0] == _CHAPTER_ACTIVITIES_SCREEN_NUMBER):
        activitiesHandler(bot, update)

    elif (_userState[chat_id][0] == _BRANCH_NOTIFICATION_SCREEN_NUMBER or
          _userState[chat_id][0] == _CHAPTER_NOTIFICATION_SCREEN_NUMBER):
        notificationsHandler(bot, update)

    elif (_userState[chat_id][0] == _BRANCH_CONTACTS_SCREEN_NUMBER or
          _userState[chat_id][0] == _CHAPTER_CONTACTS_SCREEN_NUMBER):
        contactsHandler(bot, update)

    else:
        # Log the error
        _logger.warning('Error on handleMessage, "%s" state.',
                        _userState[chat_id][0])
        goToScreen(bot, update)


@run_async
def unrecognized(bot, update):
    '''
    Unrecognized is a method so when natural language processing
    is implemented. will be easier to incorporate to the actual code
    '''
    update.message.reply_text(config.unrecognizedReply)


@run_async
def error(bot, update, error):
    '''
    Log errors
    '''
    _logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    '''
    Bot main flow function
    '''
    # Making the bot work
    # Create the EventHandler and pass it your bot's token.
    TELAPIKEY = os.environ.get("TELEGRAM_API_KEY")
    if(TELAPIKEY is None):
        print("No TELEGRAM_API_KEY variable defined, please type on terminal export \
TELEGRAM_API_KEY=value(or add it to the ~/.bashrc file).")
        return -1
    updater = Updater(TELAPIKEY)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # On different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("stop", stop))
    # inline commands to be implemented later on
    # ("info", info)
    # ("contact", contact))
    # ("activities", activities))

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
    # If this file is run as main call the main method
    main()
