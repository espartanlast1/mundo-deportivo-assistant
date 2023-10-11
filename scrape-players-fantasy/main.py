from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
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
mas_section = wait2.until(
    ec.element_to_be_clickable(
        (
            By.XPATH,
            '//*[@id="content"]/header/div[2]/ul/li[5]/a'
        )
    )
)
mas_section.click()

players_section = wait2.until(
    ec.element_to_be_clickable(
        (
            By.XPATH,
            '//*[@id="content"]/div[2]/div[1]/button[2]'
        )
    )
)
players_section.click()

sleep(10000)




