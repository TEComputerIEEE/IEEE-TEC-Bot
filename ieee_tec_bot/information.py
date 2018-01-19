#!/usr/bin/env python
# -*- coding: utf-8 -*-
# IEEE Computer TEC Telegram Bot
# Info module

import connection as conn

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
Method that returns the steps to become a member of an IEEE chapter 
'''
def chapterMembershipSteps():
        #The URL needs updating
	chapterMembershipStepsText = "<b>Para convertirse en miembro de un capítulo de IEEE</b>\n"
	chapterMembershipStepsText += "Siga los pasos descritos en el archivo adjunto "
	chapterMembershipStepsText += "o visite la dirección http://bit.ly/IEEE-Guia-Inscripcion."
	return chapterMembershipStepsText

'''
Method that gets from the api a list of branches
The connection module use cache to improve response time
'''
def listBranches():
	#Get branches from the API
	branchList = conn.apiGet("branches")["branches"]
	branchNames = []
	#Get only the names of the branches
	for branch in branchList:
		branchNames += [u"Rama Estudiantil "+branch["college"]]
	return branchNames

'''
Method that gets from the api a list of chapters
branch name is required to search the branch
The connection module use cache to improve response time
'''
def listChapters(BranchName):
	branchData = getBranchData(BranchName)
	chapterList = conn.apiGet("chapters", {"branchID":branchData["branchID"]})["chapters"]
	chapterNames = []
	for chapter in chapterList:
		chapterNames += [chapter["name"]+u" "+branchData["acronym"]]
	return chapterNames

'''
Method that gets from the api one specific branch by name
branch name is required to search the branch
The connection module use cache to improve response time
'''
def getBranchData(BranchName):
	#Get all branches from api
	branchList = conn.apiGet("branches")["branches"]
	#Search for the branch and return the acronym
	for branch in branchList:
		if(branch["college"] in BranchName):
			return branch
	raise Exception("The Branch "+ BranchName +" cannot be found.")

