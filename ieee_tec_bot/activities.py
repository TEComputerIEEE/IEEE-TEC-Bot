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


def listActivities(branchName, chapterName=None):
    '''
    Method that gets from the api a list of activities of a branch or chapter
    branch name is required to search the branch or chapter activities,
    the chapterName is required only to list chapter activities
    The connection module use cache to improve response time
    '''
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

        # List of activities
        activities = conn.apiGet(config.activitiesEntryPoint,
                                 parameters=parameters)["activities"]
    # If something's wrong just raise the same exception
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
        keyboard = [[InlineKeyboardButton("Registrarse",
                                          callback_data=callback_data)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = {"text": text, "keyboard": keyboard,
                   "reply_markup": reply_markup, "photo": activity["flyer"]}
        messages.append(message)
    messages.append({"text": "Le invitamos cordialmente a participar a \
                     nuestras actividades."})
    return messages
