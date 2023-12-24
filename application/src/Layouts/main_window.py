# !/usr/bin/env python3

# -*- coding: utf-8 -*-
# main_window.py

#

from application.src.Functions import imports as imp


def main_menu(h, w):
    """Create main menu window layout.
    Return created layout."""

    layout = [[imp.pSG.Column([[imp.pSG.Image(filename = imp.rec, key = "__IMAGE__", size = ((2 * (w // 5)), h))]],
                              element_justification = "left"),
               imp.pSG.Column([[imp.pSG.Text("Texto 1")], [imp.pSG.Text("Texto 2")], [imp.pSG.Button("Botón 1")],
                               [imp.pSG.Button("Botón 2")], [imp.pSG.Multiline("", key = "__MULTILINE__",
                                                                               size = ((3 * (w // 5)), h))]],
                              element_justification = "center")]]

    window = imp.pSG.Window("Fantasy League", layout, disable_close = True, element_justification = "center",
                            size = (w, h), text_justification = "center")

    return window

def login(h,w):
    layout = [
        [imp.pSG.Column([
                    [imp.pSG.HSeparator()],
                    [imp.pSG.Image(filename = imp.fantasy_logo, key = "__IMAGE__", size = ((2 * (w // 5)), h//10))],
                    [imp.pSG.Text("Email:")],
                    [imp.pSG.InputText()]
                ],
                element_justification = "center"
            )
        ]
    ]

    window = imp.pSG.Window("Bienvenido al asistente deportivo de Liga Fantasy del Mundo Deportivo", layout, disable_close = True, element_justification = "center",
                            size = (w, h), text_justification = "center")

    return window