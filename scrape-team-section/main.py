from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import csv
import json
import os


with open('config.json') as config_file:
    config = json.load(config_file)

email = config['email']
password = config['password']

driver = webdriver.Edge()
chrome_options = webdriver.EdgeOptions()
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
market_structure_header = ['Puntuacion', 'Nombre', 'Valor mercado', 'Promedio valor', 'Ultimo partido puntuacion', 'Penultimo partido puntuacion', 'Antepenultimo partido puntuacion', 'Venta','Time Stamp']

# Get the name of the CSV file together.
file_name = 'market-data.csv'

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
        player_data = player + [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        print(player_data)
        writer.writerow(player_data)

driver.quit()