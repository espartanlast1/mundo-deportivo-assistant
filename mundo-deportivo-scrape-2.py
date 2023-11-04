import csv
import http.client
import json
import os
import pandas
import shutil
import time

from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# Folder list.
league_folder = "data/league/"
players_folder = "data/players/"
api_folder = "data/api/"
temp1_folder = "data/temp1/"
temp2_folder = "data/temp2/"
temp3_folder = "data/temp3/"
backup_folder = "data/backup/"

# File list.
market_file = "data/league/fantasy-players-in-market.csv"
personal_team_file = "data/league/fantasy-personal-team-data.csv"
players_meta_data_file = "data/players/fantasy-metadata-players.csv"
temp_meta_data_file = "data/temp1/fantasy-metadata_"
temp_market_info_file = "data/temp2/fantasy-market_"
temp_game_week_file = "data/temp3/fantasy-game_week_"
players_market_info_file = "data/players/fantasy-market-variation.csv"
players_game_week_stats_file = "data/players/fantasy-games-week-players-stats.csv"
player_links_file = "data/players/fantasy-players-links.csv"
team_data_file = "data/league/fantasy-teams-data.csv"
teams_players_file = "data/league/fantasy-teams-players.csv"
standings_file = "data/api/standings-la-liga.csv"

# Gameweek headers.
players_game_week_header = ["Player full name", "Game Week", "AS Score", "Marca Score",
                            "Mundo Deportivo Score", "Sofa Score", "Stat 1", "Stat 2", "Stat 3", "Stat 4", "Stat 5",
                            "Stat 6", "Stat 7", "Stat 8", "Stat 9", "Stat 10", "Stat 11", "Stat 12", "Stat 13",
                            "Stat 14", "Stat 15", "Stat 16", "Stat 17", "Stat 18", "Stat 19", "Stat 20", "Stat 21",
                            "Stat 22", "Stat 23", "Stat 24", "Stat 25", "Stat 26", "Stat 27", "Stat 28", "Stat 29",
                            "Stat 30"]

spanish_list = ["player full name", "game week", "as score", "marca score", "mundo deportivo score", "sofa score",
                "pases totales", "pases precisos", "balones en largo totales", "balones en largo precisos",
                "centros totales", "centros precisos", "despejes totales", "despejes en la línea de gol",
                "duelos aéreos perdidos", "duelos aéreos ganados", "duelos perdidos", "duelos ganados", "regateado",
                "pérdidas", "regates totales", "regates completados", "despejes por alto", "despejes con los puños",
                "errores que llevan a disparo", "errores que llevan a gol", "tiros fuera", "tiros a puerta",
                "tiros bloqueados en ataque", "tiros bloqueados en defensa", "ocasiones creadas", "asistencias de gol",
                "tiros al palo", "ocasiones claras falladas", "penaltis cometidos", "penaltis provocados", "goles",
                "paradas desde dentro del área", "paradas", "goles evitados", "intercepciones", "salidas totales",
                "salidas precisas", "entradas totales", "faltas recibidas", "faltas cometidas", "fueras de juego",
                "minutos jugados", "toques", "posesiones perdidas", "goles esperados", "pases clave",
                "match_stat_expectedassists"]

english_list = ["Player full name", "Game Week", "AS Score", "Marca Score", "Mundo Deportivo Score", "Sofa Score",
                "Total Passes", "Accurate Passes", "Total Long Balls", "Accurate Long Balls", "Total Crosses",
                "Accurate Crosses", "Total clearances", "Clearances on goal line", "Aerial Duels Lost",
                "Aerial Duels Won", "Duels Lost", "Duels Won", "Dribbled Past", "Losses", "Total Dribbles",
                "Completed dribbles", "High clearances", "Fist clearances", "Failures that lead to shot",
                "Failures that lead to goal", "Shots Off Target", "Shots on Target", "Shots blocked in attack",
                "Shots blocked in defence", "Occasions created", "Goal assists", "Shots to the crossbar",
                "Failed obvious occasions", "Penalties commited", "Penalties caused", "Goals",
                "Stops from inside the area", "Stops", "Goals avoided", "Interceptions", "Total outputs",
                "Precise outputs", "Total Tackles", "Fouls Received", "Fouls Committed", "Offsides", "Minutes Played",
                "Touches", "Possessions Lost", "Expected Goals", "Key Passes", "Expected Assists", "Timestamp"]


