#!/usr/bin/env python
# -*- coding: utf-8 -*-
# IEEE Computer TEC Telegram Bot
# Connection module
"""
See https://github.com/TEComputerIEEE/IEEE-TEC-WebAPI for a full list of
entry points and parameters
"""
import requests
import requests_cache
import schedule
import config
import dummyData as data  # just needed for dummy data delete when api is ready
from dateutil import parser  # just needed for dummy data...
from datetime import timezone  # just needed for dummy data...

def apiGet(entryPoint, parameters=None, cache=True):
    '''
    General get method to connect with the Web API, returns json data or raise
    an exception entryPoint is the api entry point example /users to get user
    list(without parameters)
    Parameters is a dict with the parameters of the request
    cache by default all request will be cached to improve response time
    auth still needs to be implemented, and for now it returns just test data
    '''
    # Dummy test data
    return dummyGet(entryPoint, parameters)
    response = requests.get(entryPoint, params=parameters)
    # if the request must not be cached and the response that we get before is
    # cached
    if not cache and response.from_cache:
        # disable cache and get the response
        with requests_cache.disabled():
            response = requests.get(entryPoint, params=parameters)
    # if the response is not a valid response, raise a error
    if response.status_code != 200:
        response.raise_for_status()
    # if the request was valid return the response data in a json format
    return response.json()


def getBranchData(branchName):
    '''
    Method that gets from the api one specific branch by name
    branch name is required to search the branch
    The connection module use cache to improve response time
    '''
    if branchName == "":
        raise Exception("Cannot search a branch with an empty branch name.")
    # Get all branches from api
    branchList = apiGet(config.branchesEntryPoint)["branches"]
    # Search for the branch and return the branchData
    for branch in branchList:
        if(branch["college"] in branchName):
            return branch
    raise Exception("The Branch '%s' cannot be found.", branchName)


def getBranchDataName(branchID = None):
    '''
    Method that gets from the api one specific branch by ID,
    branchID is required to search the branch
    The connection module use cache to improve response time
    '''
    if branchID is None:
        raise Exception("branchID not provided.")
    # Get all branches from api
    branchList = apiGet(config.branchesEntryPoint)["branches"]
    # Search for the branch and return the branchData
    for branch in branchList:
        if(branch["branchID"] == branchID):
            return branch
    raise Exception("The Branch '%s' cannot be found.", branchID)


def getAllBranchesID():
    '''
    Method that gets from the api all the branchIDs,
    '''
    

def getChapterData(branchName, chapterName):
    '''
    Method that gets from the api one specific branch by name
    branch name is required to search the branch
    The connection module use cache to improve response time
    '''
    if chapterName == "":
        raise Exception("Cannot search a chapter with an empty branch name.")

    if chapterName == "":
        raise Exception("Cannot search a chapter with an empty chapter name.")

    branch = {}
    try:
        branch = getBranchData(branchName)

    except ValueError as e:
        raise Exception("The chapter '%s' cannot be found. Because the \
branch '%s'", chapterName, e)

    chapterList = apiGet(config.chaptersEntryPoint,
                         parameters={"branchID":
                                     branch["branchID"]})["chapters"]
    for chapter in chapterList:
        if(chapter["name"] in chapterName):
            return chapter

    raise Exception("The chapter '%s' cannot be found.", chapterName)


