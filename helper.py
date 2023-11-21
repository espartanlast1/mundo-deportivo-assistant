import csv
import json
import os
import pandas
import re
import shutil

from datetime import datetime, timedelta
from pathlib import Path
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


# Folder list.
aux_folder = "data/auxiliary/"
league_folder = "data/league/"
players_folder = "data/players/"
football_folder = "data/football/"
sofascore_folder = "data/sofascore/"
backup_folder = "data/backup/"
all_folders = [aux_folder, league_folder, players_folder, football_folder, sofascore_folder]

# File list.
player_links_file = "data/auxiliary/fantasy-players-links.csv"
timeout_file = "data/auxiliary/timeout.csv"
market_file = "data/players/fantasy-players-in-market.csv"
personal_team_file = "data/league/fantasy-personal-team-data.csv"
team_data_file = "data/league/fantasy-teams-data.csv"
teams_players_file = "data/league/fantasy-teams-players.csv"
players_meta_data_file = "data/players/fantasy-metadata-players.csv"
players_market_info_file = "data/players/fantasy-market-variation.csv"
players_game_week_stats_file = "data/players/fantasy-games-week-players-stats.csv"
standings_file = "data/football/standings-la-liga.csv"
sofascore_data = "data/sofascore/data"
players_s_data = "players-data-sofascore.csv"


def delete_profile():
    temp_f = Path("..", "..", "AppData", "Local", "Temp")
    for i in os.listdir(temp_f):
        if any(ext in i for ext in ["chrome_", "rust_moz", "scoped_"]) and (temp_f / i).is_dir():
            profile_path = temp_f / i
            for item in profile_path.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            profile_path.rmdir()


def wait_click(driv, selector, t):
    wait = WebDriverWait(driv, t)
    elemento = wait.until(ec.element_to_be_clickable(selector))
    return elemento


def skip_button(d, f):
    s_b = wait_click(d, f, 4)
    s_b.click()


def write_to_csv(file_path, header, data, typ):
    os.makedirs(os.path.dirname(file_path), exist_ok = True)

    # Create a CSV with all the previous information mentioned.
    with open(file_path, typ, encoding = "utf-8", newline = "") as csv_file:
        writer = csv.writer(csv_file)
        # Write the header
        if header:
            writer.writerow(header)
        # Append the data
        if data:
            writer.writerows(data)


def read_csv(filname):
    with open(filname, "r", encoding = "utf-8", newline = "") as csv_file:
        csv_reader = csv.reader(csv_file)
        data = []
        for row in csv_reader:
            data.append(row)
    return data


def read_player_url():
    with open(player_links_file, "r", encoding = "utf-8") as file:
        reader = csv.reader(file)
        return list(reader)


def read_timeout_url():
    with open(timeout_file, "r", encoding = "utf-8") as file:
        reader = csv.reader(file)
        return list(reader)


def scrape_player_info(t_p_i):
    # Create an array to save players info.
    players = []

    for player_info in t_p_i:
        # Split the text to create a list of player information.
        raw_player_information = player_info.text.split("\n")

        # Clean the data.
        cleaned_player_information = [item.replace("↑", "").replace("↓", "").replace(",", ".").
                                      replace("-", "0.0").strip() for item in raw_player_information]
        players.append(cleaned_player_information)
    return players


def login_fantasy_mundo_deportivo():
    with open("config.json", "r", encoding = "utf-8") as cf:
        c = json.load(cf)

    email_fantasy = c["email"]
    password_fantasy = c["password"]

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # driver = webdriver.Chrome(options = chrome_options)

    firefox_options = webdriver.FirefoxOptions()
    # firefox_options.add_argument("--headless")
    # firefox_service = webdriver.FirefoxService(executable_path = "/usr/local/bin/geckodriver")
    driver = webdriver.Firefox(options = firefox_options)  # , service = firefox_service)

    mundo_deportivo_liga_fantasy = "https://mister.mundodeportivo.com/new-onboarding/auth/email"
    driver.get(mundo_deportivo_liga_fantasy)

    try:
        # Wait for the cookies to appear and click the button to accept them.
        button_cookies = wait_click(driver, (By.ID, "didomi-notice-agree-button"), 2)
        button_cookies.click()
    except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
        # Element not found, we just continue.
        pass

    # Enter the email and password.
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(email_fantasy)

    password_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[2]/input')
    password_input.send_keys(password_fantasy)

    # Click on the login button.
    submit_button = wait_click(driver, (By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[3]/button'), 2)
    submit_button.click()

    # Special wait to skip the first tutorial, when we start with a new account it will appear, so better to check it.
    try:
        skip_button(driver, (By.CLASS_NAME, "btn-tutorial-skip"))
    except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
        # Element not found, we just continue.
        pass

    return driver


def scrape_backup(folder, backup):
    os.makedirs(folder, exist_ok = True)
    os.makedirs(backup, exist_ok = True)
    files = os.listdir(folder)

    for filename in files:
        original_path = os.path.join(folder, filename)
        back_path = os.path.join(backup, filename + "_bak")
        if os.path.exists(back_path):
            try:
                original_size = os.path.getsize(original_path)
                backup_size = os.path.getsize(back_path) if os.path.exists(back_path) else 0
            except FileNotFoundError:
                backup_size, original_size = -1, -1
                print(f"El archivo original '{original_path}' no existe.")
            try:
                if 0 < original_size > backup_size:
                    shutil.copy(original_path, back_path)
                else:
                    shutil.copy(back_path, original_path)
            except shutil.Error as e:
                print(f"Error al copiar archivos: {e}")
        else:
            shutil.copy(original_path, back_path)
