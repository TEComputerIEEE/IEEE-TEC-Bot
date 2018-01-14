#!/usr/bin/env python
# -*- coding: utf-8 -*-
# IEEE Computer TEC Telegram Bot
# Info module

'''
Method that gets from the api a list of branches
Some caching can be implemented since the branches will not be changing often
'''
def listBranches():
	# Api call and stuff (The API is not yet implemented)
	return ["Rama Estudiantil Tecnológico de Costa Rica"]

'''
Method that gets from the api a list of chapters
Some caching can be implemented since the chapters will not be changing often
'''
def listChapters(BranchName):
	# Api call and stuff (The API is not yet implemented)
	return ["Capítulo Computer TEC"]

'''
Method that gets from the api a abbreviation for the branch name
Some caching can be implemented since the branch names will not be changing often
'''
def getBranchAbbreviation(BranchName):
	# Api call and stuff (The API is not yet implemented)
	if(True):
		return ["Capítulo Computer TEC"]
	else:
		raise Exception("The Chapter cannot be found.")