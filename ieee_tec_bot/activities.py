#!/usr/bin/env python
# -*- coding: utf-8 -*-
# IEEE Computer TEC Telegram Bot
# Activities module

import locale
import config
import connection as conn
from dateutil import parser
from datetime import timezone
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

locale.setlocale(locale.LC_TIME, 'es_CR.utf8')


def _getActivities(branchName, chapterName=None, activityID=None):
    activities = []
    branchID = 0
    chapterID = None
    # Get the data of the branch and chapter with their names
    try:
        branchID = conn.getBranchData(branchName)["branchID"]
        parameters = {"branchID": branchID}
        # If chaptername is defined, add the chapter id to the parameters dict
        if not(chapterName is None):
            chapterID = conn.getChapterData(branchName,
                                            chapterName)["chapterID"]
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
        activitiesData = _getActivities(branchName, chapterName)
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
        key = "Registrarse"
        if(isRegistered(branchName, activity["activityID"], chat_id,
           chapterName)):
            key = "Desregistrarse"
        keyboard = [[InlineKeyboardButton(key,
                                          callback_data=callback_data)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = {"text": text, "keyboard": keyboard,
                   "reply_markup": reply_markup, "photo": activity["flyer"]}
        messages.append(message)
    messages.append({"text": "Le invitamos cordialmente a participar a \
nuestras actividades."})
    return messages


def isRegistered(branchName, activityID, chat_id, chapterName=None):
    """
    Method that returns true if the user is already registered to the activity
    """
    # NEEDS A NEW API CALL For Now:
    assistants = listActivityAssistants(branchName, activityID, chapterName)
    for assistant in assistants:
        if assistant["chatID"] == chat_id:
            return True
    return False


def listActivityAssistants(branchName, activityID, chapterName=None):
    '''
    Method that returns the users(only return the chat id) that are registered
    on a activity
    '''
    try:
        activitiesData = _getActivities(branchName, chapterName, activityID)
        activities = activitiesData["activities"]
    except ValueError as e:
        raise e
    if len(activities) != 1:
        return []
    else:
        assistants = []
        for assistant in activities[0]["users"]:
            assistants.append(assistant)
        return assistants


def register(user, branchID, activityID, chapterID=None):
    """
    Method to register or unregister a user from a activity
    returns the text of the message response
    """
    try:
        parameters = {"branchID": branchID, "activityID": activityID}
        if not(chapterID is None):
            parameters.update({"chapterID": chapterID})
        activity = conn.apiGet(config.activitiesEntryPoint,
                               parameters=parameters)["activities"][0]
    except ValueError as e:
        raise e
    succes = True  # Here goes the api call to register
    if (succes):
        date = parser.parse(activity["date"])  # Parse Date
        # Transform to local timezone
        date = date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        dateStr = date.strftime("el día <b>%A %d</b> de %B %Y. a las \
 <b>%I:%M %p</b>")
        response = ["Se ha registro correctamente a la actividad <b>",
                    activity["name"], "</b>. Recuerde que la misma se realizar\
á ", dateStr]
    else:
        response = ["Su registro a la actividad no se pudo realizar porque ",
                    "porqué?"]
    return "".join(response)
