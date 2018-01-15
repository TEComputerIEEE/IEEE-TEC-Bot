#!/usr/bin/env python
# -*- coding: utf-8 -*-
# IEEE Computer TEC Telegram Bot
# Info module

'''
Method that returns the about information formated as is
'''
def about():
	#About info have to be formated here(the contributors link can be pulled from github)
	aboutText = "<b>Acerca del Bot</b>\nLorem ipsum dolor sit amet, consectetur adipiscing elit.\n<b>Desarrolladores:</b>\n"
	for i in range(1, 8):
		aboutText+="⚫ Nombre Completo - @johndoe\n"
	aboutText+="Para más información visite el proyecto en <a href='https://github.com/TEComputerIEEE/IEEE-TEC-Bot/'>github</a>."
	return aboutText
'''
Method that gets from the api a list of branches
Some caching can be implemented since the branches will not be changing often
'''
def listBranches():
	# Api call and stuff (The API is not yet implemented)
	return [u"Rama Estudiantil Tecnológico de Costa Rica"]

'''
Method that gets from the api a list of chapters
Some caching can be implemented since the chapters will not be changing often
'''
def listChapters(BranchName):
	abbreviation = getBranchAbbreviation(BranchName)
	# Api call and stuff (The API is not yet implemented)
	return [u"Capítulo Computer "+abbreviation]

'''
Method that gets from the api a abbreviation for the branch name
Some caching can be implemented since the branch names will not be changing often
'''
def getBranchAbbreviation(BranchName):
	# Api call and stuff (The API is not yet implemented)
	if(True):
		return u"TEC"
	else:
		raise Exception("The Chapter cannot be found.")

