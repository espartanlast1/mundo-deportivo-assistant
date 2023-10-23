import time
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import csv
import json
import os
import http.client
import re
from bs4 import BeautifulSoup


def login_fantasy_mundo_deportivo():

    with open('config.json') as config_file:
        config = json.load(config_file)

    email_fantasy = config['email']
    password_fantasy = config['password']

    driver = webdriver.Chrome()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    mundo_deportivo_liga_fantasy = "https://mister.mundodeportivo.com/new-onboarding/auth/email"
    driver.get(mundo_deportivo_liga_fantasy)

    wait1 = WebDriverWait(driver, 3)
    wait2 = WebDriverWait(driver, 3)
    wait3 = WebDriverWait(driver, 3)

    # Wait for the cookies to appear and click the button to accept them.
    button_cookies = wait1.until(
        ec.element_to_be_clickable(
            (
                By.ID,
                'didomi-notice-agree-button'
            )
        )
    )

    button_cookies.click()

    # Enter the email and password.
    email_input = driver.find_element(By.ID, 'email')
    email_input.send_keys(email_fantasy)

    password_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[2]/input')
    password_input.send_keys(password_fantasy)

    # Click on the login button.
    submit_button = wait2.until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="app"]/div/div[2]/div/form/div[3]/button'
            )
        )
    )
    submit_button.click()

    # Special wait to skip the first tutorial, when we start with a new account it will appear, so better to check it.
    try:

        skip_button = wait3.until(
            ec.element_to_be_clickable(
                (
                    By.CLASS_NAME,
                    'btn-tutorial-skip'
                )
            )
        )
        skip_button.click()

    except Exception:
        # Element not found, we just continue.
        pass

    return driver