def dummyGet(entryPoint, parameters=None):
    '''
    Dummy test data to be used insted of the Web API
    DONT call it directly use the apiGet funct instead
    See https://github.com/TEComputerIEEE/IEEE-TEC-WebAPI/issues/3 for full
    dummy data entry points and params
    '''
    if entryPoint == config.activitiesEntryPoint:
        activities = {"activities": []}
        if parameters is None:
            # For every branch in the branches json
            for branch in data.branches["branches"]:
                # add the activities of that branch to a dict
                activities.update({"activities":
                                   activities["activities"] +
                                   branch["activities"]})
            # For every chapter in the branches json
            for chapter in data.chapters["chapters"]:
                # add the activities of that branch to a dict
                activities.update({"activities":
                                   activities["activities"] +
                                   chapter["activities"]})
            # returns all IEEE activities
            return activities

        # if the branch ID is in the parameters
        elif "branchID" in parameters.keys():
            # if the chapter ID is in the parameters then search for branch and
            # chapter
            if "chapterID" in parameters.keys():
                # For every chapter in the chapters json
                for chapter in data.chapters["chapters"]:
                    # return the activity if the ids are equal
                    if(chapter["chapterID"] == parameters["chapterID"] and
                       chapter["branchID"] == parameters["branchID"]):
                        if not("activityID" in parameters.keys()):
                            return {"activities": chapter["activities"]}
                        else:
                            for activity in chapter["activities"]:
                                if(activity["activityID"] ==
                                   parameters["activityID"]):
                                    return {"activities": [activity]}
                            raise ValueError("No branchID + chapterID + acti\
vityID combination found")
                raise ValueError("No branchID + chapterID combination found")

            # else just search for branch activities
            else:
                # For every branch in the branches json
                for branch in data.branches["branches"]:
                    # return the activity if the ids are equal
                    if(branch["branchID"] == parameters["branchID"]):
                        if not("activityID" in parameters.keys()):
                            return {"activities": branch["activities"]}
                        else:
                            for activity in branch["activities"]:
                                if(activity["activityID"] ==
                                   parameters["activityID"]):
                                    return {"activities": [activity]}
                            raise ValueError("No branchID + activityID combina\
tion found")

                raise ValueError("BranchID '%d' not found",
                                 parameters["branchID"])
        else:
            raise ValueError("No valid parameters")

    elif entryPoint == config.branchesEntryPoint:
        branches = {"branches": []}
        if parameters is None:
            # For every branch in the branches json
            for branch in data.branches["branches"]:
                # add the branch data to a dict
                branches.update({"branches":
                                 branches["branches"]+[{"branchID":
                                                        branch["branchID"],
                                                        "college":
                                                        branch["college"],
                                                        "acronym":
                                                        branch["acronym"]}]})
            return branches
        elif "branchID" in parameters.keys():
            # For every branch in the branches json
            for branch in data.branches["branches"]:
                # return the branch data if the ids are equal
                if(branch["branchID"] == parameters["branchID"]):
                    return {"branches": [{"branchID": branch["branchID"],
                                          "college": branch["college"],
                                          "acronym": branch["acronym"]}]}
            raise ValueError("BranchID not found")
        else:
            raise ValueError("No valid parameters")

    elif entryPoint == config.chaptersEntryPoint:
        chapters = {"chapters": []}
        if parameters is None:
            # For every chapter in the chapters json
            for chapter in data.chapters["chapters"]:
                # add the chapter data to a dict
                chapters.update({"chapters":
                                 chapters["chapters"]+[{"chapterID":
                                                        chapter["chapterID"],
                                                        "name":
                                                        chapter["name"],
                                                        "branchID":
                                                        chapter["branchID"]}]})
            return chapters

        elif "branchID" in parameters.keys():
            if "chapterID" in parameters.keys():
                # For every chapter in the chapters json
                for chapter in data.chapters["chapters"]:
                    # return the chapter data if the ids are equal
                    if(chapter["branchID"] == parameters["branchID"] and
                       chapter["chapterID"] == parameters["chapterID"]):
                        return {"chapters": [{"chapterID": ["chapterID"],
                                              "name": chapter["name"],
                                              "branchID": chapter["branchID"]}]
                                }

                raise ValueError("No branchID + chapterID combination found")

            else:
                # For every chapter in the chapters json
                for chapter in data.chapters["chapters"]:
                    # add the chapter data to a dict if the branch ids are ==
                    if(chapter["branchID"] == parameters["branchID"]):
                        chapters.update({"chapters":
                                         chapters["chapters"] +
                                         [{"chapterID": chapter["chapterID"],
                                           "name": chapter["name"], "branchID":
                                           chapter["branchID"]}]})
                return chapters
        else:
            raise ValueError("No valid parameters")

    elif entryPoint == config.contactsEntryPoint:
        # if the branch ID is in the parameters
        if "branchID" in parameters.keys():
            # if the chapter ID is in the parameters then search for branch and
            # chapter contacts
            if "chapterID" in parameters.keys():
                # For every chapter in the chapters json
                for chapter in data.chapters["chapters"]:
                    # return the contacts if the ids are equal
                    if(chapter["chapterID"] == parameters["chapterID"] and
                       chapter["branchID"] == parameters["branchID"]):
                        return {"contacts": chapter["contacts"]}

                raise ValueError("No branchID + chapterID combination found")

            # else just search for branch contacts
            else:
                # For every branch in the branches json
                for branch in data.branches["branches"]:
                    # return the contacts if the ids are equal
                    if(branch["branchID"] == parameters["branchID"]):
                        return {"contacts": branch["contacts"]}

                raise ValueError("BranchID not found")

        else:
            raise ValueError("No valid parameters")

    elif entryPoint == config.usersEntryPoint:
        # if no parameters return all users
        if parameters is None:
            return data.users
        elif "chatID" in parameters:
            # search for the user
            for user in data.users["users"]:
                # return the contacts if the ids are equal
                if(user["chatID"] == parameters["chatID"]):
                    return {"users": [user]}
            raise ValueError("No user find with that id")
        else:
            raise ValueError("No valid parameters")
    
    elif entryPoint == config.notificationsEntryPoint:
        print ("estoy en entryPoint")
        print (parameters)
        
        if parameters is None:
            raise ValueError("No valid parameters")
        
        if "branchID" in parameters:
            for branch in data.branches["branches"]:
                if int(branch["branchID"]) == int(parameters["branchID"]):
                    if "chapterID" in parameters:
                        for chapter in data.chapters["chapters"]:
                            if chapter["chapterID"] == parameters["chapterID"]:
                                # If chatID is provided returns same chatID if it's subscribed.
                                # if it's not subscribed returns []
                                if "chatID" in parameters: 
                                    for user in chapter["users"]:
                                        if user["chatID"] == parameters["chatID"]:
                                            return parameters["chatID"]
                                    return []
                                # If chatID is not provided returns all users from Chapter.
                                # IMPLEMENT A for TO RETURN ONLY CHATIDs
                                return chapter["users"]

                    # If chapterID is not provided returns all users from Branch.
                    else:
                        # If chatID is provided returns same chatID if it's subscribed.
                        # if it's not subscribed returns []
                        if "chatID" in parameters: 
                            for user in branch["users"]:
                                if int(user["chatID"]) == int(parameters["chatID"]):
                                    return parameters["chatID"]
                            return []
                        # If chatID is not provided returns all users from Branch.
                        # IMPLEMENT A for TO RETURN ONLY CHATIDs
                        return branch["users"]
                        #return [ user["chatID"] for user in branch["users"] ] 
        else: 
            raise ValueError("No branchID provided")

    else:
        raise ValueError('Invalid entry point')


