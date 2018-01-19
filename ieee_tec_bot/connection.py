#!/usr/bin/env python
# -*- coding: utf-8 -*-
# IEEE Computer TEC Telegram Bot
# Connection module
# See https://github.com/TEComputerIEEE/IEEE-TEC-WebAPI for a full list of entry points and parameters

import requests
import requests_cache
import schedule
import config
import random #just needed for dummy data delete when api is ready
from datetime import date #just needed for dummy data delete when api is ready
import dummyData as data #just needed for dummy data delete when api is ready

'''
General get method to connect with the Web API, returns json data or raise a exception
entryPoint is the api entry point example /users to get user list(without parameters)
Parameters is a dict with the parameters of the request
cache by default all request will be cached to improve response time
auth still needs to be implemented, and for now it returns just test data
'''
def apiGet(entryPoint, parameters=None, cache=True):
	#Dummy test data
	return dummyGet(entryPoint, parameters)
	response = requests.get(config.webApiAddr+'/'+entryPoint, params=parameters)
	#if the request must not be cached and the response that we get before is cached
	if not cache and response.from_cache:
		#disable cache and get the response
		with requests_cache.disabled():
			respose = requests.get(config.webApiAddr+'/'+entryPoint, params=parameters)
	#if the response is not a valid response, raise a error
	if response.status_code != 200:
		response.raise_for_status()
	#if the request was valid return the response data in a json format
	return response.json()

'''
Dummy test data to be used insted of the Web API
DONT call it directly use the apiGet funct instead
See https://github.com/TEComputerIEEE/IEEE-TEC-WebAPI/issues/3 for full dummy data entry points and params
'''
def dummyGet(entryPoint, parameters=None):
	if entryPoint == "activities":
		activities = {"activities":[]}
		if parameters == None:
			#For every branch in the branches json
			for branch in data.branches["branches"]:
				#add the activities of that branch to a dict
				activities.update({"activities":activities["activities"]+branch["activities"]})
			#For every chapter in the branches json
			for chapter in data.chapters["chapters"]:
				#add the activities of that branch to a dict
				activities.update({"activities":activities["activities"]+chapter["activities"]})
			#returns all IEEE activities
			return activities
		#if the branch ID is in the parameters
		elif "branchID" in parameters.keys():
			#if the chapter ID is in the parameters then search for branch and chapter
			if "chapterID" in parameters.keys():
				#For every chapter in the chapters json
				for chapter in data.chapters["chapters"]:
					#return the activity if the ids are equal
					if(chapter["chapterID"]==parameters["chapterID"] and chapter["branchID"]==parameters["branchID"]):
						return {"activities":chapter["activities"]}
				raise ValueError("No branchID + chapterID combination found")		
			#else just search for branch activities
			else:
				#For every branch in the branches json
				for branch in data.branches["branches"]:
					#return the activity if the ids are equal
					if(branch["branchID"]==parameters["branchID"]):
						return {"activities":branch["activities"]}
				raise ValueError("BranchID not found")
		else:
			raise ValueError("No valid parameters")

	elif entryPoint == "branches":
		branches = {"branches":[]}
		if parameters == None:
			#For every branch in the branches json
			for branch in data.branches["branches"]:
				#add the branch data to a dict
				branches.update({"branches":branches["branches"]+ [{"branchID":branch["branchID"],
																	"college":branch["college"],
																	"acronym":branch["acronym"]}]})
			return branches
		elif "branchID" in parameters.keys(): 
			#For every branch in the branches json
			for branch in data.branches["branches"]:
				#return the branch data if the ids are equal
				if(branch["branchID"]==parameters["branchID"]):
					return { "branches" : [{"branchID":branch["branchID"],
											"college":branch["college"],
											"acronym":branch["acronym"]}]}
			raise ValueError("BranchID not found")
		else:
			raise ValueError("No valid parameters")

	elif entryPoint == "chapters":
		chapters = {"chapters":[]}
		if parameters == None:
			#For every chapter in the chapters json
			for chapter in data.chapters["chapters"]:
				#add the chapter data to a dict
				chapters.update({"chapters":chapters["chapters"]+ [{"chapterID":chapter["chapterID"],
																	"name":chapter["name"],
																	"branchID":chapter["branchID"]}]})
			return chapters
		elif "branchID" in parameters.keys(): 
			if "chapterID" in parameters.keys():
				#For every chapter in the chapters json
				for chapter in data.chapters["chapters"]:
					#return the chapter data if the ids are equal
					if(chapter["branchID"]==parameters["branchID"] and chapter["chapterID"]==parameters["chapterID"]):
						return { "chapters" : [{"chapterID":chapter["chapterID"],
												"name":chapter["name"],
												"branchID":chapter["branchID"]}]}
				raise ValueError("No branchID + chapterID combination found")
			else:
				#For every chapter in the chapters json
				for chapter in data.chapters["chapters"]:
					#add the chapter data to a dict if the branch ids are equal
					if(chapter["branchID"]==parameters["branchID"]):
						chapters.update({"chapters":chapters["chapters"]+ [{"chapterID":chapter["chapterID"],
																			"name":chapter["name"],
																			"branchID":chapter["branchID"]}]})
				return chapters
		else:
			raise ValueError("No valid parameters")
	elif entryPoint == "contacts":
		contacts = {"contacts":[]}
		#if the branch ID is in the parameters
		if "branchID" in parameters.keys():
			#if the chapter ID is in the parameters then search for branch and chapter contacts
			if "chapterID" in parameters.keys():
				#For every chapter in the chapters json
				for chapter in data.chapters["chapters"]:
					#return the contacts if the ids are equal
					if(chapter["chapterID"]==parameters["chapterID"] and chapter["branchID"]==parameters["branchID"]):
						return {"contacts":chapter["contacts"]}
				raise ValueError("No branchID + chapterID combination found")		
			#else just search for branch contacts
			else:
				#For every branch in the branches json
				for branch in data.branches["branches"]:
					#return the contacts if the ids are equal
					if(branch["branchID"]==parameters["branchID"]):
						return {"contacts":branch["contacts"]}
				raise ValueError("BranchID not found")
		else:
			raise ValueError("No valid parameters")

	elif entryPoint == "users":
		#if no parameters return all users
		if parameters == None:
			return data.users
		elif "chatID" in parameters:
			#search for the user
			for user in data.users["users"]:
				#return the contacts if the ids are equal
				if(user["chatID"]==parameters["chatID"]):
					return {"users":[user]}
			raise ValueError("No user find with that id")
		else:
			raise ValueError("No valid parameters")
	else:
		raise ValueError('Invalid entry point')

