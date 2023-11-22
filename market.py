import helper


# So it didn't show any warning of variable may be undefined.
logger = "Defined"

# For debugging, this sets up a formatting for a logfile, and where it is.
try:
    if not helper.os.path.exists("market.log"):
        helper.logging.basicConfig(filename = "market.log", level = helper.logging.ERROR,
                                   format = "%(asctime)s %(levelname)s %(name)s %(message)s")
        logger = helper.logging.getLogger(__name__)
    else:
        helper.logging.basicConfig(filename = "market.log", level = helper.logging.ERROR,
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

    # Select each player.
    market_players_info = market_players_table.find_elements(helper.By.CLASS_NAME, "player-row")

    #
    players = helper.scrape_player_info(market_players_info)

    # ------ Start process to save all the information in a CSV. ------
    market_structure_header = ["Points", "Full name", "Market value", "Average value", "Ante penultimate match score",
                               "Penultimate match score", "Last match score", "Attempt to buy"]
    helper.write_to_csv(helper.market_file, market_structure_header, players, "w")
    driver.quit()


if __name__ == "__main__":
    # it = helper.datetime.now()
    scrape_market_section_fantasy()
    for i in helper.all_folders:
        helper.scrape_backup(i, helper.backup_folder)
    helper.delete_profile()
    helper.automated_commit()
    # print(str(helper.datetime.now() - it))
