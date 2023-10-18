import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import csv
import json
import os

with open('config.json') as config_file:
    config = json.load(config_file)

email = config['email']
password = config['password']

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

# Get the table with all the teams information.
# Find all the user elements
table_elements = driver.find_elements(by=By.CSS_SELECTOR,value="ul.user-list li a.btn.btn-sw-link.user")

# Extract the href values from each user element
user_hrefs = [user.get_attribute("href") for user in table_elements]
# Create a dictionary to map position classes to their positions
position_mapping = {
    "pos-1": "Portero",
    "pos-2": "Defensa",
    "pos-3": "Medio Campista",
    "pos-4": "Delantero"
}
user_hrefs = list(set(user_hrefs))
# Create a CSV file for storing the data
csv_filename = "fantasy-teams-players.csv"
file_exists1 = os.path.exists(csv_filename)
with open(csv_filename, 'a' if file_exists1 else 'w', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    # Write the header row to the CSV file
    if not file_exists1:
        csv_writer.writerow(["Team Name", "Position", "Name", "Surname"])

    # Iterate through the user elements
    for user_element in user_hrefs:
        driver.get(user_element)

        h1_element = driver.find_element(by=By.TAG_NAME, value='h1')
        TeamName= h1_element.text
        # Navigate to the user's individual page
        # Find the parent element that contains all the starting player links
        lineup_players = driver.find_element(By.CLASS_NAME, "lineup-starting")
        lineup_subs = driver.find_element(By.CLASS_NAME, "lineup-subs")

        # Find all the player links within the parent element
        player_links = lineup_players.find_elements(By.TAG_NAME, 'a')
        playersubs_links = lineup_subs.find_elements(By.TAG_NAME, 'a')

        player_links = player_links + playersubs_links
        player_hrefs = [player_link.get_attribute("href") for player_link in player_links]
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

            csv_writer.writerow([TeamName,position, name, surname])
        driver.get(user_element)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Select the parent div element with the class "wrapper" to narrow down the search
        parent_div = soup.find(name="div", class_="wrapper items thin-scrollbar")

        # Find all div elements with class "item" within the parent div
        items = parent_div.find_all(name="div", class_="item")

        # Initialize a dictionary to store label-value pairs
        label_value_dict = {}

        # Extract data from each item
        for item in items:
            label = item.find('div', class_='label').text
            value = item.find('div', class_='value').text
            # Store the label-value pair in the dictionary
            label_value_dict[label] = value
        # Create a CSV file for storing the team data
        team_csv_filename = "fantasy-teams-data.csv"
        file_exists = os.path.exists(team_csv_filename)
        with open(team_csv_filename, 'a' if file_exists else 'w', newline='') as team_csv_file:
            # Iterate through each player href
            team_csv_writer = csv.writer(team_csv_file)

            # Write the header
            if not file_exists:
                team_csv_writer .writerow(["Team Name", "Puntos", "Media", "Valor", "Jugadores"])

            # Now, you can access the data using the label as the key
            points = label_value_dict.get("Puntos")
            average = label_value_dict.get("Media")
            team_value = label_value_dict.get("Valor")
            players_count = label_value_dict.get("Jugadores")

            # Write the data to the CSV file
            team_csv_writer.writerow([TeamName, points, average, team_value, players_count])

    # Close the WebDriver when done
    driver.quit()