'''
General post method to connect with the Web API
entryPoint is the api entry point example /users to post a new user(the user should be send in the body)
Parameters is a dict with the parameters of the request
body is a dict with body data
auth still needs to be implemented
'''
def apiPost(entryPoint, parameters=None, body=None):
	response = requests.post(config.webApiAddr+'/'+entryPoint, params=parameters, data=body)
	#if the response is not a valid response, raise a error
	if response.status_code != 200:
		response.raise_for_status()
	#if the request was valid return the response data in a json format
	return response.json()

'''
General put method to connect with the Web API
entryPoint is the api entry point example /users to update a new user(the user should be send in the body)
Parameters is a dict with the parameters of the request
body is a dict with body data
auth still needs to be implemented
'''
def apiUpdate(entryPoint, parameters=None, body=None):
	response = requests.put(config.webApiAddr+'/'+entryPoint, params=parameters, data=body)
	#if the response is not a valid response, raise a error
	if response.status_code != 200:
		response.raise_for_status()
	#if the request was valid return the response data in a json format
	return response.json()

'''
As the expired cache is stored until the same request is called,
a function to free space is required.
'''
def clearCache():
	requests_cache.core.remove_expired_responses()

'''
This module cannot be run as a main
'''
if __name__ != '__main__':
	#Monkey patch requests
	requests_cache.install_cache('../resources/icb_cache', backend='sqlite', expire_after=config.cacheTime*3600)
	#Schedule a cache cleaning every day at the especified time
	schedule.every().day.at(config.clearCacheTime)