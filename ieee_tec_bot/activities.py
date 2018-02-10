#!/usr/bin/env python
# -*- coding: utf-8 -*-
# IEEE Computer TEC Telegram Bot
# Activities module

import locale
import config
import connection as conn
from dateutil import parser
from datetime import timezone, datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# locale.setlocale(locale.LC_TIME, 'es_CR.utf8') # Linux
locale.setlocale(locale.LC_TIME, 'es-CR') # Windows

def _getActivities(branchName=None, chapterName=None, branchID=None, chapterID=None, activityID=None):
    activities = []
    # Get the data of the branch and chapter with their names
    try:
        if(branchID is None):
            if not (branchName is None):
                branchID = conn.getBranchData(branchName)["branchID"]
            else:
                raise ValueError("A branchID or Branch Name needs to be \
                provided")
        parameters = {"branchID": branchID}
        # If chaptername is defined, add the chapter id to the parameters dict
        if chapterID is None:
            if not(chapterName is None):
                chapterID = conn.getChapterData(branchName,
                                                chapterName)["chapterID"]
                parameters.update({"chapterID": chapterID})
        else:
            parameters.update({"chapterID": chapterID})

        if not(activityID is None):
            parameters.update({"activityID": activityID})

        # List of activities
        activities = conn.apiGet(config.activitiesEntryPoint,
                                 parameters=parameters)["activities"]
        result = {"branchID": branchID, "chapterID": chapterID,
                  "activities": activities}
        return result
    # If something's wrong just raise the same exception
    except ValueError as e:
        raise e


