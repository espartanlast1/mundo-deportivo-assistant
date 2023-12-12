# !/usr/bin/env python3

# -*- coding: utf-8 -*-
# fantasy_teams.py

#

import helper

from bs4 import BeautifulSoup

# So it didn't show any warning of variable may be undefined.
logger = "Defined"

# For debugging, this sets up a formatting for a logfile, and where it is.
if helper.lorca != "Windows":
    try:
        if not helper.os.path.exists(helper.r_folder + "fantasy_teams.log"):
            helper.logging.basicConfig(filename = helper.r_folder + "fantasy_teams.log", level = helper.logging.ERROR,
                                       format = "%(asctime)s %(levelname)s %(name)s %(message)s")
            logger = helper.logging.getLogger(__name__)
        else:
            helper.logging.basicConfig(filename = helper.r_folder + "fantasy_teams.log", level = helper.logging.ERROR,
                                       format = "%(asctime)s %(levelname)s %(name)s %(message)s")
            logger = helper.logging.getLogger(__name__)
    except Exception as error:
        logger.exception(error)


def scrape_all_players_fantasy():
    """
    Function that gets all the fantasy players URLs and save them into a CSV file.
    """
    driver = helper.login_fantasy_mundo_deportivo()

    # Go directly to URL
    driver.get("https://mister.mundodeportivo.com/more#players")

    # Set a maximum number of attempts to click the button (optional)
    max_attempts = 12
    attempt = 1
    button_exists = True

    # Create a loop to continuously check for the button's existence
    while button_exists and attempt <= max_attempts:
        try:
            # Now, wait for the button to be clickable
            more_players_button = helper.wait_click(driver, (helper.By.CLASS_NAME, "search-players-more"), 4)
            # Click the button
            more_players_button.click()
            # Give some time for content to load (you can adjust this sleep duration as needed)
            helper.sleep(2.5)
            # Increment the attempt counter
            attempt += 1
        except (AttributeError, helper.NoSuchElementException, helper.ElementClickInterceptedException,
                helper.TimeoutException):
            # The button is not found, set the flag to False
            button_exists = False

    # After the loop, perform another action if the button no longer exists
    if not button_exists:
        # Wait for the players' table to be clickable
        players_table = helper.wait_click(driver, (helper.By.CLASS_NAME, "player-list"), 4)
        link_elements = players_table.find_elements(helper.By.CSS_SELECTOR, "a.btn-sw-link")
        hrefs = [link.get_attribute("href") for link in link_elements]
        data = [[url] for url in hrefs]

        helper.write_to_csv(helper.player_links_file, False, data, "w")
    driver.quit()


def scrape_personal_team_fantasy():
    driver = helper.login_fantasy_mundo_deportivo()

    driver.get("https://mister.mundodeportivo.com/team")

    team_players_table = driver.find_element(helper.By.CLASS_NAME, "player-list")

    # Select each player.
    team_players_info = team_players_table.find_elements(helper.By.CLASS_NAME, "info")
    whole_team_id = helper.extract_player_id(team_players_table)

    #
    players = helper.scrape_player_info(team_players_info, whole_team_id)

    # ------- Start process to save all the information in a CSV. --------
    team_players_header = ["ID", "Name", "Market value", "Average value", "Ante penultimate match score",
                           "Penultimate match score", "Last match score"]
    helper.write_to_csv(helper.personal_team_file, team_players_header, players, "w")
    driver.quit()


def process_urls(t_p_d, t_d_d, t_d_h, u_e, p_m, l_m):
    driver = helper.login_fantasy_mundo_deportivo()
    driver.get(u_e)
    h1_element = driver.find_element(by = helper.By.TAG_NAME, value = "h1")
    t_n = h1_element.text
    # Navigate to the userTeam's individual page
    try:
        # Find the parent element that contains all the starting player links
        lineup_players = driver.find_element(helper.By.CLASS_NAME, "lineup-starting")
        # Find all the player links the ones that are playing
        player_links = lineup_players.find_elements(helper.By.TAG_NAME, "a")
    except helper.NoSuchElementException:
        player_links = []
    try:
        lineup_subs = driver.find_element(helper.By.CLASS_NAME, "lineup-subs")
        # Find all the player links the ones that are subs
        playersubs_links = lineup_subs.find_elements(helper.By.TAG_NAME, "a")
    except helper.NoSuchElementException:
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
        position = p_m.get(position_class, "Unknown")
        t_p_d.append([t_n, position, name, surname])
    driver.get(u_e)
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
        translated_label = l_m.get(label, t_d_h)
        value = item.find("div", class_ = "value").text
        label_value_dict[translated_label] = value

    points = label_value_dict.get("Points")
    average = (label_value_dict.get("Average")).replace(",", ".")
    team_value = (label_value_dict.get("Value")).replace(",", ".")
    players_count = label_value_dict.get("Players")

    # Write the data to the CSV file
    t_d_d.append([t_n, points, average, team_value, players_count])
    driver.quit()


def scrape_teams_information():
    """
    Function that gets all the teams competing in the fantasy league, along with their corresponding players.
    Also, the code gets basic information on every team (money, average, etc.).
    """
    driver = helper.login_fantasy_mundo_deportivo()

    # Select the markets section, wait ten seconds as it usually takes some time to load the page.
    driver.get("https://mister.mundodeportivo.com/standings")

    # Get the table with all the teams' information.
    # Find all the user elements
    table_elements = driver.find_elements(by = helper.By.CSS_SELECTOR, value = "ul.user-list li a.btn.btn-sw-link.user")

    # Extract the href values from each userTeam element
    user_hrefs = [user.get_attribute("href") for user in table_elements]
    # Since each player can have different positon, this is so that we can find depending on which pos the player is at
    position_mapping = {"pos-1": "Goalkeeper", "pos-2": "Defence", "pos-3": "Midfielder", "pos-4": "Forward"}

    user_hrefs = list(set(user_hrefs))

    teams_players_header = ["Team Name", "Position", "Name", "Surname"]
    original_labels = ["Team Name", "Puntos", "Media", "Valor", "Jugadores"]
    team_data_header = ["Team Name", "Points", "Average", "Value", "Players"]
    label_mapping = dict(zip(original_labels, team_data_header))

    teams_players_data = [[] for _ in range(len(user_hrefs))]
    team_data_data = [[] for _ in range(len(user_hrefs))]

    # Goes through all the userTeams and gets each teams players
    threads = []
    for i in range(len(user_hrefs)):
        thread = helper.threading.Thread(target = process_urls, args = (teams_players_data[i], team_data_data[i],
                                                                        team_data_header, user_hrefs[i],
                                                                        position_mapping, label_mapping))
        threads.append(thread)
        helper.sleep(0.1)
        thread.start()

    for thread in threads:
        thread.join()

    all_t_data_data = [item for sublist in team_data_data for item in sublist]
    all_t_players_data = [item for sublist in teams_players_data for item in sublist]
    helper.write_to_csv(helper.team_data_file, team_data_header, sorted(all_t_data_data, key = lambda x: x[0][0]), "w")
    helper.write_to_csv(helper.teams_players_file, teams_players_header,
                        sorted(all_t_players_data, key = lambda x: x[0][0]), "w")
    # Close the WebDriver when done
    driver.quit()


if __name__ == "__main__":
    # it = helper.datetime.now()
    scrape_all_players_fantasy()
    scrape_personal_team_fantasy()
    scrape_teams_information()
    helper.delete_profile()
    for folder in helper.all_folders:
        helper.scrape_backup(folder, helper.backup_folder)
    helper.automated_commit("League.")
    # print(str(helper.datetime.now() - it))
