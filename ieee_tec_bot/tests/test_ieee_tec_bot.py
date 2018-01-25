#!/usr/bin/env python
# -*- coding: utf-8 -*-
# IEEE Computer TEC Telegram Bot
'''
Tests for the ieee_tec_bot module
'''
from telegram.ext import Updater
import telegram
import os # For TELAPIKEY
import pytest
import base64
from ieee_tec_bot import ieee_tec_bot as ieeeBot
from ieee_tec_bot import config

# Making the bot work
# Create the EventHandler and pass it your bot's token.
TELAPIKEY = os.environ.get("TELEGRAM_API_KEY")
if(TELAPIKEY == None):
    print("No TELEGRAM_API_KEY variable defined, please type on terminal export TELEGRAM_API_KEY=value(or add it to the ~/.bashrc file).")
updater = Updater(TELAPIKEY)
# Start the bot
updater.start_polling()
bot = updater.bot
chat_id = 138014594

'''
Function that test if all the keyboards are returned
'''
def test_get_keys():
	homeKeys = ieeeBot.getKeys(ieeeBot.homeScreen)
	infoKeys = ieeeBot.getKeys(ieeeBot.infoScreen)
	benefitsKeys = ieeeBot.getKeys(ieeeBot.benefitScreen)
	guideKeys = ieeeBot.getKeys(ieeeBot.guideScreen)
	baKeys = ieeeBot.getKeys(ieeeBot.branchActivities)
	caKeys = ieeeBot.getKeys(ieeeBot.chapterActivities, "Tecnológico de Costa Rica")
	bnKeys = ieeeBot.getKeys(ieeeBot.branchNotifications)
	cnKeys = ieeeBot.getKeys(ieeeBot.chapterNotifications, "Tecnológico de Costa Rica")
	bcKeys = ieeeBot.getKeys(ieeeBot.branchContacts)
	ccKeys = ieeeBot.getKeys(ieeeBot.chapterContacts, "Tecnológico de Costa Rica")
	correct = isinstance(homeKeys, list) != [] and homeKeys != []
	correct &= isinstance(infoKeys, list) != [] and infoKeys != []
	correct &= isinstance(benefitsKeys, list) != [] and benefitsKeys != []
	correct &= isinstance(guideKeys, list) != [] and guideKeys != []
	correct &= isinstance(baKeys, list) != [] and baKeys != []
	correct &= isinstance(caKeys, list) != [] and caKeys != []
	correct &= isinstance(bnKeys, list) != [] and bnKeys != []
	correct &= isinstance(cnKeys, list) != [] and cnKeys != []
	correct &= isinstance(bcKeys, list) != [] and bcKeys != []
	correct &= isinstance(ccKeys, list) != [] and ccKeys != []
	assert correct

'''
Function that test if the open keyboard function is working properly
'''
def test_open_keyboard():
	keys = [['Test key'], ['Test key2'], ['Test key3'], ['Test key4']]
	result = ieeeBot.openKeyboard(bot, chat_id, keys, message="Test message.")
	assert result.text=="Test message."

'''
Function that test if the send photo part of the function is working properly
'''
def test_send_photo():
	keys = [['Test key']]
	photoString = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAADtSURBVBgZBcFBSpVhGAbQ8/18JNEFu1dEW4MbaAFOhDbQPBoE7ag91MhRtYgop9KgIsIfDcQQ3+ftnNEAAACACcCnrzlJ5/zsBQAsAB93fbKzG3kOACwAp+vDbdyrLwDAaJ87ItKHI37eVGUpL7fAJLZaM6Id7bf4DmBSWrtxJ9qiHSgAk/htz8atiAfRNt51KW/G5GzwoZ8oLVpcObDFBSZQIqK1iAgKk/ddHmsRLdpTv6z39SiYlGNtdaS1diVWb/eASWk/PPPHtdg4FAVgocSxuPZqvB6rFgVgUi5FqX9Q+SZ3+QswGgAAAPAfKnCHO1UwyPEAAAAASUVORK5CYII="
	photoData = base64.b64decode(photoString) 
	with open("tests/testImage.png", "wb") as file:
		file.write(photoData)
	with open("tests/testImage.png", "rb") as photo:
		result = ieeeBot.openKeyboard(bot, chat_id, keys, message="Test message.", photo=photo)
		assert result.text=="Test message."

'''
Function that test if the send document part of the function is working properly
'''
def test_send_document():
	keys = [['Test key']]
	documentData = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAADtSURBVBgZBcFBSpVhGAbQ8/18JNEFu1dEW4MbaAFOhDbQPBoE7ag91MhRtYgop9KgIsIfDcQQ3+ftnNEAAACACcCnrzlJ5/zsBQAsAB93fbKzG3kOACwAp+vDbdyrLwDAaJ87ItKHI37eVGUpL7fAJLZaM6Id7bf4DmBSWrtxJ9qiHSgAk/htz8atiAfRNt51KW/G5GzwoZ8oLVpcObDFBSZQIqK1iAgKk/ddHmsRLdpTv6z39SiYlGNtdaS1diVWb/eASWk/PPPHtdg4FAVgocSxuPZqvB6rFgVgUi5FqX9Q+SZ3+QswGgAAAPAfKnCHO1UwyPEAAAAASUVORK5CYII="
	with open("tests/testDocument.txt", "w") as file:
		file.write(documentData)
	with open("tests/testDocument.txt", "rb") as file:
		result = ieeeBot.openKeyboard(bot, chat_id, keys, message="Test message.", document=file)
		assert result.text=="Test message."
		
updater.stop()