def listActivities(branchName, chat_id=None, chapterName=None):
    '''
    Method that gets from the api a list of activities of a branch or chapter
    branch name is required to search the branch or chapter activities,
    the chapterName is required only to list chapter activities
    The connection module use cache to improve response time
    The chat id is used for the "Registrar", "Desregistrar"
    '''
    try:
        activitiesData = _getActivities(branchName=branchName,
                                        chapterName=chapterName)
        branchID = activitiesData["branchID"]
        chapterID = activitiesData["chapterID"]
        activities = activitiesData["activities"]
    except ValueError as e:
        raise e
    # If no activities found then return a generic message to let the user know
    if activities == []:
        text = "No se encontraron actividades registradas para "
        if not(chapterName is None):
            text = "".join([text, "el capítulo ", chapterName, " de "])

        text = "".join([text, "la rama estudiatil de la universidad ",
                       branchName, "."])
        return [{"text": text}]

    messages = []
    # Format the message response and append them to a list
    # Each message response have this format message={"text":"some text",
    # "keyboard":keyboard, "reply_markup":reply_markup,
    # "photo":activity["flyer"]}
    # And also a document can be sent adding the key to de dict
    for activity in activities:
        text = "".join(["<b>", activity["name"], "</b>\n"])
        text = "".join([text, activity["description"], "\n"])
        text = "".join([text, "<b>Lugar: </b>", activity["place"], "\n"])
        date = parser.parse(activity["date"])  # Parse Date
        # Transform to local timezone
        date = date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        dateStr = date.strftime("<b>Día:</b> %A %d de %B %Y. \
        <b>Hora:</b> %I:%M %p")
        text = "".join([text, dateStr])
        callback_data = "".join(["register:",
                                ":".join([str(branchID), str(chapterID),
                                          str(activity["activityID"])])])
        key = "Registrarme"
        if(isRegistered(branchID, activity["activityID"], chat_id,
           chapterID)):
            key = "Cancelar Registro"
        keyboard = [[InlineKeyboardButton(key,
                                          callback_data=callback_data)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = {"text": text, "keyboard": keyboard,
                   "reply_markup": reply_markup, "photo": activity["flyer"]}
        messages.append(message)
    messages.append({"text": "Le invitamos cordialmente a participar a \
    nuestras actividades."})
    return messages


def isRegistered(branchID, activityID, chat_id, chapterID=None):
    """
    Method that returns true if the user is already registered to the activity
    """
    # NEEDS A NEW API CALL For Now:
    assistants = listActivityAssistants(branchID, activityID, chapterID)
    asistant = list(filter(lambda user: user['chatID'] == chat_id, assistants))
    return True if asistant != [] else False


def listActivityAssistants(branchID, activityID, chapterID=None):
    '''
    Method that returns the users(only return the chat id) that are registered
    on a activity
    '''
    try:
        activitiesData = _getActivities(branchID=branchID, chapterID=chapterID,
                                        activityID=activityID)
        activities = activitiesData["activities"]
    except ValueError as e:
        raise e
    if len(activities) != 1:
        return []
    else:
        return activities[0]["users"]


def register(user, branchID, activityID, chapterID=None):
    """
    Method to register or unregister a user from a activity
    returns the text of the message response
    """
    try:
        parameters = {"branchID": branchID, "activityID": activityID,
                      "chatID": user["chatID"]}
        if not(chapterID is None):
            parameters.update({"chapterID": chapterID})
        registerRequest = conn.apiUpdate(config.registerEntryPoint,
                                         parameters=parameters, body=user)
        return registerRequest["message"]
    except ValueError as e:
        raise e


def remindTo():
    '''
    Method that return a dict
    {"chat_id": "message"}
    Message is the reminders string formated to send
    '''
    result = {}
    branchList = conn.apiGet(config.branchesEntryPoint)["branches"]
    now = datetime.now().replace(tzinfo=timezone.utc)
    header = "Recuerde su inscripción a las siguientes actividades mañana:\n"
    for branch in branchList:
        # Search in all the branch activities
        activityList = _getActivities(branchID=branch["branchID"])[
                                      "activities"]
        for activity in activityList:
            date = parser.parse(activity["date"])  # Parse Date
            # Transform to local timezone
            date = date.replace(tzinfo=timezone.utc).astimezone(tz=None)
            dateStr = date.strftime(" a las %I:%M %p")
            diff = date - now
            if diff.days == 1:
                text = "".join(["<b>", activity["name"], "</b> ", dateStr,
                                " en <b>", activity["place"], "</b>.\n"])
                assistants = listActivityAssistants(branch["branchID"],
                                                    activity["activityID"])
                for user in assistants:
                    if user["notify"]:
                        if user["chatID"] in result:
                            result.update({user["chatID"]:
                                           "".join([result[user["chatID"]],
                                                    text])})
                        else:
                            text = "".join([header, text])
                            result.update({user["chatID"]: text})

        # Search in all chapters
        chapterList = conn.apiGet(config.chaptersEntryPoint,
                                  {"branchID": branch["branchID"]})["chapters"]
        for chapter in chapterList:
            activityList = _getActivities(branchID=branch["branchID"],
                                          chapterID=chapter["chapterID"])[
                                          "activities"]
            for activity in activityList:
                date = parser.parse(activity["date"])  # Parse Date
                # Transform to local timezone
                date = date.replace(tzinfo=timezone.utc).astimezone(tz=None)
                dateStr = date.strftime(" a las %I:%M %p")
                diff = date - now
                if diff.days == 1:
                    text = "".join(["<b>", activity["name"], "</b> ", dateStr,
                                    " en <b>", activity["place"], "</b>.\n"])
                    assistants = listActivityAssistants(branch["branchID"],
                                                        activity["activityID"],
                                                        chapter["chapterID"])
                    for user in assistants:
                        if user["notify"]:
                            if user["chatID"] in result:
                                result.update({user["chatID"]:
                                               "".join([result[user["chatID"]],
                                                        text])})
                            else:
                                text = "".join([header, text])
                                result.update({user["chatID"]: text})

    return result

def isSubscribedNotification(branchID, chapterID, chat_id):
    parameters = {"branchID": branchID, "chatID": chat_id}
    if chapterID != None:
        parameters["chapterID"] = chapterID

    return conn.dummyGet(config.notificationsEntryPoint, parameters = parameters)

def subscribeNotification(branchID, chapterID=None, chat_id=None):
    """
    Method to subscribe or unsubscribe a user from a notification,
    returns the text of the message response
    """
    try:
        parameters = {"branchID": branchID}
        if chapterID != None:
            parameters["chapterID"] = chapterID

        user = {"chatID": chat_id}
        # if chat_id is None:
        #    parameters.update({"chapterID": chapterID})
        subscribeRequest = conn.apiUpdate(config.notificationsEntryPoint, parameters=parameters, body=user)
        return subscribeRequest["message"]
    except ValueError as e:
        raise e

def showNotificationOption(branchName, chat_id=None, chapterName=None):
    '''
    Method that gets from the api a list of activities of a branch or chapter
    branch name is required to search the branch or chapter activities,
    the chapterName is required only to list chapter activities
    The connection module use cache to improve response time
    The chat id is used for the "Registrar", "Desregistrar"
    '''
    try:
        activitiesData = _getActivities(branchName=branchName, chapterName=chapterName)
        branchID = activitiesData["branchID"]
        chapterID = activitiesData["chapterID"]
    except ValueError as e:
        raise e


    messages = []
    # Format the message response and append them to a list
    # Each message response have this format message={"text":"some text",
    # "keyboard":keyboard, "reply_markup":reply_markup,
    # "photo":activity["flyer"]}
    # And also a document can be sent adding the key to de dict

    callback_data = [str(branchID), str(chapterID)]

    key = "Suscribirme a notificaciones"
   
    if chapterName is None: # If chapterName is none means that the user selected a Branch.
        text = "¿Desea recibir notificaciones de " + branchName + "?"
    else:
        text = "¿Desea recibir notificaciones de " + chapterName + "?"
    
    if isSubscribedNotification(branchID = branchID, chapterID = chapterID, chat_id = chat_id) == int(chat_id):
        key = "Cancelar notificaciones"

        if (chapterName is None): # If chapterName is none means that the user selected a Branch.
            text = "¿Desea dejar de recibir notificaciones de " + branchName + "?"
        else:
            text = "¿Desea dejar de recibir notificaciones de " + chapterName + "?"

    callback_data = "".join(["notify:",
                                ":".join([str(branchID), str(chapterID), str(chat_id)])])
        
    keyboard = [[InlineKeyboardButton(text = key, callback_data=callback_data)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    

    message = {"text": text, "keyboard": keyboard, "reply_markup": reply_markup}
    messages.append(message)

    return messages