def wait_click(driv, selector):
    wait = WebDriverWait(driv, 10)
    elemento = wait.until(ec.element_to_be_clickable(selector))
    return elemento


def write_to_csv(file_path, header, data):
    os.makedirs(os.path.dirname(file_path), exist_ok = True)

    # Create a CSV with all the previous information mentioned.
    with open(file_path, "w", encoding = "utf-8", newline = "") as archivo_csv:
        writer = csv.writer(archivo_csv)
        # Write the header
        writer.writerow(header)
        # Append the data
        writer.writerows(data)


def login_fantasy_mundo_deportivo():

    with open("config.json", "r", encoding = "utf-8") as cf:
        c = json.load(cf)

    email_fantasy = c["email"]
    password_fantasy = c["password"]

    # driver = webdriver.Chrome()
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")

    firefox_options = webdriver.FirefoxOptions()
    # firefox_options.add_argument("--headless")
    # firefox_service = webdriver.FirefoxService(executable_path = "/usr/local/bin/geckodriver")
    driver = webdriver.Firefox(options = firefox_options)  # , service = firefox_service)

    mundo_deportivo_liga_fantasy = "https://mister.mundodeportivo.com/new-onboarding/auth/email"
    driver.get(mundo_deportivo_liga_fantasy)

    # Wait for the cookies to appear and click the button to accept them.
    button_cookies = wait_click(driver, (By.ID, "didomi-notice-agree-button"))
    button_cookies.click()

    # Enter the email and password.
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(email_fantasy)

    password_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[2]/input')
    password_input.send_keys(password_fantasy)

    # Click on the login button.
    submit_button = wait_click(driver, (By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[3]/button'))
    submit_button.click()

    # Special wait to skip the first tutorial, when we start with a new account it will appear, so better to check it.
    try:
        skip_button = wait_click(driver, (By.CLASS_NAME, "btn-tutorial-skip"))
        skip_button.click()
    except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
        # Element not found, we just continue.
        pass

    return driver


def scrape_market_section_fantasy():
    driver = login_fantasy_mundo_deportivo()

    # Select the markets section, wait ten seconds as it usually takes some time to load the page.
    driver.get("https://mister.mundodeportivo.com/market")

    # Get the players' data table.
    market_players_table = driver.find_element(By.ID, "list-on-sale")

    # Select each player.
    market_players_info = market_players_table.find_elements(By.CLASS_NAME, "player-row")

    # Create an array to save players info.
    players = []

    for market_player_info in market_players_info:
        # Split the text to create a list of player information.
        raw_player_information = market_player_info.text.split("\n")

        # Clean the data.
        cleaned_player_information = [item.replace("↑", "").replace("↓", "").replace(",", ".") for item in
                                      raw_player_information]
        players.append(cleaned_player_information)

    # ------ Start process to save all the information in a CSV. ------
    # Create first row of the CSV file.
    market_structure_header = ["Points", "Full name", "Market value", "Average value", "Ante penultimate match score",
                               "Penultimate match score", "Last match score", "Attempt to buy"]
    write_to_csv(market_file, market_structure_header, players)
    driver.quit()


def scrape_personal_team_fantasy():
    driver = login_fantasy_mundo_deportivo()

    driver.get("https://mister.mundodeportivo.com/team")

    team_players_table = driver.find_element(By.CLASS_NAME, "player-list")

    # Select each player.
    team_players_info = team_players_table.find_elements(By.CLASS_NAME, "info")

    # Create an array to save players info.
    players = []

    for team_player_info in team_players_info:
        # Split the text to create a list of player information.
        raw_player_information = team_player_info.text.split("\n")

        # Clean the data.
        cleaned_player_information = [item.replace("↑", "").replace("↓", "").replace(",", ".").strip() for item in
                                      raw_player_information]
        players.append(cleaned_player_information)

    # ------- Start process to save all the information in a CSV. --------

    # Create first row of the CSV file.
    team_players_header = ["Name", "Market value", "Average value", "Ante penultimate match score",
                           "Penultimate match score", "Last match score"]
    write_to_csv(personal_team_file, team_players_header, players)

    driver.quit()


def scrape_all_players_fantasy():
    """
    Function that gets all the fantasy players URLs and save them into a CSV file.
    """
    driver = login_fantasy_mundo_deportivo()

    # Go directly to URL
    driver.get("https://mister.mundodeportivo.com/more#players")

    # Set a maximum number of attempts to click the button (optional)
    max_attempts = 15
    attempt = 1
    button_exists = True

    # Create a loop to continuously check for the button's existence
    while button_exists and attempt <= max_attempts:
        try:
            # Now, wait for the button to be clickable
            more_players_button = wait_click(driver, (By.CLASS_NAME, "search-players-more"))
            # Click the button
            more_players_button.click()
            # Give some time for content to load (you can adjust this sleep duration as needed)
            time.sleep(4)
            # Increment the attempt counter
            attempt += 1
        except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
            # The button is not found, set the flag to False
            button_exists = False

    # After the loop, perform another action if the button no longer exists
    if not button_exists:
        # Wait for the players' table to be clickable
        players_table = wait_click(driver, (By.CLASS_NAME, "player-list"))
        link_elements = players_table.find_elements(By.CSS_SELECTOR, "a.btn-sw-link")
        hrefs = [link.get_attribute("href") for link in link_elements]
        data = [[url] for url in hrefs]

        os.makedirs(os.path.dirname(player_links_file), exist_ok = True)

        with open(player_links_file, "w", encoding = "utf-8", newline = "") as file:
            writer = csv.writer(file)
            writer.writerows(data)

    driver.quit()


def scrape_players_stats_fantasy():
    with open(player_links_file, "r", encoding = "utf-8") as file:
        reader = csv.reader(file)
        url_csv_file = list(reader)

    driver = login_fantasy_mundo_deportivo()

    # Special wait to skip the first tutorial, when we start with a new account it will appear, so better to check it.
    try:
        skip_button = wait_click(driver, (By.CLASS_NAME, "btn-tutorial-skip"))
        skip_button.click()
    except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
        # Element not found, we just continue.
        pass

    # Displaying the contents of the CSV file
    for row in url_csv_file:
        for url in row:
            driver.get(url)

            # ------ Store players metadata ------
            scrape_fantasy_players_meta_data(driver)
            # Get all the information to call the CSV according to the player name and surname.
            players_info = driver.find_element(By.XPATH, '//*[@id="content"]/div[5]/div[1]/div/div[1]')
            players_name = players_info.find_element(By.CLASS_NAME, "name").text
            players_surname = players_info.find_element(By.CLASS_NAME, "surname").text
            player_complete_name = players_name + players_surname
            # ------ Store players value table ------
            scrape_fantasy_players_value_table(driver, player_complete_name)
            # ------ Store players game week ------
            scrape_fantasy_players_game_week(driver, player_complete_name)

    driver.quit()
    clean_meta_data_variation()
    clean_market_variation()
    clean_game_week_variation()


def scrape_fantasy_players_meta_data(driver):
    # Get all the information to call the CSV according to the player name and surname.
    players_info = driver.find_element(By.XPATH, '//*[@id="content"]/div[5]/div[1]/div/div[1]')
    players_name = players_info.find_element(By.CLASS_NAME, "name").text
    players_surname = players_info.find_element(By.CLASS_NAME, "surname").text
    player_complete_name = players_name + players_surname

    # Get all the player's metadata.
    players_meta_data_header = ["Player full name", "Current Value", "Points", "Average", "Matches", "Goals", "Cards",
                                "Time Stamp"]

    player_wrapper = driver.find_elements(By.CSS_SELECTOR, "div.player-stats-wrapper div.value")

    valor_actual = player_wrapper[0].text
    puntos = player_wrapper[1].text
    media = player_wrapper[2].text.replace(",", ".")
    partidos = player_wrapper[3].text
    goles = player_wrapper[4].text
    tarjetas = player_wrapper[5].text
    time_stamp = str(datetime.now())

    player_meta_data_row = [player_complete_name, valor_actual, puntos, media, partidos, goles, tarjetas, time_stamp]

    write_to_csv(temp_meta_data_file + player_complete_name + ".csv", players_meta_data_header, player_meta_data_row)

    # os.makedirs(os.path.dirname(temp_meta_data_file), exist_ok = True)
    #
    # with open(temp_meta_data_file + player_complete_name + ".csv", "w", encoding = "utf-8",
    #           newline = "") as archivo_csv:
    #     writer = csv.writer(archivo_csv)
    #     writer.writerow(players_meta_data_header)
    #     writer.writerow()
    #     # Save all the data for each player.


def clean_meta_data_variation():
    reference_df = pandas.DataFrame(columns = ["Player full name", "Current Value", "Points", "Average", "Matches",
                                               "Goals", "Cards", "Time Stamp"])
    for filename in os.listdir(temp1_folder):
        if filename.endswith(".csv"):
            dataframe = pandas.read_csv(os.path.join(temp1_folder, filename))
            reference_df = pandas.concat([reference_df, dataframe], ignore_index = True)

    reference_df.to_csv(players_meta_data_file, index = False)


def scrape_fantasy_players_value_table(driver, player_complete_name):

    script_element = driver.find_element(By.XPATH, "/html/body/script[14]")
    script_content = script_element.get_attribute("text")
    value_content = script_content.split("playerVideoOffset")[0].split(";")[1].strip()

    # Transform the "Valor" table into a JSON so that it can be later store into a CSV.
    json_str = value_content[value_content.index("(") + 1:-1]
    data = json.loads(json_str)
    points = data["points"]

    # os.makedirs(os.path.dirname(temp_market_info_file + player_complete_name + ".csv"), exist_ok = True)
    #
    # with open(temp_market_info_file + player_complete_name + ".csv", "w", encoding = "utf-8",
    #           newline = "") as archivo_csv:
    #     writer = csv.writer(archivo_csv)
    # Define the structure of the CSV.
    fechas = ["Nombre"]
    valores = [player_complete_name]

    meses = {"ene": "jan", "abr": "apr", "ago": "aug", "sept": "sep", "dic": "dec"}

    for point in points:
        parts = point["date"].split()
        parts[0] = parts[0].zfill(2)
        parts[1] = meses.get(parts[1].lower(), parts[1])
        corrected = " ".join(parts)
        fechas.append(datetime.strptime(corrected, "%d %b %Y").strftime("%d/%m/%Y"))
        valores.append(point["value"])

    write_to_csv(temp_market_info_file + player_complete_name + ".csv", fechas, valores)


def clean_market_variation():
    def find_min_max_dates(directory):
        low_date = None
        high_date = None

        for file in os.listdir(directory):
            if file.endswith(".csv"):
                df = pandas.read_csv(os.path.join(directory, file), parse_dates = [0])
                date_col = df.columns[1:]
                min_date = pandas.to_datetime(date_col, format = "%d/%m/%Y").min().strftime("%d/%m/%Y")
                max_date = pandas.to_datetime(date_col, format = "%d/%m/%Y").max().strftime("%d/%m/%Y")
                if low_date is None or min_date < low_date:
                    low_date = min_date
                if high_date is None or max_date > high_date:
                    high_date = max_date

        return low_date, high_date

    # Encontrar las fechas mínima y máxima
    minimum_date, maximum_date = find_min_max_dates(temp2_folder)

    # Crear un rango de fechas diarias entre la mínima y la máxima
    date_range = pandas.date_range(start = minimum_date, end = maximum_date, freq = "D")
    reference_df = pandas.DataFrame(columns = ["Nombre"] + date_range.strftime("%d/%m/%Y").to_list())

    # Iterar a través de los archivos CSV y llenar el DataFrame
    for filename in os.listdir(temp2_folder):
        if filename.endswith(".csv"):
            dataframe = pandas.read_csv(os.path.join(temp2_folder, filename))
            nombre_jugador = dataframe["Nombre"].values[0]
            dataframe = dataframe.drop(columns = ["Nombre"])
            player_values = pandas.concat([pandas.DataFrame({"Nombre": [nombre_jugador]}), dataframe.fillna(0)],
                                          axis = 1)

            # Unir el resultado con el DataFrame del jugador
            reference_df = pandas.concat([reference_df, player_values])

    # Ordenar las columnas de fechas
    date_columns = reference_df.columns[1:]
    date_columns = sorted(date_columns, key = lambda x: pandas.to_datetime(x, format = "%d/%m/%Y"))
    reference_df = reference_df[["Nombre"] + date_columns]

    # Rellenar datos faltantes con 0
    reference_df = reference_df.fillna(0)

    # Cambiar el tipo de dato de columnas numéricas a enteros
    reference_df[date_columns] = reference_df[date_columns].applymap(int)

    # Guardar el DataFrame en un nuevo archivo CSV
    reference_df.to_csv(players_market_info_file, index = False)


def scrape_fantasy_players_game_week(driver, player_complete_name):
    # Find the points box.
    players_game_weeks = driver.find_elements(By.CLASS_NAME, "btn-player-gw")

    # Go through each game week
    temp_list = []

    for player_game_week in players_game_weeks:
        try:
            # Define an array where all the information will be stored in order to save everything into the CSV later,
            # first element is the full name of the player.
            player_game_week_data = [player_complete_name]

            # Get the data of which game week has the statics happened.
            game_week = player_game_week.find_element(By.CLASS_NAME, "gw")

            # Append the game week to the data array.
            player_game_week_data.append(game_week.text)

            player_game_week.click()

            time.sleep(1.2)

            stats_sports_providers_div = driver.find_element(By.CLASS_NAME, "providers")
            stats_sports_providers = stats_sports_providers_div.find_elements(By.CLASS_NAME, "points")

            for stats in stats_sports_providers:
                stats_filtered = stats.text.replace(",", ".")
                player_game_week_data.append(stats_filtered)

            # ------- Get all the providers stats and save them in different variables --------

            # Click on player "View more stats" button.
            player_view_more_stats = wait_click(driver, (By.XPATH, '//*[@id="popup-content"]/div[4]/div/button'))
            player_view_more_stats.click()

            time.sleep(1.2)

            player_stats = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/div[2]/table")
            # player_stats_breakdown = player_stats.find_elements(By.CLASS_NAME, "td-qty")
            player_stats_breakdown = player_stats.find_elements(By.TAG_NAME, "tr")

            for player in player_stats_breakdown:
                player_filter = player.text.replace(",", ".")
                player_game_week_data.append(player_filter)

            # Add a timestamp to the data array.
            date_time = datetime.now()
            formatted_date_time = date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
            player_game_week_data.append(formatted_date_time)
            temp_list.append(player_game_week_data)

            close_player_game_week = wait_click(driver, (By.XPATH, '//*[@id="popup"]/button'))
            close_player_game_week.click()
            time.sleep(1.2)

        except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
            # Element not found, we just continue into the next game week.
            pass
    if len(temp_list) < 10:
        print(player_complete_name)
    write_to_csv(temp_game_week_file + player_complete_name + ".csv", players_game_week_header, temp_list)


def procesar_fila(fila):

    mapping = dict(zip(spanish_list, english_list))

    datos_procesados = [""] * (len(english_list))

    aplicar_mapeo, i = False, 0
    for valor in fila:
        if " ".join(str(valor).split(" ")[:-1]).lower() == "pases totales" and \
                not all(ext in str(valor) for ext in ["2023", ":"]):
            aplicar_mapeo = True
        elif all(ext in str(valor) for ext in ["2023", ":"]):
            datos_procesados[int(english_list.index("Timestamp"))] = str(valor)
        if " ".join(str(valor).split(" ")[:-1]).lower() == "valoración" or str(valor).lower() == "nan" or \
                all(ext in str(valor) for ext in ["2023", ":"]):
            yeet = True
        else:
            yeet = False

        if not yeet:
            if aplicar_mapeo:
                columna = " ".join(str(valor).split(" ")[:-1]).lower()
                column = mapping.get(columna.lower(), columna)
                if str(valor).split(" ")[-1] == "0.1":
                    pass
                if column in english_list:
                    datos_procesados[int(english_list.index(column))] = str(valor).split(" ")[-1]
                else:
                    print(columna)
                    print(column)
            else:
                datos_procesados[i] = str(valor)
                i += 1
    for i in datos_procesados:
        if i == "":
            datos_procesados[datos_procesados.index(i)] = "0"

    return datos_procesados


def clean_game_week_variation():

    reference_df = pandas.DataFrame(columns = english_list)

    for filename in os.listdir(temp3_folder):
        if filename.endswith(".csv"):
            df_origen = pandas.read_csv(os.path.join(temp3_folder, filename))
            for fila in df_origen.itertuples(index = False):
                datos_a_insertar = procesar_fila(fila)
                reference_df.loc[len(reference_df)] = datos_a_insertar

    reference_df.to_csv(players_game_week_stats_file, index = False)


def scrape_teams_information():
    """
    Function that gets all the teams competing in the fantasy league, along with their corresponding players.
    Also, the code gets basic information on every team (money, average, etc).
    """
    driver = login_fantasy_mundo_deportivo()

    # Select the markets section, wait ten seconds as it usually takes some time to load the page.
    driver.get("https://mister.mundodeportivo.com/standings")

    # Get the table with all the teams' information.
    # Find all the user elements
    table_elements = driver.find_elements(by = By.CSS_SELECTOR, value = "ul.user-list li a.btn.btn-sw-link.user")

    # Extract the href values from each userTeam element
    user_hrefs = [user.get_attribute("href") for user in table_elements]
    # Since each player can have different positon, this is so that we can find depending on which pos the player is at
    position_mapping = {"pos-1": "Portero", "pos-2": "Defensa", "pos-3": "Medio Campista", "pos-4": "Delantero"}

    user_hrefs = list(set(user_hrefs))

    teams_players_header = ["Team Name", "Position", "Name", "Surname"]
    team_data_header = ["Team Name", "Puntos", "Media", "Valor", "Jugadores"]
    teams_players_data = []
    team_data_data = []

    # Goes through all the userTeams and gets each teams players
    for user_element in user_hrefs:
        driver.get(user_element)
        h1_element = driver.find_element(by = By.TAG_NAME, value = "h1")
        team_name = h1_element.text
        # Navigate to the userTeam's individual page
        try:
            # Find the parent element that contains all the starting player links
            lineup_players = driver.find_element(By.CLASS_NAME, "lineup-starting")
            # Find all the player links the ones that are playing
            player_links = lineup_players.find_elements(By.TAG_NAME, "a")
        except NoSuchElementException:
            player_links = []
        try:
            lineup_subs = driver.find_element(By.CLASS_NAME, "lineup-subs")
            # Find all the player links the ones that are subs
            playersubs_links = lineup_subs.find_elements(By.TAG_NAME, "a")
        except NoSuchElementException:
            playersubs_links = []
        # put them all together and only get the links from the Hrefs
        player_links = player_links + playersubs_links
        player_hrefs = [player_link.get_attribute("href") for player_link in player_links]

        # In this for once with all players links we get the name, surname and position
        for player in player_hrefs:
            driver.get(player)
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract class = pos-" text
            position_class = soup.select_one(".team-position i")["class"][0]

            # Find the "left" div
            left_div = soup.find("div", class_ = "left")

            # Extract the name from within the "left" div
            name = left_div.find("div", class_ = "name").text
            surname = left_div.find("div", class_ = "surname").text

            # Map the position class to the corresponding position
            position = position_mapping.get(position_class, "Unknown")

            teams_players_data.append([team_name, position, name, surname])
        driver.get(user_element)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Select the parent div element with the class "wrapper" to narrow down the search
        parent_div = soup.find(name = "div", class_ = "wrapper items thin-scrollbar")

        # Find all div elements with class "item" within the parent div
        items = parent_div.find_all(name = "div", class_ = "item")

        # Initialize a dictionary to store label-value pairs
        label_value_dict = {}

        # Extract data from each item and set each label with each corresponding value
        for item in items:
            label = item.find("div", class_ = "label").text
            value = item.find("div", class_ = "value").text
            label_value_dict[label] = value

            points = label_value_dict.get("Puntos")
            average = label_value_dict.get("Media")
            team_value = label_value_dict.get("Valor")
            players_count = label_value_dict.get("Jugadores")
            # Replace commas with periods
            average = average.replace(",", ".")
            team_value = team_value.replace(",", ".")

            # Write the data to the CSV file
            team_data_data.append([team_name, points, average, team_value, players_count])

        write_to_csv(team_data_file, team_data_header, team_data_data)
        write_to_csv(teams_players_file, teams_players_header, teams_players_data)

        # Close the WebDriver when done
        driver.quit()


def scrape_la_liga_standings(api_key):
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": api_key}

    # Specify the type of API request to make, league = 140 stands for La Liga,
    # and season = 2023 stands for the current date of the league.
    conn.request("GET", "/standings?league=140&season=2023", headers = headers)

    # Get the API response.
    res = conn.getresponse()
    data = res.read()

    # Decode the data and load it as a JSON object
    json_data = json.loads(data.decode("utf-8"))

    """
    JSON file includes a bunch of information we will not use, so we just get the important information we need 
    that being made by only getting the response object inside the JSON file
    and inside the response object we get the league, and inside the league we get the standings object, 
    the standing object has the information we need in this case.
    """
    standings = json_data.get("response", [])[0].get("league", {}).get("standings", [])[0]

    # Create a CSV file to store La Liga standings.
    header = ["Rank", "Team Name", "Total Points", "Goals Difference", "Games Played", "Games Won", "Games Draw",
              "Games Lost", "All goals for", "All Goals Against", "Home games wins", "Home games draws",
              "Home games loses", "Home games goals for", "Home games Goals Against", "Away games Wins",
              "Away games Draws", "Away games Loses", "Away games goals for", "Away games goals Against", "Date"]

    # List to append all teams information.
    team_data_list = []

    # Loop through each teams
    for standing in standings:
        values = [standing["rank"], standing["team"]["name"], standing["points"], standing["goalsDiff"],
                  standing["all"]["played"], standing["all"]["win"], standing["all"]["draw"], standing["all"]["lose"],
                  standing["all"]["goals"]["for"], standing["all"]["goals"]["against"], standing["home"]["win"],
                  standing["home"]["draw"], standing["home"]["lose"], standing["home"]["goals"]["for"],
                  standing["home"]["goals"]["against"], standing["away"]["win"], standing["away"]["draw"],
                  standing["away"]["lose"], standing["away"]["goals"]["for"], standing["away"]["goals"]["against"],
                  datetime.now()]

        # Append values to the team_data_list
        team_data_list.append(values)

    os.makedirs(os.path.dirname(standings_file), exist_ok = True)
    # Writing data to CSV file
    with open(standings_file, "a" if os.path.exists(standings_file) else "w", encoding = "utf-8",
              newline = "") as csv_file:
        writer = csv.writer(csv_file)

        if not os.path.exists(standings_file):
            writer.writerow(header)
            # Write team data
        writer.writerows(team_data_list)


def scrape_backup(folder, backup):
    os.makedirs(os.path.dirname(folder), exist_ok = True)
    os.makedirs(os.path.dirname(backup), exist_ok = True)
    files = os.listdir(folder)

    for filename in files:
        original_path = os.path.join(folder, filename)
        backup_path = os.path.join(backup, filename + "_bak")

        if os.path.exists(original_path):
            if os.path.exists(backup_path):
                original_size = os.path.getsize(original_path)
                backup_size = os.path.getsize(backup_path)
                if original_size >= backup_size:
                    shutil.copy(original_path, backup_path)
                else:
                    shutil.copy(backup_path, original_path)
            else:
                shutil.copy(original_path, backup_path)


if __name__ == "__main__":

    with open("config.json", "r", encoding = "utf-8") as config_file:
        config = json.load(config_file)

    api_football = config["api-football"]

    # if sys.argv[1] == "market":
    #     scrape_market_section_fantasy()
    # elif sys.argv[1] == "personal":
    #     scrape_personal_team_fantasy()
    # elif sys.argv[1] == "api":
    #     scrape_la_liga_standings(api_football)
    # elif sys.argv[1] == "all":
    #     scrape_all_players_fantasy()
    # elif sys.argv[1] == "stats":
    #     pass
    #     # scrape_players_stats_fantasy()
    # elif sys.argv[1] == "teams":
    #     scrape_teams_information()
    # else:
    #     exit(0)

    scrape_market_section_fantasy()
    scrape_personal_team_fantasy()
    scrape_all_players_fantasy()
    scrape_players_stats_fantasy()
    scrape_teams_information()
    scrape_la_liga_standings(api_football)
    scrape_backup(league_folder, backup_folder)
    scrape_backup(players_folder, backup_folder)
    scrape_backup(api_folder, backup_folder)
