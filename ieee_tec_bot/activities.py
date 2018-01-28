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

'''
Method that gets from the api a list of activities of a branch or chapter
branch name is required to search the branch or chapter activities, the chapterName
is required only to list chapter activities
The connection module use cache to improve response time
'''
def listActivities(branchName, chapterName=None):
	activities = []
	branchID=0
	chapterID=None
	#Get the data of the branch and chapter with their names
	try:
		branchID = conn.getBranchData(branchName)["branchID"]
		parameters = {"branchID":branchID}
		#if chaptername is defined, then add the chapter id to the parameters dict
		if chapterName!=None:
			chapterID = conn.getChapterData(branchName,chapterName)["chapterID"]
			parameters.update({"chapterID":chapterID})
		#list of activities
		activities = conn.apiGet(config.activitiesEntryPoint, parameters=parameters)["activities"]
	#if something's wrong just raise the same exception
	except ValueError as e:
		raise e
	#if no activities found then return a generic message to let the user know
	if activities == []:
		text = "No se encontraron actividades registradas para "
		if chapterName!=None:
			text +=  "el capítulo " +chapterName+" de "
		text += "la rama estudiatil de la universidad " + branchName+ "."
		return [{"text":text}]

	messages = []
	#format the message response and append them to a list
	#each message response have this format message={"text":"some text", "keyboard":keyboard, "reply_markup":reply_markup, "photo":activity["flyer"]}
	#and also a document can be sent adding the key to de dict
	for activity in activities:
		text = "".join(["<b>",activity["name"],"</b>\n"])
		text += activity["description"]+"\n"
		text += "<b>Lugar: </b>"+activity["place"]+"\n"
		date = parser.parse(activity["date"]).replace(tzinfo=timezone.utc).astimezone(tz=None)
		dateStr = date.strftime("<b>Día:</b> %A %d de %B %Y. <b>Hora:</b> %I:%M %p")
		text += dateStr
		callback_data = "Subscribe:"+":".join([str(branchID),str(chapterID),str(activity["activityID"])])
		keyboard = [[InlineKeyboardButton("Subscribirse", callback_data=callback_data)]]
		reply_markup = InlineKeyboardMarkup(keyboard)
		message = {"text":text, "keyboard":keyboard, "reply_markup":reply_markup, "photo":activity["flyer"]}
		messages.append(message)
	messages.append({"text":"Le invitamos cordialmente a participar a nuestras actividades."})
	return messages
