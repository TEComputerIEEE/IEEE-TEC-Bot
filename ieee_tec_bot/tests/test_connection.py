#!/usr/bin/env python
# -*- coding: utf-8 -*-
# IEEE Computer TEC Telegram Bot
'''
Tests for the connection module
'''
import pytest
from ieee_tec_bot import connection as conn
from ieee_tec_bot import config


'''
Test if the connection with the API to get activities is working
'''
def test_activities_get():
	activities = conn.apiGet(config.activitiesEntryPoint)["activities"]
	activity1 = conn.apiGet(config.activitiesEntryPoint, {"branchID":1})["activities"]
	activity2 = conn.apiGet(config.activitiesEntryPoint, {"branchID":1, "chapterID":1})["activities"]
	exist = activities != [] and activity1 !=[] and activity2 !=[]
	assert exist

'''
Test if the format of the format of the returned activity is correct
'''
def test_activities_structure():
	activity = conn.apiGet(config.activitiesEntryPoint)["activities"][0]
	correct = isinstance(activity["activityID"], int) and activity["activityID"] > 0
	correct &= isinstance(activity["name"], str) and len(activity["name"]) > 5
	correct &= isinstance(activity["maxCapacity"], int) and activity["maxCapacity"] > 0
	correct &= isinstance(activity["description"], str) and activity["description"] != ""
	correct &= isinstance(activity["place"], str) and activity["place"] != ""
	correct &= isinstance(activity["date"], str) and activity["date"] != ""
	correct &= isinstance(activity["users"], list)
	correct &= isinstance(activity["flyer"], str) and activity["flyer"] != ""
	assert correct

'''
Test if the connection with the API to get branches is working
'''
def test_branch_get():
	branches = conn.apiGet(config.branchesEntryPoint)["branches"]
	branch = conn.apiGet(config.branchesEntryPoint, {"branchID":1})["branches"]
	exist = len(branches) > 0 and len(branch) > 0
	assert exist

'''
Test if the format of the format of the returned branch is correct
'''
def test_branch_structure():
	branch = conn.apiGet(config.branchesEntryPoint, {"branchID":1})["branches"][0]
	correct = isinstance(branch["branchID"], int) and branch["branchID"] > 0
	correct &= isinstance(branch["college"], str) and len(branch["college"]) > 5
	correct &= isinstance(branch["acronym"], str) and branch["acronym"] != ""
	assert correct


'''
Test if the connection with the API to get contacts is working
'''
def test_contacts_get():
	contacts1 = conn.apiGet(config.contactsEntryPoint, {"branchID":1})["contacts"]
	contacts2 = conn.apiGet(config.contactsEntryPoint, {"branchID":1, "chapterID":1})["contacts"]
	exist =  contacts1 != [] and contacts2 != []
	assert exist

'''
Test if the format of the format of the returned contact is correct
'''
def test_contacts_structure():
	activity = conn.apiGet(config.contactsEntryPoint,  {"branchID":1})["contacts"][0]
	correct = isinstance(activity["contactID"], int) and activity["contactID"] > 0
	correct &= isinstance(activity["name"], str) and activity["name"] != ""
	correct &= isinstance(activity["userName"], str) and activity["userName"] != ""
	correct &= isinstance(activity["role"], str) and activity["role"] != ""
	assert correct

'''
Test if the connection with the API to get chapters is working
'''
def test_chapter_get():
	chapters = conn.apiGet(config.chaptersEntryPoint, {"branchID":1})["chapters"]
	chapter = conn.apiGet(config.chaptersEntryPoint, {"branchID":1, "chapterID":1})["chapters"]
	exist = chapters !=[] and chapter !=[]
	assert exist

'''
Test if the format of the format of the returned chapter is correct
'''
def test_chapter_structure():
	chapter = conn.apiGet(config.chaptersEntryPoint, {"branchID":1, "chapterID":1})["chapters"][0]
	correct = isinstance(chapter["chapterID"], int) and chapter["chapterID"] > 0
	correct &= isinstance(chapter["branchID"], int) and chapter["branchID"] > 0
	correct &= isinstance(chapter["name"], str) and len(chapter["name"]) > 5
	assert correct

'''
Test if the connection with the API to get users is working
'''
def test_user_get():
	user = conn.apiGet(config.usersEntryPoint, {"chatID":1})["users"]
	exist = user != [] 
	assert exist

'''
Test if the format of the format of the returned user is correct
'''
def test_user_structure():
	user = conn.apiGet(config.usersEntryPoint, {"chatID":1})["users"][0]
	correct = isinstance(user["name"], str) and user["name"]!= ""
	correct &= isinstance(user["studentID"], str) and user["studentID"]!= ""
	correct &= isinstance(user["email"], str) and len(user["email"]) > 5
	assert correct

'''
Test if the connection with the API to post is working
'''
def test_post():
	request = conn.apiPost("http://httpbin.org/post",  body={"chatID":1})
	assert len(request) > 0

'''
Test if the connection with the API to put is working
'''
def test_update():
	request = conn.apiUpdate("http://httpbin.org/put", body={"chatID":1})
	assert len(request) > 0