def scrape_market_section_fantasy():
    driver = login_fantasy_mundo_deportivo()

    # Select the markets section, wait ten seconds as it usually takes some time to load the page.
    driver.get("https://mister.mundodeportivo.com/market")

    # Get the players data table.
    market_players_table = driver.find_element(By.ID, 'list-on-sale')

    # Select each player.
    market_players_info = market_players_table.find_elements(By.CLASS_NAME,'player-row')

    # Create an array to save players info.
    players = []

    for market_player_info in market_players_info:
        # Split the text to create a list of player information.
        raw_player_information = market_player_info.text.split('\n')

        # Clean the data.
        cleaned_player_information = [item.replace("↑", "").replace("↓", "").replace(",", ".") for item in
                                      raw_player_information]

        players.append(cleaned_player_information)

    # ------ Start process to save all the information in a CSV. ------

    # Create first row of the CSV file.
    market_structure_header = ['Points', 'Full name', 'Market value', 'Average value',
                               'Ante penultimate match score', 'Penultimate match score',
                               'Last match score', 'Attempt to buy', 'Time Stamp']

    # Get the name of the CSV file together.
    file_name = 'data/league/fantasy-players-in-market.csv'

    # Check if the file exists
    file_exists = os.path.exists(file_name)

    with open(file_name, 'a' if file_exists else 'w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)

        # Write the header
        if not file_exists:
            writer.writerow(market_structure_header)

        # Append the players
        writer.writerows(players)

    driver.quit()


def scrape_personal_team_fantasy():
    driver = login_fantasy_mundo_deportivo()

    driver.get("https://mister.mundodeportivo.com/team")

    team_players_table = driver.find_element(By.CLASS_NAME, 'player-list')

    # Select each player.
    team_players_info = team_players_table.find_elements(By.CLASS_NAME,'info')

    # Create an array to save players info.
    players = []

    for team_player_info in team_players_info:
        # Split the text to create a list of player information.
        raw_player_information = team_player_info.text.split('\n')

        # Clean the data.
        cleaned_player_information = [item.replace("↑", "").replace("↓", "").replace(",", ".") for item in
                                      raw_player_information]

        players.append(cleaned_player_information)

    # ------- Start process to save all the information in a CSV. --------

    # Create first row of the CSV file.
    team_players_header = ['Name', 'Market value', 'Average value',
                           'Ante penultimate match score', 'Penultimate match score',
                           'Last match score']

    # Get the name of the CSV file together.
    file_name = 'data/league/fantasy-personal-team-data.csv'

    # Check if the file exists
    file_exists = os.path.exists(file_name)

    # Create a CSV with all the previous information mentioned.
    with open(file_name, 'a' if file_exists else 'w', newline='') as archivo_csv:

        writer = csv.writer(archivo_csv)

        # Write the header
        if not file_exists:
            writer.writerow(team_players_header)

        writer.writerows(players)

    driver.quit()


def scrape_all_players_fantasy(email, password):
    driver = webdriver.Chrome()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    mundo_deportivo_liga_fantasy = "https://mister.mundodeportivo.com/new-onboarding/auth/email"

    driver.get(mundo_deportivo_liga_fantasy)
    wait1 = WebDriverWait(driver, 5)
    wait2 = WebDriverWait(driver, 5)
    wait3 = WebDriverWait(driver, 5)
    wait4 = WebDriverWait(driver, 5)

    # Wait for the cookies to appear and click the button to accept them.
    button_cookies = wait1.until(
        ec.element_to_be_clickable(
            (
                By.ID,
                'didomi-notice-agree-button'
            )
        )
    )

    button_cookies.click()

    # Enter the email and password.
    email_input = driver.find_element(By.ID, 'email')
    email_input.send_keys(email)

    password_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[2]/input')
    password_input.send_keys(password)

    # Click on the login button.
    submit_button = wait2.until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="app"]/div/div[2]/div/form/div[3]/button'
            )
        )
    )
    submit_button.click()

    # Special wait to skip the first tutorial, when we start with a new account it will appear, so better to check it.
    try:

        skip_button = wait3.until(
            ec.element_to_be_clickable(
                (
                    By.CLASS_NAME,
                    'btn-tutorial-skip'
                )
            )
        )
        skip_button.click()

    except Exception:
        # Element not found, we just continue.
        pass

    # Select the more section, wait five seconds as it usually takes some time to load the page.
    more_section = wait4.until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="content"]/header/div[2]/ul/li[5]/a'
            )
        )
    )
    more_section.click()

    players_section = wait4.until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="content"]/div[2]/div[1]/button[2]'
            )
        )
    )
    players_section.click()

    # ------------- Process to check if the more button exists, if it does, continue to click it until it disappears.
    button_locator = (By.CLASS_NAME, 'search-players-more')

    # Set a maximum number of attempts to click the button (optional)
    max_attempts = 15
    attempt = 1
    button_exists = True

    # Create a loop to continuously check for the button's existence
    while button_exists and attempt <= max_attempts:
        try:
            # Now, wait for the button to be clickable
            more_players_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(button_locator)
            )

            # Click the button
            more_players_button.click()

            # Give some time for content to load (you can adjust this sleep duration as needed)
            time.sleep(5)

            # Increment the attempt counter
            attempt += 1
        except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
            # The button is not found, set the flag to False
            button_exists = False

    # After the loop, perform another action if the button no longer exists
    if not button_exists:
        # Wait for the players table to be clickable
        players_table = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'player-list'))
        )
        print(players_table.text)

        link_elements = players_table.find_elements(By.CSS_SELECTOR, 'a.btn-sw-link')

        hrefs = [link.get_attribute('href') for link in link_elements]

        with open('data/fantasy-players-links.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for href in hrefs:
                writer.writerow([href])


def scrape_players_stats_fantasy(email, password):
    driver = webdriver.Chrome()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    mundo_deportivo_liga_fantasy = "https://mister.mundodeportivo.com/new-onboarding/auth/email"

    driver.get(mundo_deportivo_liga_fantasy)
    wait1 = WebDriverWait(driver, 5)
    wait2 = WebDriverWait(driver, 5)
    wait3 = WebDriverWait(driver, 5)
    wait4 = WebDriverWait(driver, 5)

    # Wait for the cookies to appear and click the button to accept them.
    button_cookies = wait1.until(
        ec.element_to_be_clickable(
            (
                By.ID,
                'didomi-notice-agree-button'
            )
        )
    )

    button_cookies.click()

    # Enter the email and password.
    email_input = driver.find_element(By.ID, 'email')
    email_input.send_keys(email)

    password_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[2]/input')
    password_input.send_keys(password)

    # Click on the login button.
    submit_button = wait2.until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="app"]/div/div[2]/div/form/div[3]/button'
            )
        )
    )
    submit_button.click()

    # Special wait to skip the first tutorial, when we start with a new account it will appear, so better to check it.
    try:

        skip_button = wait3.until(
            ec.element_to_be_clickable(
                (
                    By.CLASS_NAME,
                    'btn-tutorial-skip'
                )
            )
        )
        skip_button.click()

    except Exception:
        # Element not found, we just continue.
        pass

    filename = 'data/fantasy-players-links.csv'

    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        url_csv_file = list(reader)

        # displaying the contents of the CSV file
    for row in url_csv_file:
        for url in row:
            driver.get(url)

            """ ------ Store players metadata ------ """

            scrape_fantasy_players_meta_data(driver)

            # Get all the information to call the CSV according to the player name and surname.
            players_info = driver.find_element(By.XPATH, '//*[@id="content"]/div[5]/div[1]/div/div[1]')
            players_name = players_info.find_element(By.CLASS_NAME, 'name').text
            players_surname = players_info.find_element(By.CLASS_NAME, 'surname').text
            player_complete_name = players_name + players_surname

            # ------ Store players value table ------ 
            scrape_fantasy_players_value_table(driver, player_complete_name)

            # ------ Store players game week ------
            scrape_fantasy_players_game_week(driver, player_complete_name)



