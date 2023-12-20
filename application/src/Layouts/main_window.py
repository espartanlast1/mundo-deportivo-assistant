# !/usr/bin/env python3

# -*- coding: utf-8 -*-
# main_window.py

#

from src.Functions import imports


def main_menu(h, w):
    """Create main menu window layout.
    Return created layout."""

    layout = [[imports.pSG.Column([[imports.pSG.Image(filename = "src/img/recommendation.png", key = "__IMAGE__",
                                    size = ((2 * (w // 5)), h))]], element_justification = "left"),
               imports.pSG.Column([[imports.pSG.Text("Texto 1")], [imports.pSG.Text("Texto 2")],
                                   [imports.pSG.Button("Botón 1")], [imports.pSG.Button("Botón 2")],
                                   [imports.pSG.Multiline("", key = "__MULTILINE__", size = ((3 * (w // 5)), h))]],
                                  element_justification = "center")]]

    window = imports.pSG.Window("Fantasy League", layout, disable_close = True, element_justification = "center",
                                size = (w, h), text_justification = "center")

    return window
