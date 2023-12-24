# !/usr/bin/env python3

# -*- coding: utf-8 -*-
# LigaGUI.py

#

import application.src.Functions.imports as imp

print(imp.root)
login = imp.main_window.login(600,1000)
login.read()

menu_eng = imp.main_window.main_menu(450, 750)
menu_eng.read()
