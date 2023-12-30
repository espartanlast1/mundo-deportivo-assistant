# !/usr/bin/env python3

# -*- coding: utf-8 -*-
# LigaGUI.py

#

import Utils.helper as helper
import Utils.routes as route


lorca = helper.platform.system()


def custom_login(user, pwd):
    if lorca != "Windows":
        helper.makedirs(helper.path.dirname("/home/221A5673Geronimo/temp_file"), exist_ok = True)

    firefox_options = helper.webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")
    driver = helper.webdriver.Firefox(options = firefox_options)

    driver.set_page_load_timeout(300)

    navigation_to = True
    while navigation_to:
        try:
            driver.get("https://mister.mundodeportivo.com/new-onboarding/auth/email")
            navigation_to = False
        except helper.TimeoutException:
            helper.sleep(2)
            pass

    # Wait for the cookies to appear and click the button to accept them.
    helper.sleep(helper.uniform(0.4, 0.6))
    intercept = True
    while intercept:
        try:
            more = helper.wait_click(driver, (helper.By.ID, "didomi-notice-learn-more-button"), 4)
            if more:
                more.click()
            helper.sleep(helper.uniform(0.4, 0.6))
            button_name = "//button[contains(@class, 'didomi-button-standard') and normalize-space() = 'Rechazar todo']"
            not_consent_button = helper.wait_click(driver, driver.find_element(helper.By.XPATH, button_name), 4)
            driver.execute_script("arguments[0].scrollIntoView(true);", not_consent_button)
            if not_consent_button:
                not_consent_button.click()
            intercept = False
        except (helper.ElementClickInterceptedException, helper.StaleElementReferenceException):
            helper.sleep(6)
            intercept = True
        except helper.NoSuchElementException:
            pass

    # Enter the email and password.
    email_input = driver.find_element(helper.By.ID, "email")
    email_input.send_keys(user)

    password_input = driver.find_element(helper.By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[2]/input')
    password_input.send_keys(pwd)

    # Click on the login button.
    submit_button = helper.wait_click(driver, (helper.By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[3]/button'), 2)
    if submit_button:
        submit_button.click()

    # Special wait to skip the first tutorial, when we start with a new account it will appear, so better to check it.
    helper.skip_button(driver, (helper.By.CLASS_NAME, "btn-tutorial-skip"))

    helper.sleep(helper.uniform(0.4, 0.8))

    return driver


window = helper.main_window.test_tab()

# Bucle principal
k = 0
while True:
    event, values = window.read()

    if event == helper.pSG.WIN_CLOSED or event == 'Salir':
        break
    elif event == '-TABS-':
        # Obtener el nombre de la pestaña activa
        active_tab = values['-TABS-']

        # Actualizar el contenido de la pestaña activa
        if all(active_tab != ext for ext in ["tab1", "tab2"]):
            window[f'{active_tab}_text'].update(value = window[f'{active_tab}_text'].get() + str(k))
    k += 1

window.close()



login = helper.login_window.login()
c, chosen_gif, event, mostrar_password, u = None, None, "pass", False, None

while event != "Aceptar" and event != helper.WIN_CLOSED:
    event, values = login.read()
    if event == "Mostrar":
        mostrar_password = not mostrar_password
        if mostrar_password:
            login["pass"].update(password_char = "")
        else:
            login["pass"].update(password_char = "*")
    elif event == "login":
        if values["user"] and values["pass"]:
            u = values["user"]
            c = values["pass"]
            event = "Aceptar"
            login.close()
            helper.pSG.popup(f"Usuario: {u}\nContraseña: {c}", auto_close = True, auto_close_duration = 2)
        else:
            if values["user"] == "":
                login["user"].set_focus()
            elif values["pass"] == "":
                login["pass"].set_focus()

if u and c:
    loading = [route.image_folder + gif for gif in helper.listdir(route.image_folder) if "gif" in gif]
    chosen_gif = helper.choice(loading)
    # driver = custom_login(u, c)
while not helper.path.exists("xd"):
    helper.pSG.popup_animated(chosen_gif, grab_anywhere = False,
                              location = ((helper.pSG.Window.get_screen_size()[0] // 2) - 60,
                                          (helper.pSG.Window.get_screen_size()[1] // 2) - 80),
                              message = "Downloading data,\nplease be patient...",
                              no_titlebar = True, time_between_frames = 80)

menu_eng = helper.main_window.test_tab()
menu_eng.read()