def apiPost(entryPoint, body, parameters=None):
    '''
    General post method to connect with the Web API
    entryPoint is the api entry point example /users to post a new
    user(the user should be send in the body)
    Parameters is a dict with the parameters of the request
    body is a dict with body data
    auth still needs to be implemented
    '''
    return dummyPost(entryPoint, body, parameters)
    response = requests.post(entryPoint, params=parameters, data=body)
    # if the response is not a valid response, raise a error
    if response.status_code != 200:
        response.raise_for_status()
    # if the request was valid return the response data in a json format
    return response.json()


def dummyPost(entryPoint, body, parameters=None):
    '''
    Dummy method to add some things on the dict(the changes will not be
    stored on disk, just memmory)
    '''
    if entryPoint == config.usersEntryPoint:
        if "chatID" in body.keys():
            chat_id = body["chatID"]
            user = list(filter(lambda user: user['chatID'] == chat_id,
                               data.users["users"]))
            if len(user) == 0:
                if "name" in body.keys():
                    if "studentID" in body.keys():
                        if "email" in body.keys():
                            name = body["name"]
                            studentID = body["studentID"]
                            email = body["email"]
                            data.users.update({"users":
                                               data.users["users"] +
                                               [{"chatID": chat_id,
                                                 "name": name,
                                                 "email": email,
                                                 "studentID": studentID}]})
                            return {"status_code": 200}
                        else:
                            raise ValueError("No email provided")
                    else:
                        raise ValueError("No student Id provided")
                else:
                    raise ValueError("No name provided")
            else:
                raise ValueError("User already exist")
        else:
            raise ValueError("No Chat Id provided")

    else:
        raise ValueError("No valid entry point for post")


def apiUpdate(entryPoint, body, parameters=None):
    '''
    General put method to connect with the Web API
    entryPoint is the api entry point example /users to update a new
    user(the user should be send in the body)
    Parameters is a dict with the parameters of the request
    body is a dict with body data
    auth still needs to be implemented
    '''
    return dummyUpdate(entryPoint, parameters=parameters, body=body)
    response = requests.put(entryPoint, params=parameters, data=body)
    # if the response is not a valid response, raise an error
    if response.status_code != 200:
        response.raise_for_status()
    # if the request was valid return the response data in a json format
    return response.json()


