# !/usr/bin/env python3

# -*- coding: utf-8 -*-
# imports.py

#

# CODE NUMBERS
"""
"""

import PySimpleGUI as pSG

from application.src.Layouts import main_window
from os import getcwd
from time import sleep

"""Contains all imports necessary."""


root = getcwd() + "/"
app = root + "application/"
src = app + "src/"
scrape = root + "scrape/"
models = root + "models/"
img = src + "img/"
rec = img + "recommendation.png"
fantasy_logo = img + "mister-fantasy-md-logo.png"
