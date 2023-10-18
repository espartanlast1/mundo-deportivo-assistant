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

def scrape_market_section_fantasy ( email , password ):
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
    submit_button = wait1.until(
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

    # Select the markets section, wait ten seconds as it usually takes some time to load the page.
    markets_section = wait2.until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="content"]/header/div[2]/ul/li[2]/a'
            )
        )
    )
    markets_section.click()

    # Get the table with all the player markets information.
    market_players_table = wait4.until(
        ec.element_to_be_clickable(
            (
                By.ID,
                'list-on-sale'
            )
        )
    )

    # Create an array to save players info.
    players = []

    # Separate every item in a new array everytime there's a break line.
    players_market_information_array = market_players_table.text.split('\n')

    """
    As all the information is in a single array, we need to classify correctly depending on each player. 
    Each players information consists of 9 columns, so we will individually trim 9 columns of the market array 
    each time and create a new array each player with all his information.
    """
    for i in range(0, len(players_market_information_array), 9):
        # list slicing to get 9 elements, then the other 9 and so on.
        player_information = players_market_information_array[i:i + 9]
        players.append(player_information)

    # ------ Start process to save all the information in a CSV. ------

    # Create the name of the csv
    current_datetime = datetime.now()

    # Format the name of the CSV with date and time.
    market_time = current_datetime.strftime('%Y-%m-%d %H:%M')
    market_time = market_time.replace(" ", "-")

    # Create first row of the CSV file.
    market_structure_header = ['Puntuacion', 'Nombre', 'Valor mercado', 'Promedio valor',
                               'Antepenultimo partido puntuacion', 'Penultimo partido puntuacion',
                               'Ultimo partido puntuacion', 'Venta', 'Time Stamp']

    # Get the name of the CSV file together.
    file_name = 'data/fantasy-market-data.csv'

    # Check if the file exists
    file_exists = os.path.exists(file_name)

    # Create a CSV with all the previous information mentioned.
    with open(file_name, 'a' if file_exists else 'w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)

        # Write the header
        if not file_exists:
            writer.writerow(market_structure_header)

        for player in players:
            # Add the current timestamp to each player's data
            player_data = player + [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            writer.writerow(player_data)

    driver.quit()

def scrape_personal_team_fantasy ( email, password):
    driver = webdriver.Chrome()
    chrome_options = webdriver.Chrome()

    mundo_deportivo_liga_fantasy = "https://mister.mundodeportivo.com/new-onboarding/auth/email"

    driver.get(mundo_deportivo_liga_fantasy)
    wait1 = WebDriverWait(driver, 10000)
    wait2 = WebDriverWait(driver, 10000)

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
    submit_button = wait1.until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="app"]/div/div[2]/div/form/div[3]/button'
            )
        )
    )
    submit_button.click()

    # Special wait to skip the first tutorial.
    """"
    skip_button = wait1.until(
        ec.element_to_be_clickable(
            (
                By.CLASS_NAME,
                'btn-tutorial-skip'
            )
        )
    )
    skip_button.click()
    """

    # Select the markets section, wait ten seconds as it usually takes some time to load the page.
    team_selection = wait2.until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="content"]/header/div[2]/ul/li[3]/a'
            )
        )
    )
    team_selection.click()

    # Get the table with all the player markets information.
    team_table = wait2.until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="content"]/div[2]/div[4]/ul'
            )
        )
    )
    market_players_table = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[4]/ul')

    # Separate every item in a new array everytime there's a break line.
    players_market_information_array = market_players_table.text.split('\n')

    """
    As all the information is in a single array, we need to classify correctly depending on each player. 
    Each players information consists of 9 columns, so we will individually trim 9 columns of the market array 
    each time and create a new array each player with all his information.
    """
    # create the list to fill with the players information and the start index to loop through the array.
    players = []
    start_index = 0

    # Loop until there's no "Vender" left
    while 'Vender' in players_market_information_array[start_index:]:
        # Get the index of the next "Vender" and add 1 to get the end index.
        end_index = players_market_information_array.index('Vender', start_index) + 1
        # Get the player information from the start index to the end index.
        player_information = players_market_information_array[start_index:end_index]

        players.append(player_information)
        start_index = end_index

    # Start process to save all the information in a CSV.

    # Create the name of the csv
    current_datetime = datetime.now()

    # Format the name of the CSV with date and time.
    market_time = current_datetime.strftime('%Y-%m-%d %H:%M')
    market_time = market_time.replace(" ", "-")

    # Create first row of the CSV file.
    market_structure_header = ['Puntuacion', 'Nombre', 'Valor mercado', 'Promedio valor',
                               'Antepenultimo partido puntuacion', 'Penultimo partido puntuacion',
                               'Ultimo partido puntuacion', 'Time Stamp']

    # Get the name of the CSV file together.
    file_name = 'data/fantasy-team-data.csv'

    # Check if the file exists
    file_exists = os.path.exists(file_name)

    # Create a CSV with all the previous information mentioned.
    with open(file_name, 'a' if file_exists else 'w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)

        print(market_structure_header)
        # Write the header
        if not file_exists:
            writer.writerow(market_structure_header)

        for player in players:
            # Add the current timestamp to each player's data
            player.pop()
            player_data = player + [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            print(player_data)
            writer.writerow(player_data)

    driver.quit()

def scrape_all_players_fantasy( email ,password ):
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
        except (NoSuchElementException, ElementClickInterceptedException,TimeoutException):
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

def scrape_players_stats_fantasy(email , password):
    driver = webdriver.Chrome()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    mundo_deportivo_liga_fantasy = "https://mister.mundodeportivo.com/new-onboarding/auth/email"

    driver.get(mundo_deportivo_liga_fantasy)
    wait1 = WebDriverWait(driver, 5)
    wait2 = WebDriverWait(driver, 5)
    wait3 = WebDriverWait(driver, 5)


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
    url_csv_file = []

    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        url_csv_file = list(reader)

        # displaying the contents of the CSV file
    for row in url_csv_file:
        for url in row:

            driver.get(url)

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
            media = player_wrapper[2].text
            partidos = player_wrapper[3].text
            goles = player_wrapper[4].text
            tarjetas = player_wrapper[5].text
            time_stamp = datetime.now()

            file_exists = os.path.exists(players_meta_data)

            with open(players_meta_data, 'a' if file_exists else 'w', newline='') as archivo_csv:

                writer = csv.writer(archivo_csv)

                # Write the CSV header.
                if not file_exists:
                    writer.writerow(players_meta_data_header)

                writer.writerow(
                    [player_complete_name, valor_actual, puntos, media, partidos, goles, tarjetas, time_stamp])
                # Save all the data for each player.
                """"
                
                for point in points:
                    # Assuming 'Valor' and 'Fecha' are the columns you want to save the data into

                    row = [''] * len(player_structure_header)
                    row[player_structure_header.index('Name')] = player_complete_name
                    row[player_structure_header.index('Historic Value')] = point['value']
                    row[player_structure_header.index('Date')] = point['date']
                    writer.writerow(row)

            players_file_name_market = "data/players/" + players_name + "-" + players_surname + ".csv"

            # Define the structure of the CSV.
            player_structure_header = ['Valor Actual', 'Puntos', 'Media', 'Partidos',
                                       'Goles', 'Tarjetas', 'Fecha', 'Valor Historico',
                                       'Jornada 1', 'Time Stamp', ]

            players_market_info = "data/players/market-variation.csv"


            # Get the player basic information.

            # Get the player "Valor" table.
            players_market_info = "data/players/market-variation.csv"

            players_market_info_header = ['Name', 'Date', 'Historic Value']

            script_element = driver.find_element(By.XPATH, '/html/body/script[14]')
            script_content = script_element.get_attribute("text")
            value_content = script_content.split("playerVideoOffset")[0].split(";")[1].strip()

            # Transform the "Valor" table into a JSON so that it can be later store into a CSV.
            json_str = value_content[value_content.index('(') + 1:-1]
            data = json.loads(json_str)
            points = data['points']

            with open(players_market_info, 'w', newline='') as archivo_csv:

                writer = csv.writer(players_market_info_header)

                # Write the CSV header.
                writer.writerow(player_structure_header)

                #writer.writerow([valor_actual, puntos, media, partidos, goles, tarjetas])
                # Save all the data for each player.

                for point in points:
                    # Assuming 'Valor' and 'Fecha' are the columns you want to save the data into

                    row = [''] * len(player_structure_header)
                    row[player_structure_header.index('Name')] = player_complete_name
                    row[player_structure_header.index('Historic Value')] = point['value']
                    row[player_structure_header.index('Date')] = point['date']
                    writer.writerow(row)
                    """""

def scrape_la_liga_standings (api_key):
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

    email_fantasy = config['email']
    password_fantasy = config['password']
    api_football = config['api-football']

    scrape_market_section_fantasy(email_fantasy, password_fantasy)
    scrape_personal_team_fantasy(email_fantasy, password_fantasy)
    scrape_la_liga_standings(api_football)
    scrape_all_players_fantasy(email_fantasy,password_fantasy)
    scrape_players_stats_fantasy(email_fantasy,password_fantasy)