def scrape_fantasy_players_meta_data(driver):
    # Get all the information to call the CSV according to the player name and surname.
    players_info = driver.find_element(By.XPATH, '//*[@id="content"]/div[5]/div[1]/div/div[1]')
    players_name = players_info.find_element(By.CLASS_NAME, 'name').text
    players_surname = players_info.find_element(By.CLASS_NAME, 'surname').text
    player_complete_name = players_name + players_surname

    # Get all the player's metadata.
    players_meta_data = "data/players/fantasy-metadata-players.csv"
    players_meta_data_header = ['Player full name', 'Current Value', 'Points', 'Average', 'Matches', 'Goals',
                                'Cards', 'Time Stamp']

    player_wrapper = driver.find_elements(By.CSS_SELECTOR, 'div.player-stats-wrapper div.value')

    valor_actual = player_wrapper[0].text
    puntos = player_wrapper[1].text
    media = player_wrapper[2].text.replace(",", ".")
    partidos = player_wrapper[3].text
    goles = player_wrapper[4].text
    tarjetas = player_wrapper[5].text
    time_stamp = datetime.now()

    file_exists_players_metadata = os.path.exists(players_meta_data)

    with open(players_meta_data, 'a' if file_exists_players_metadata else 'w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)

        # Write the CSV header.
        if not file_exists_players_metadata:
            writer.writerow(players_meta_data_header)

        writer.writerow(
            [player_complete_name, valor_actual, puntos, media, partidos, goles, tarjetas, time_stamp])
        # Save all the data for each player.


def scrape_fantasy_players_value_table(driver, player_complete_name):
    # Define the structure of the CSV.
    player_structure_header = ['Full Name', 'Value', 'Date']

    # Get the player "Valor" table.
    players_market_info = "data/players/fantasy-market-variation.csv"

    file_exists_players_value = os.path.exists(players_market_info)

    script_element = driver.find_element(By.XPATH, '/html/body/script[14]')
    script_content = script_element.get_attribute("text")
    value_content = script_content.split("playerVideoOffset")[0].split(";")[1].strip()

    # Transform the "Valor" table into a JSON so that it can be later store into a CSV.
    json_str = value_content[value_content.index('(') + 1:-1]
    data = json.loads(json_str)
    points = data['points']

    with open(players_market_info, 'a' if file_exists_players_value else 'w', newline='') as archivo_csv:

        writer = csv.writer(archivo_csv)

        # Write the CSV header.
        if not file_exists_players_value:
            writer.writerow(player_structure_header)

        for point in points:
            # Assuming 'Valor' and 'Fecha' are the columns you want to save the data into

            row = [''] * len(player_structure_header)
            row[player_structure_header.index('Full Name')] = player_complete_name
            row[player_structure_header.index('Value')] = point['value']
            row[player_structure_header.index('Date')] = point['date']
            writer.writerow(row)

def scrape_fantasy_players_game_week(driver, player_complete_name):
    wait3 = WebDriverWait(driver, 5)
    wait4 = WebDriverWait(driver, 5)

    # Find the points box.
    players_game_weeks = driver.find_elements(By.CLASS_NAME, "btn-player-gw")

    # Go through each game week
    for player_game_week in players_game_weeks:
        try:
            # Define an array where all the information will be store in order to save everything into the CSV later.
            player_game_week_data = []

            # Append the full name of the player to the data array.
            player_game_week_data.append(player_complete_name)

            # Get the data of which game week has the statics happened.
            game_week = player_game_week.find_element(By.CLASS_NAME, 'gw')

            #  Append the game week to the data array.
            player_game_week_data.append(game_week.text)

            player_game_week.click()

            time.sleep(2)

            stats_sports_providers_div = driver.find_element(By.CLASS_NAME, 'providers')
            stats_sports_providers = stats_sports_providers_div.find_elements(By.CLASS_NAME, 'sum')

            for stats in stats_sports_providers:
                stats_filtered = stats.text.replace(",", ".")

                player_game_week_data.append(stats_filtered)

            # ------- Get all the providers stats and save them in different variables --------

            # Click on player "View more stats" button.
            player_view_more_stats = wait3.until(
                ec.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="popup-content"]/div[4]/div/button'
                    )
                )
            )
            player_view_more_stats.click()

            time.sleep(2)

            player_stats = driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div/div[2]/table')
            # player_stats_breakdown = player_stats.find_elements(By.CLASS_NAME, 'td-qty')
            player_stats_breakdown = player_stats.find_elements(By.TAG_NAME, 'tr')

            for player in player_stats_breakdown:
                player_filter = player.text.replace(",", ".")
                player_game_week_data.append(player_filter)

            # Add a timestamp to the data array.
            player_game_week_data.append(datetime.now())

            # Save all the information into the CSV file
            players_game_week_stats = "data/players/fantasy-games-week-players-stats.csv"

            players_game_week_stats_header_1 = [
                'Player full name',
                'Game Week',
                'AS Score',
                'Marca Score',
                'Mundo Deportivo Score',
                'Sofa Score',
                'Total passes',
                'Accurate passes',
                'Total long balls',
                'Accurate long balls',
                'Total crosses',
                'Aerial duels lost',
                'Duels lost',
                'Duels won',
                'Dribbled past',
                'Losses',
                'Total dribbles',
                'Shots on target',
                'Goals',
                'Interceptions',
                'Total tackles',
                'Fouls received',
                'Fouls committed',
                'Offsides',
                'Minutes played',
                'Touches',
                'Rating',
                'Lost possessions',
                'Expected goals',
                'MATCH_STAT_expectedAssists',
                'Time Stamp'
            ]

            players_game_week_stats_header = [
                'Player full name',
                'Game Week',
                'AS Score',
                'Marca Score',
                'Mundo Deportivo Score',
                'Sofa Score',
                'Stat 1',
                'Stat 2',
                'Stat 3',
                'Stat 4',
                'Stat 5',
                'Stat 6',
                'Stat 7',
                'Stat 8',
                'Stat 9',
                'Stat 10',
                'Stat 11',
                'Stat 12',
                'Stat 13',
                'Stat 14',
                'Stat 15',
                'Stat 16',
                'Stat 17',
                'Stat 18',
                'Stat 19',
                'Stat 20',
                'Stat 21',
                'Stat 22',
                'Stat 23',
                'Stat 24',
                'Stat 25',
                'Stat 26',
                'Stat 27',
                'Stat 28'
            ]

            file_exists_players_game_week_stats = os.path.exists(players_game_week_stats)

            with open(players_game_week_stats, 'a' if file_exists_players_game_week_stats else 'w',
                      newline='') as archivo_csv:

                writer = csv.writer(archivo_csv)

                # Write the CSV header.
                if not file_exists_players_game_week_stats:
                    writer.writerow(players_game_week_stats_header)

                writer.writerow(player_game_week_data)

            close_player_game_week = wait4.until(
                ec.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="popup"]/button'
                    )
                )
            )
            close_player_game_week.click()

        except Exception:
            # Element not found, we just continue into the next game week.
            continue


