# !/usr/bin/env python3

# -*- coding: utf-8 -*-
# main_window.py

#

import Utils.helper as helper
import Utils.routes as route


def test_tab():

    height, width = ((helper.pSG.Window.get_screen_size()[1] // 100) * 100),\
                    ((helper.pSG.Window.get_screen_size()[0] // 50) * 50)
    # Definir el contenido de las pestañas
    if not helper.path.exists(route.current_path + str(height) + str(width) + ".png"):
        helper.create_image(route.current_alignment, )
    if not helper.path.exists(route.recommendation_path + str(height) + str(width) + ".png"):
        helper.create_image(route.future_alignment)

    current = route.current_path + str(height) + str(width) + ".png"
    recommendation = route.recommendation_path + str(height) + str(width) + ".png"
    tab1_layout = [
        [
            helper.pSG.Column([
                [helper.pSG.Text("Personal Team Title")],
                [helper.pSG.Image(filename = current, key = "personal_team", size = (width // 2, height))]
            ], element_justification = "center", size = (width // 2, height))
        ]
    ]

    tab2_layout = [[
            helper.pSG.Column([
                [helper.pSG.Text("Personal Team Title")],
                [helper.pSG.Image(filename = current, key = "personal_team", size = (width // 2, height))]
            ], element_justification = "center", size = (width // 2, height)),
            helper.pSG.Column([
                [helper.pSG.Text("Market Team Title")],
                [helper.pSG.Image(filename = recommendation, key = "market_team", size = (width // 2, height))]
            ], element_justification = "center", size = (width // 2, height))
        ]
    ]

    tab3_layout = [
        [helper.pSG.Text("Contenido inicial de la pestaña 3", key = "tab3_text")],
    ]

    tab4_layout = [
        [helper.pSG.Text("Contenido inicial de la pestaña 4", key = "tab4_text")],
    ]

    # Diseño principal con pestañas
    layout = [
        [helper.pSG.TabGroup([
            [helper.pSG.Tab("Mi equipo", tab1_layout, element_justification = "center", key = "tab1")],
            [helper.pSG.Tab("Equipo ideal", tab2_layout, element_justification = "center", key = "tab2")],
            [helper.pSG.Tab("Predicciones de valor mis jugadores", tab3_layout, element_justification = "center",
                            key = "tab3")],
            [helper.pSG.Tab("Predicciones de valor jugadores de mercado", tab4_layout, element_justification = "center",
                            key = "tab4")]
        ], enable_events = True, key = "-TABS-", size = (width, (height - 50)))],
        [helper.pSG.Button("Salir")]
    ]

    window = helper.pSG.Window("Ejemplo de Pestañas en PySimpleGUI", layout, background_color = "yellow",
                               location = (10, 10), size = (width, height))

    return window

    # Bucle principal
