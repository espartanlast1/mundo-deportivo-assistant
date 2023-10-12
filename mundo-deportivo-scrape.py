from datetime import datetime
from selenium import webdriver
from selenium.common import NoSuchElementException
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
    file_name = 'data/market-data.csv'

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
    file_name = 'data/team-data.csv'

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

    # Select the markets section, wait ten seconds as it usually takes some time to load the page.
    table_section = wait2.until(
        ec.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="content"]/header/div[2]/ul/li[4]/a'
            )
        )
    )
    table_section.click()

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

