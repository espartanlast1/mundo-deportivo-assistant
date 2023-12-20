# !/usr/bin/env python3

# -*- coding: utf-8 -*-
# market.py

#

import helper


# So it didn't show any warning of variable may be undefined.
logger = "Defined"

# For debugging, this sets up a formatting for a logfile, and where it is.
if helper.lorca != "Windows":
    try:
        if not helper.os.path.exists(helper.r_folder + "market.log"):
            helper.logging.basicConfig(filename = helper.r_folder + "market.log", level = helper.logging.ERROR,
                                       format = "%(asctime)s %(levelname)s %(name)s %(message)s")
            logger = helper.logging.getLogger(__name__)
        else:
            helper.logging.basicConfig(filename = helper.r_folder + "market.log", level = helper.logging.ERROR,
                                       format = "%(asctime)s %(levelname)s %(name)s %(message)s")
            logger = helper.logging.getLogger(__name__)
    except Exception as error:
        logger.exception(error)


def scrape_market_section_fantasy():
    driver = helper.login_fantasy_mundo_deportivo()

    # Select the markets section, wait ten seconds as it usually takes some time to load the page.
    driver.get("https://mister.mundodeportivo.com/market")

    # Get the players' data table.
    market_players_table = driver.find_element(helper.By.ID, "list-on-sale")
    whole_team_id = helper.extract_player_id(market_players_table)

    # Select each player.
    market_players_info = market_players_table.find_elements(helper.By.CLASS_NAME, "player-row")

    #
    players = helper.scrape_player_info(market_players_info, whole_team_id)

    # ------ Start process to save all the information in a CSV. ------
    market_structure_header = ["ID", "Points", "Full name", "Market value", "Average value",
                               "Ante penultimate match score", "Penultimate match score", "Last match score",
                               "Attempt to buy"]
    helper.write_to_csv(helper.market_file, market_structure_header, players, "w")
    driver.quit()


def scrape_personal_lineup_fantasy():
    driver = helper.login_fantasy_mundo_deportivo()

    driver.get("https://mister.mundodeportivo.com/team")

    team_players_lineup = driver.find_element(helper.By.CLASS_NAME, "team__lineup")

    aux_formation = team_players_lineup.text.split("\nMedia total")[-1].split("\n")
    r_formation = [i for i in aux_formation if "-" in i][0].replace("-", "")
    formation = r_formation[2] + r_formation[1] + r_formation[0]
    whole_lineup = team_players_lineup.find_elements(helper.By.TAG_NAME, "button")
    whole_lineup_id = [i.get_attribute("data-id_player") for i in whole_lineup if
                       i.get_attribute("data-id_player") is not None if i.get_attribute("data-id_player").isdigit()]
    list_images = helper.os.listdir(helper.image_folder)
    whole_lineup_name = []
    for i in whole_lineup_id:
        for _ in list_images:
            if i == _.split("_")[0]:
                whole_lineup_name.append(_.split(".png")[0].split("_")[-1])

    current = [[formation]] + [[i] for i in whole_lineup_name]

    helper.write_to_csv(helper.personal_lineup_file, False, current, "w")
    driver.quit()


if __name__ == "__main__":
    # it = helper.datetime.now()
    scrape_market_section_fantasy()
    scrape_personal_lineup_fantasy()
    helper.delete_profile()
    for folder in helper.all_folders:
        helper.scrape_backup(folder, helper.backup_folder)
    helper.automated_commit("Market.")
    # print(str(helper.datetime.now() - it))