def dummyUpdate(entryPoint, body, parameters=None):
    '''
    Dummy method to update some things on the dict(the changes will not be
    stored on disk, just memmory)
    '''
    if entryPoint == config.registerEntryPoint:
        if parameters is None:
            raise ValueError("No parameters where provided")
        if "chatID" in parameters.keys():
            chat_id = parameters["chatID"]
            notify = False
            if "notify" in parameters.keys():
                notify = parameters["notify"]
            user = list(filter(lambda user: user['chatID'] == chat_id,
                               data.users["users"]))
            alreadyExist = True if user != [] else False
            if alreadyExist:
                if "branchID" in parameters.keys():
                    branchID = parameters["branchID"]
                    if "activityID" in parameters.keys():
                        activityID = parameters["activityID"]
                        if "chapterID" in parameters.keys():
                            chapterID = parameters["chapterID"]
                            chapter = list(filter(
                                           lambda chapter:
                                           (chapter['chapterID'] == chapterID
                                            and
                                            chapter["branchID"] == branchID),
                                           data.chapters["chapters"]))
                            if len(chapter) != 1:
                                raise ValueError("The chapter cannot be found",
                                                 branchID, chapterID)
                            activity = list(filter(
                                            lambda acti:
                                            acti['activityID'] == activityID,
                                            chapter[0]["activities"]))
                            if len(activity) != 1:
                                raise ValueError("The activity can't be found",
                                                 branchID, chapterID,
                                                 activityID)
                            user = list(filter(lambda user:
                                               user["chatID"] == chat_id,
                                               activity[0]["users"]))
                            # Dummy way to update that big structure
                            # Delete and then append new element
                            data.chapters["chapters"].remove(chapter[0])
                            chapter[0]["activities"].remove(activity[0])
                            if len(user) == 0:
                                # First check if there's space left
                                if(activity[0]["maxCapacity"] >
                                   len(activity[0]["users"])):
                                    # If the user is not on the list then
                                    # register them
                                    activity[0].update({"users":
                                                        activity[0]["users"] +
                                                        [{"chatID": chat_id,
                                                          "notify": notify}]})
                                    # Parse Date
                                    date = parser.parse(activity[0]["date"])
                                    # Transform to local timezone
                                    date = (date.replace(tzinfo=timezone.utc).
                                            astimezone(tz=None))
                                    dateStr = date.strftime("%A %d de %B %Y. \
a las %I:%M %p")
                                    message = "".join(["Su registro a la \
actividad <b>", activity[0]["name"], "</b> se realizó correctamente. Recuerde \
que la misma se realizará el día ", dateStr])
                                else:
                                    message = "".join(["Su registro a la \
actividad <b>", activity[0]["name"], "</b> no se pudo realizar ya que se ha \
excedido la cantidad máxima para este evento. Puede intentar contactar a un \
representante para ver si se puede realizar algo al respecto...(Aquí adjuntar\
adjuntar info de representantes del capítulo o rama)"])
                            else:
                                # Remove the user from the registered list
                                activity[0]["users"].remove(user[0])
                                message = "".join(["Se ha cancelado su registro a la \
actividad <b>", activity[0]["name"], "</b>. Algo más....."])
                            # Then just sum up
                            chapter[0]["activities"].append(activity[0])
                            data.chapters["chapters"].append(chapter[0])
                            return {"message": message}
                        else:
                            branch = list(filter(
                                            lambda branch:
                                            branch["branchID"] == branchID,
                                            data.branches["branches"]))
                            if len(branch) != 1:
                                raise ValueError("The branch cannot be found",
                                                 branchID)
                            activity = list(filter(
                                              lambda acti:
                                              acti['activityID'] == activityID,
                                              branch[0]["activities"]))
                            if len(activity) != 1:
                                raise ValueError("The activity can't be found",
                                                 branchID, activityID)
                            user = list(filter(
                                          lambda user:
                                          user["chatID"] == chat_id,
                                          activity[0]["users"]))
                            # Dummy way to update that big structure
                            # Delete and then append new element
                            data.branches["branches"].remove(branch[0])
                            branch[0]["activities"].remove(activity[0])
                            if len(user) == 0:
                                # First check if there's space left
                                if(activity[0]["maxCapacity"] >
                                   len(activity[0]["users"])):
                                    # If the user is not on the list then
                                    # register them
                                    activity[0].update({"users":
                                                        activity[0]["users"] +
                                                        [{"chatID": chat_id,
                                                          "notify": notify}]})
                                    # Parse Date
                                    date = parser.parse(activity[0]["date"])
                                    # Transform to local timezone
                                    date = (date.replace(tzinfo=timezone.utc).
                                            astimezone(tz=None))
                                    dateStr = date.strftime("%A %d de %B %Y \
a las %I:%M %p")
                                    message = "".join(["Su registro a la \
actividad <b>", activity[0]["name"], "</b> se realizó correctamente. Recuerde \
que la misma se realizará el día ", dateStr])
                                else:
                                    message = "".join(["Su registro a la \
actividad <b>", activity[0]["name"], "</b> no se pudo realizar ya que se ha \
excedido la cantidad máxima para este evento. Puede intentar contactar a un \
representante para ver si se puede realizar algo al respecto...(Aquí adjuntar\
adjuntar info de representantes del capítulo o rama)"])
                            else:
                                # Remove the user from the registered list
                                activity[0]["users"].remove(user[0])
                                message = "".join(["Se ha cancelado su registro a la \
actividad <b>", activity[0]["name"], "</b>. Algo más....."])
                            # Then just sum up
                            branch[0]["activities"].append(activity[0])
                            data.branches["branches"].append(branch[0])
                            return {"message": message}
                    else:
                        raise ValueError("No Activity Id Provided")
                else:
                    raise ValueError("No Branch ID provided")
        else:
            raise ValueError("No chat id provided")
    
    elif entryPoint == config.notificationsEntryPoint:
        message = []
        if parameters is None:
            raise ValueError("No valid parameters")
            return {"message": message}
        elif "branchID" in parameters:
            for branch in data.branches["branches"]:
                if str(branch["branchID"]) == str(parameters["branchID"]):
                    if "chapterID" in parameters:
                        for chapter in data.chapters["chapters"]:
                            if str(chapter["chapterID"]) == str(parameters["chapterID"]):
                                # Update users in Chapter.
                                # If it's subscribed then unsubscribe, or viceversa.
                                for user in chapter["users"]:
                                    if int(user["chatID"]) == int(body["chatID"]):
                                        # Remove user
                                        chapter["users"].remove({'chatID': int(body["chatID"])})
                                        
                                        message = "".join(["La suscripción a las notificaciones de <b>",
                                         chapter["name"],"</b> ha sido cancelada. No recibirá más notificaciones."])
                                        return {"message": message}
                                # Add user 
                                chapter["users"].append({'chatID': int(body["chatID"])})
                                message = "".join(["La suscripción a las notificaciones de <b>",
                                chapter["name"],"</b> se realizó correctamente. Recibirá solamente una notificación semanal."])
                                return {"message": message}
                    else:
                        # If chapterID is not provided update users in Branch.
                        # If it's subscribed then unsubscribe, or viceversa.
                        print ("ES UNA RAMA, VAMO' A ACTUALIZAR")
                        for user in branch["users"]:
                            if int(user["chatID"]) == int(body["chatID"]):
                                # Remove user
                                branch["users"].remove({'chatID': int(body["chatID"])})
                                
                                message = "".join(["La suscripción a las notificaciones de Rama Estudiantil <b>",
                                branch["college"],"</b> ha sido cancelada. No recibirá más notificaciones."])
                                return {"message": message}
                        # Add user 
                        branch["users"].append({'chatID': int(body["chatID"])})
                        
                        message = "".join(["La suscripción a las notificaciones de Rama Estudiantil <b>",
                        branch["college"],"</b> se realizó correctamente. Recibirá solamente una notificación semanal."])
                        return {"message": message}

            raise ValueError("branchID not founded.")
            return {"message": message}
        else: 
            raise ValueError("No branchID provided.")
            return {"message": message}
    else:
        raise ValueError('Invalid entry point')


def clearCache():
    '''
    As the expired cache is stored until the same request is called,
    a function to free space is required.
    '''
    requests_cache.core.remove_expired_responses()


if __name__ != '__main__':  # This module cannot run as main
    # Monkey patch requests
    requests_cache.install_cache('../resources/icb_cache', backend='sqlite',
                                 expire_after=config.cacheTime*3600)
    # Schedule a cache cleaning every day at the especified time
    schedule.every().day.at(config.clearCacheTime).do(clearCache)
