# !/usr/bin/env python3

# -*- coding: utf-8 -*-
# main_window.py

#

import Utils.helper as h


def login():
    """Create login window."""

    h, w = 210, 320
    new_size = 30
    data_bytes_io = imp.io.BytesIO(imp.base64.b64decode(imp.pSG.EMOJI_BASE64_THINK))
    img = imp.PIL.Image.open(data_bytes_io)
    cur_width, cur_height = img.size
    scale = min((new_size / cur_height), (new_size / cur_width))
    img = img.resize((int(cur_width * scale), int(cur_height * scale)), imp.Resampling.LANCZOS)
    bio = imp.io.BytesIO()
    img.save(bio, format = "PNG")
    new_emoji = imp.base64.b64encode(bio.getvalue())

    layout = [
        [imp.pSG.Column([
            [imp.pSG.Image(filename = imp.fantasy_logo, key = "__IMAGE__", size = (w, (h // 2)))],
            [imp.pSG.Column([[imp.pSG.Text("Login:", justification = "left", size = (10, 1))]]),
             imp.pSG.Column([[imp.pSG.Input(key = "user", size = (25, 10))]])],
            [imp.pSG.Column([[imp.pSG.Text("Password:", justification = "left", size = (10, 1))]],
                            element_justification = "left"),
             imp.pSG.Column([[imp.pSG.Input(enable_events = True, key = "pass", password_char = "*", size = (18, 1)),
                              imp.pSG.Image(new_emoji, enable_events = True, key = "Mostrar"),
                              imp.pSG.Button("login", bind_return_key = True, size = (0, 0))]])]],
                element_justification = "center")]
    ]

    window = imp.pSG.Window("Bienvenido al asistente deportivo de Liga Fantasy del Mundo Deportivo", layout,
                            element_justification = "center", size = (w, h), text_justification = "center")

    return window