"""
Function that gets all the teams competing in the fantasy league, along with their corresponding players. 
Also, the code gets basic information on every team (money, average, etc).
"""
def scrape_teams_information():
    driver = login_fantasy_mundo_deportivo()

    # Select the markets section, wait ten seconds as it usually takes some time to load the page.
    driver.get("https://mister.mundodeportivo.com/standings")

    # Get the table with all the teams information.
    # Find all the user elements
    table_elements = driver.find_elements(by=By.CSS_SELECTOR, value="ul.user-list li a.btn.btn-sw-link.user")

    # Extract the href values from each userTeam element
    user_hrefs = [user.get_attribute("href") for user in table_elements]
    # Since each player can have different positon, this is so that we can find depending on which pos the player is at
    position_mapping = {
        "pos-1": "Portero",
        "pos-2": "Defensa",
        "pos-3": "Medio Campista",
        "pos-4": "Delantero"
    }
    user_hrefs = list(set(user_hrefs))
    # Create or get the name CSV file for storing the data
    csv_filename = "data/league/fantasy-teams-players.csv"
    file_exists1 = os.path.exists(csv_filename)
    with open(csv_filename, 'a' if file_exists1 else 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the CSV header if the file exists.
        if not file_exists1:
            csv_writer.writerow(["Team Name", "Position", "Name", "Surname"])

        # goes through all the userTeams and gets each teams players
        for user_element in user_hrefs:
            driver.get(user_element)

            h1_element = driver.find_element(by=By.TAG_NAME, value='h1')
            TeamName = h1_element.text
            # Navigate to the userTeam's individual page
            try:
                # Find the parent element that contains all the starting player links
                lineup_players = driver.find_element(By.CLASS_NAME, "lineup-starting")
                # Find all the player links the ones that are playing
                player_links = lineup_players.find_elements(By.TAG_NAME, 'a')
            except NoSuchElementException:
                player_links = []
            try:
                lineup_subs = driver.find_element(By.CLASS_NAME, "lineup-subs")
                # Find all the player links the ones that are subs
                playersubs_links = lineup_subs.find_elements(By.TAG_NAME, 'a')
            except NoSuchElementException:
                playersubs_links = []
            #put them all together and only get the links from the Hrefs
            player_links = player_links + playersubs_links
            player_hrefs = [player_link.get_attribute("href") for player_link in player_links]

            #In this for once with all players links we get the name, surname and position
            for player in player_hrefs:
                driver.get(player)
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Extract class="pos-" text
                position_class = soup.select_one('.team-position i')['class'][0]

                # Find the 'left' div
                left_div = soup.find('div', class_='left')

                # Extract the name from within the 'left' div
                name = left_div.find('div', class_='name').text
                surname = left_div.find('div', class_='surname').text

                # Map the position class to the corresponding position
                position = position_mapping.get(position_class, "Unknown")

                csv_writer.writerow([TeamName, position, name, surname])
            driver.get(user_element)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Select the parent div element with the class "wrapper" to narrow down the search
            parent_div = soup.find(name="div", class_="wrapper items thin-scrollbar")

            # Find all div elements with class "item" within the parent div
            items = parent_div.find_all(name="div", class_="item")

            # Initialize a dictionary to store label-value pairs
            label_value_dict = {}

            # Extract data from each item and set each label with each corresponding value 
            for item in items:
                label = item.find('div', class_='label').text
                value = item.find('div', class_='value').text
                label_value_dict[label] = value
            # Create or get the name of CSV file for storing the team data
            team_csv_filename = "data/league/fantasy-teams-data.csv"
            file_exists = os.path.exists(team_csv_filename)
            with open(team_csv_filename, 'a' if file_exists else 'w', newline='') as team_csv_file:
                team_csv_writer = csv.writer(team_csv_file)
                # Write the header
                if not file_exists:
                    team_csv_writer.writerow(["Team Name", "Puntos", "Media", "Valor", "Jugadores"])

                points = label_value_dict.get("Puntos")
                average = label_value_dict.get("Media")
                team_value = label_value_dict.get("Valor")
                players_count = label_value_dict.get("Jugadores")
                # Replace commas with periods
                average = average.replace(",", ".")
                team_value = team_value.replace(",", ".")

                # Write the data to the CSV file
                team_csv_writer.writerow([TeamName, points, average, team_value, players_count])

        # Close the WebDriver when done
        driver.quit()

def scrape_la_liga_standings(api_key):
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': api_key
    }

    # Specify the type of API request to make, league = 140 stands for La Liga,
    # and season = 2023 stands for the current date of the league.
    conn.request("GET", "/standings?league=140&season=2023", headers=headers)

    # Get the API response.
    res = conn.getresponse()
    data = res.read()

    # Decode the data and load it as a JSON object
    json_data = json.loads(data.decode("utf-8"))

    """""
    JSON file includes a bunch of information we will not use, so we just get the important information we need 
    that being made by  only getting the response object inside the JSON file
    and inside the response object we get the league, and inside the league we get the standings object, 
    the standing object has the information we need in this case.
    """""
    standings = json_data.get('response', [])[0].get('league', {}).get('standings', [])[0]

    # Create a CSV file to store La Liga standings.
    header = [
        "Rank",
        "Team Name",
        "Total Points",
        "Goals Difference",
        "Games Played",
        "Games Won",
        "Games Draw",
        "Games Lost",
        "All goals for",
        "All Goals Against",
        "Home games wins",
        "Home games draws",
        "Home games loses",
        "Home games goals for",
        "Home games Goals Against",
        "Away games Wins",
        "Away games Draws",
        "Away games Loses",
        "Away games goals for",
        "Away games goals Against",
        "Date"
    ]

    # List to append all teams information.
    team_data_list = []

    # Loop through each teams
    for standing in standings:
        values = [
            standing["rank"],
            standing["team"]["name"],
            standing["points"],
            standing["goalsDiff"],
            standing["all"]["played"],
            standing["all"]["win"],
            standing["all"]["draw"],
            standing["all"]["lose"],
            standing["all"]["goals"]["for"],
            standing["all"]["goals"]["against"],
            standing["home"]["win"],
            standing["home"]["draw"],
            standing["home"]["lose"],
            standing["home"]["goals"]["for"],
            standing["home"]["goals"]["against"],
            standing["away"]["win"],
            standing["away"]["draw"],
            standing["away"]["lose"],
            standing["away"]["goals"]["for"],
            standing["away"]["goals"]["against"],
            datetime.now()
        ]

        # Append values to the team_data_list
        team_data_list.append(values)

    # Specify the CSV file path
    csv_file_path = "data/standings-la-liga.csv"
    file_exists = os.path.exists(csv_file_path)

    # Writing data to CSV file
    with open(csv_file_path, 'a' if file_exists else 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        if not file_exists:
            writer.writerow(header)
            # Write team data
        writer.writerows(team_data_list)


if __name__ == '__main__':

    with open('config.json') as config_file:
        config = json.load(config_file)

    api_football = config['api-football']

    choice = input("Enter a number (1-6) to call the corresponding function: ")

    if choice == "1":
        scrape_market_section_fantasy()
    elif choice == "2":
        scrape_personal_team_fantasy()
    elif choice == "3":
        scrape_la_liga_standings(api_football)
    elif choice == "4":
        pass
        #scrape_all_players_fantasy(email_fantasy, password_fantasy)
    elif choice == "5":
        pass
        #scrape_players_stats_fantasy(email_fantasy, password_fantasy)
    elif choice == "6":
        scrape_teams_information()
    else:
        print("Invalid choice!")