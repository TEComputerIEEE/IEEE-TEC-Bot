#!/usr/bin/env python
# -*- coding: utf-8 -*-
# IEEE Computer TEC Telegram Bot
'''
Tests for the information module
'''

import pytest
from ieee_tec_bot import information as info
from ieee_tec_bot import config

'''
Test if the about return a non empty string
'''
def test_about():
	assert isinstance(info.about(), str) and info.about() != ""

'''
Test if the IEEEBenefist return a non empty string
'''
def test_ieee_benefits():
	assert isinstance(info.IEEEBenefist(), str) and info.IEEEBenefist() != ""

'''
Test if the chaptersBenefits return a non empty string
'''
def test_ieee_chapter_benefits():
	assert isinstance(info.chaptersBenefits(), str) and info.chaptersBenefits() != ""

'''
Test if the membershipSteps return a non empty string
'''
def test_membership_steps():
	assert isinstance(info.membershipSteps(), str) and info.membershipSteps() != ""

'''
Test if the chapterMembershipSteps return a non empty string
'''
def test_chapter_membership_steps():
	assert isinstance(info.chapterMembershipSteps(), str) and info.chapterMembershipSteps() != ""

'''
Test if the function is returning branches
'''
def test_list_branches():
	assert isinstance(info.listBranches(), list) and info.listBranches() != ""

'''
Test if the function is returning chapters
'''
def test_list_chapters():
	assert isinstance(info.listChapters("Tecnológico de Costa Rica"), list) and info.listChapters("Tecnológico de Costa Rica") != []

'''
Test if the function is returning the branch data
'''
def test_get_branch_data():
	branch = info.getBranchData("Tecnológico de Costa Rica")
	correct = branch["college"] == u"Tecnológico de Costa Rica"
	correct &= branch["acronym"] == u"TEC"
	assert correct
