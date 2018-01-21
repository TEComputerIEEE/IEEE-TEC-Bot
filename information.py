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
