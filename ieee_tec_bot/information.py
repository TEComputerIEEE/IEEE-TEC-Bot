#!/usr/bin/env python
# -*- coding: utf-8 -*-
# IEEE Computer TEC Telegram Bot
# Information module

import connection as conn
import config

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
Method that give the information of the IEEE membership and send it
to the main program
'''
def IEEEBenefist():
	IEEEBtext="<b>Oportunidades de crecimiento: </b>\n🔹Competitividad personal.\n🔹Habilidades extracurriculares.\n🔹Capacidad de liderazgo.\n(organizar, dirigir y trabajo en equipo)\n🔹Redes de contactos.\n(sociales y profesionales)\n🔹Pertenencia a una comunidad global.\n(Sociedades Técnicas, Grupos de afinidad y voluntariado)\n🔹Competiciones a nivel local, regional y mundial.\n<b>(premios en efectivo, membresías, artículos electrónicos, viajes a muchas parte del mundo)</b>\n🔹Fondos para desarrollo y ejecución de proyectos\n\n<b>Información Actual y Confiable:</b>\n🔹Libros, revistas, bases de datos, material didáctico, charlas (presenciales y en línea), conferencias (nacionales e internacionales)\n\n<b>Otros Beneficios:\n</b>🔹IEEE Jobs Site, IEEE Mentoring Connection, Reconocimientos y mucho más"
	return IEEEBtext
'''
Method that give the information of the all chapter benefists and send it
to the main program----Now only the CS chapter (in develop CAS EBM  IAS NPSS PES)
'''
def chaptersBenefits():
	CBenefistText="<b>Beneficios de ser miembro de Computer Society:\n</b>🔹Revista Computer mensual (digital).\n🔹Revista ComputingEdge mensual (digital).\n🔹Descuentos solo para miembros a conferencias y eventos.\n🔹Seminarios web solo para miembros.\n🔹Acceso ilimitado a Computing Now, computer.org, y a la nueva aplicación móvil myCS.\n🔹<b>Membresía al Capítulo Computer local.\n</b>🔹<b>Skillsoft Skillchoice™ Complete</b>, con más de 67.000 libros, videos, cursos, practices para examen y recursos de orientación.\n🔹Acceso a 15.000 recursos técnicos y de negocio en Books24x7.\n🔹30 tokens para la aplicación móvil myCS.\n🔹Acceso a la Librería Digital de Computer Society."
	return CBenefistText


'''
Method that returns the steps to become a IEEE member formated 
'''
def membershipSteps():
	#The URL needs updating
	membershipStepsText = "<b>Para convertirse en miembro de IEEE</b>\n"
	membershipStepsText += "Siga los pasos descritos en el archivo adjunto "
	membershipStepsText += "o visite la dirección http://bit.ly/IEEE-Guia-Inscripcion."
	return membershipStepsText

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
	branchList = conn.apiGet(config.branchesEntryPoint)["branches"]
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
def listChapters(branchName):
	branchData = conn.getBranchData(branchName)
	chapterList = conn.apiGet(config.chaptersEntryPoint, {"branchID":branchData["branchID"]})["chapters"]
	chapterNames = []
	for chapter in chapterList:
		chapterNames += [chapter["name"]+u" "+branchData["acronym"]]
	return chapterNames


'''
Method that gets from the api a list of contacts of a branch or chapter
branch name is required to search the branchs contacts or chapters contacts
The connection module use cache to improve response time
'''
def listContacts(branchName, chapterName=None):
	#Api Call stuff
	#contacts=conn.apiGet("contacts", {"branchID":branchData["branchID"]})["contacts"] #if chapterName=None.....
	#format the contacts and the response text
	text = "Estos son los contactos de....\n <b>name</b>\n <i>Chair</i>\n@johndoe"
	messages = [{"text":text}]
	return messages
