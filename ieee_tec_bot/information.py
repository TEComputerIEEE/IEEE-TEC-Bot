#!/usr/bin/env python
# -*- coding: utf-8 -*-
# IEEE Computer TEC Telegram Bot
# Information module

import connection as conn
import config


def about():
    '''
    Method that returns the about information formated as is
    '''
    # About info have to be formated here
    aboutText = ["<b>Acerca del Bot</b>\nLorem ipsum dolor sit amet, consectetur\
     adipiscing elit.\n<b>Desarrolladores:</b>\n"]
    contacts = ["⚫ Nombre Completo - @johndoe\n" for i in range(1, 8)]
    aboutText.append(contacts)
    aboutText.append("Para más información visite el proyecto en \
    <a href='https://github.com/TEComputerIEEE/IEEE-TEC-Bot/'>github</a>.")
    return "".join(aboutText)


def IEEEBenefist():
    '''
    Method that give the information of the IEEE membership and send it
    to the main program
    '''
    IEEEBtext = "<b>Oportunidades de crecimiento: </b>\n🔹Competitividad personal.\
                \n🔹Habilidades extracurriculares.\n🔹Capacidad de liderazgo.\n\
                (organizar, dirigir y trabajo en equipo)\n🔹Redes de contactos.\
                \n(sociales y profesionales)\n🔹Pertenencia a una comunidad \
                global.\n(Sociedades Técnicas, Grupos de afinidad y \
                voluntariado)\n🔹Competiciones a nivel local, regional y \
                mundial.\n<b>(premios en efectivo, membresías, artículos \
                electrónicos, viajes a muchas parte del mundo)</b>\n🔹Fondos \
                para desarrollo y ejecución de proyectos\n\n<b>Información \
                Actual y Confiable:</b>\n🔹Libros, revistas, bases de datos, \
                material didáctico, charlas (presenciales y en línea), \
                conferencias (nacionales e internacionales)\n\n<b>Otros \
                Beneficios:\n</b>🔹IEEE Jobs Site, IEEE Mentoring Connection, \
                Reconocimientos y mucho más"
    return IEEEBtext


def chaptersBenefits():
    '''
    Method that give the information of the all chapter benefists and send it
    to the main program----Now only the CS chapter (in develop CAS EBM
    IAS NPSS PES)
    '''
    CBenefistText = "<b>Beneficios de ser miembro de Computer Society:\n</b>\
                    🔹Revista Computer mensual (digital).\n🔹Revista \
                    ComputingEdge mensual (digital).\n🔹Descuentos solo para \
                    miembros a conferencias y eventos.\n🔹Seminarios web solo \
                    para miembros.\n🔹Acceso ilimitado a Computing Now, \
                    computer.org, y a la nueva aplicación móvil myCS.\n🔹<b>\
                    Membresía al Capítulo Computer local.\n</b>🔹<b>Skillsoft \
                    Skillchoice™ Complete</b>, con más de 67.000 libros, \
                    videos, cursos, practices para examen y recursos de \
                    orientación.\n🔹Acceso a 15.000 recursos técnicos y de \
                    negocio en Books24x7.\n🔹30 tokens para la aplicación móvil\
                     myCS.\n🔹Acceso a la Librería Digital de Computer Society."
    return CBenefistText


def membershipSteps():
    '''
    Method that returns the steps to become a IEEE member formated
    '''
    # The URL needs updating
    membershipStepsText = ["<b>Para convertirse en miembro de IEEE</b>\n",
                           "Siga los pasos descritos en el archivo adjunto ",
                           "o visite la dirección \
                           http://bit.ly/IEEE-Guia-Inscripcion."]
    return "".join(membershipStepsText)


def chapterMembershipSteps():
    '''
    Method that returns the steps to become a member of an IEEE chapter
    '''
    # The URL needs updating
    chapterMembershipStepsText = ["<b>Para convertirse en miembro de un \
                                  capítulo de IEEE</b>\n", "Siga los pasos \
                                  descritos en el archivo adjunto ", "o visite\
                                   la dirección \
                                   http://bit.ly/IEEE-Guia-Inscripcion."]
    return "".join(chapterMembershipStepsText)


def listBranches():
    '''
    Method that gets from the api a list of branches
    The connection module use cache to improve response time
    '''
    # Get branches from the API
    branchList = conn.apiGet(config.branchesEntryPoint)["branches"]
    branchNames = []
    # Get only the names of the branches
    for branch in branchList:
        branchNames.append("".join([u"Rama Estudiantil ", branch["college"]]))
    return branchNames


def listChapters(branchName):
    '''
    Method that gets from the api a list of chapters
    branch name is required to search the branch
    The connection module use cache to improve response time
    '''
    branchData = conn.getBranchData(branchName)
    chapterList = conn.apiGet(config.chaptersEntryPoint,
                              {"branchID": branchData["branchID"]})["chapters"]
    chapterNames = []
    for chapter in chapterList:
        chapterNames.append("".join([chapter["name"], u" ",
                            branchData["acronym"]]))
    return chapterNames


def listContacts(branchName, chapterName=None):
    '''
    Method that gets from the api a list of contacts of a branch or chapter
    branch name is required to search the branchs contacts or chapters contacts
    The connection module use cache to improve response time
    '''
    # Api Call stuff
    # contacts=conn.apiGet("contacts",
    # {"branchID":branchData["branchID"]})["contacts"] #if chapterName=None....
    # format the contacts and the response text
    text = "Estos son los contactos de....\n <b>name</b>\n \
    <i>Chair</i>\n@johndoe"
    messages = [{"text": text}]
    return messages
