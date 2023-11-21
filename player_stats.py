import helper
import math
import requests
import threading

from time import sleep


# Gameweek headers.
players_meta_data_header = ["Player full name", "Current Value", "Points", "Average", "Matches", "Goals", "Cards",
                            "Time Stamp"]
spanish_map_list = ["player full name", "posición", "equipo", "contrincante", "game week", "mixto", "as score",
                    "marca score", "mundo deportivo score", "sofa score", "valor actual", "puntos", "media", "partidos",
                    "goles", "tarjetas", "pases totales", "pases precisos",
                    "balones en largo totales", "balones en largo precisos", "centros totales", "centros precisos",
                    "despejes totales", "despejes en la línea de gol", "duelos aéreos perdidos",
                    "duelos aéreos ganados", "duelos perdidos", "duelos ganados", "regateado", "pérdidas",
                    "regates totales", "regates completados", "despejes por alto", "despejes con los puños",
                    "errores que llevan a disparo", "errores que llevan a gol", "tiros fuera", "tiros a puerta",
                    "tiros bloqueados en ataque", "tiros bloqueados en defensa", "ocasiones creadas",
                    "asistencias de gol", "tiros al palo", "ocasiones claras falladas", "penaltis cometidos",
                    "penaltis provocados", "penaltis fallados", "penaltis parados", "goles",
                    "goles en propia puerta", "paradas desde dentro del área", "paradas", "goles evitados",
                    "intercepciones", "salidas totales", "salidas precisas", "entradas totales", "faltas recibidas",
                    "faltas cometidas", "fueras de juego", "minutos jugados", "toques",
                    "entradas como último hombre", "posesiones perdidas", "goles esperados", "pases clave",
                    "match_stat_expectedassists", "15/16", "16/17", "17/18", "18/19", "19/20", "20/21", "21/22",
                    "22/23", "23/24"]
spanish_checklist = ["pases totales", "pases precisos", "balones en largo totales", "balones en largo precisos",
                     "centros totales", "centros precisos", "despejes totales", "despejes en la línea de gol",
                     "duelos aéreos perdidos", "duelos aéreos ganados", "duelos perdidos", "duelos ganados",
                     "regateado", "pérdidas", "regates totales", "regates completados", "despejes por alto",
                     "despejes con los puños", "errores que llevan a disparo", "errores que llevan a gol",
                     "tiros fuera", "tiros a puerta", "tiros bloqueados en ataque", "tiros bloqueados en defensa",
                     "ocasiones creadas", "asistencias de gol", "tiros al palo", "ocasiones claras falladas",
                     "penaltis cometidos", "penaltis provocados", "penaltis fallados", "penaltis parados", "goles",
                     "goles en propia puerta", "paradas desde dentro del área", "paradas", "goles evitados",
                     "intercepciones", "salidas totales", "salidas precisas", "entradas totales", "faltas recibidas",
                     "faltas cometidas", "fueras de juego", "minutos jugados", "toques",
                     "entradas como último hombre", "posesiones perdidas",  "goles esperados", "pases clave",
                     "match_stat_expectedassists"]
english_list = ["Player full name", "Position", "Team", "Opposing Team", "Game Week", "Mixed", "AS Score",
                "Marca Score", "Mundo Deportivo Score", "Sofa Score", "Current Value", "Points", "Average", "Matches",
                "Goals", "Cards", "Total Passes", "Accurate Passes", "Total Long Balls", "Accurate Long Balls",
                "Total Crosses", "Accurate Crosses", "Total clearances", "Clearances on goal line", "Aerial Duels Lost",
                "Aerial Duels Won", "Duels Lost", "Duels Won", "Dribbled Past", "Losses", "Total Dribbles",
                "Completed dribbles", "High clearances", "Fist clearances", "Failures that lead to shot",
                "Failures that lead to goal", "Shots Off Target", "Shots on Target", "Shots blocked in attack",
                "Shots blocked in defence", "Occasions created", "Goal assists", "Shots to the crossbar",
                "Failed obvious occasions", "Penalties commited", "Penalties caused", "Failed penalties",
                "Stopped penalties", "Goals", "Own goals", "Stops from inside the area", "Stops", "Goals avoided",
                "Interceptions", "Total outputs", "Precise outputs", "Total Tackles", "Fouls Received",
                "Fouls Committed", "Offsides", "Minutes Played", "Touches", "Entries as last man",
                "Possessions Lost", "Expected Goals", "Key Passes", "Expected Assists", "Average Season 15/16",
                "Average Season 16/17", "Average Season 17/18", "Average Season 18/19", "Average Season 19/20",
                "Average Season 20/21", "Average Season 21/22", "Average Season 22/23", "Average Season 23/24",
                "Timestamp"]
url_lock = threading.Lock()
lock = threading.Lock()


def scrape_fantasy_players_meta_data(driver):
    # Get all the information to call the CSV according to the player name and surname.
    players_info = driver.find_element(helper.By.XPATH, '//*[@id="content"]/div[5]/div[1]/div/div[1]')
    position = players_info.find_element(
            helper.By.XPATH, '//*[@id="content"]/div[5]/div[1]/div/div[1]/div[1]/i'). \
        get_attribute("class").split(" ")[0]
    if position == "pos-1":
        position = "0"
    elif position == "pos-2":
        position = "1"
    elif position == "pos-3":
        position = "2"
    elif position == "pos-4":
        position = "3"
    players_name = players_info.find_element(helper.By.CLASS_NAME, "name").text
    players_surname = players_info.find_element(helper.By.CLASS_NAME, "surname").text
    player_complete_name = players_name + players_surname
    player_image = driver.find_element(helper.By.CSS_SELECTOR, ".player-pic img").get_attribute("src").split("?version")
    response = requests.get(player_image[0])
    img_file = "img/" + player_complete_name + ".png"
    helper.os.makedirs(helper.os.path.dirname(img_file), exist_ok = True)
    with open(img_file, "wb") as img:
        img.write(response.content)

    # Get all the player's metadata.
    player_wrapper = driver.find_elements(helper.By.CSS_SELECTOR, "div.player-stats-wrapper div.value")

    valor_actual = player_wrapper[0].text
    puntos = player_wrapper[1].text
    media = player_wrapper[2].text.replace(",", ".")
    partidos = player_wrapper[3].text
    goles = player_wrapper[4].text
    tarjetas = player_wrapper[5].text
    time_stamp = str(helper.datetime.now())

    return [player_complete_name, valor_actual, puntos, media, partidos, goles, tarjetas, time_stamp], position,\
        player_complete_name


def scrape_fantasy_players_value_table(driver, player_complete_name):
    def player_exists(tl, pcn):
        ex = False
        for p in tl[1:]:
            if p[0] == pcn:
                ex = True
                break
            else:
                if p[0] == tl[-1][0] and not ex:
                    ex = False
        return ex

    def extract_date(extract):
        meses = {"ene": "jan", "abr": "apr", "ago": "aug", "sept": "sep", "dic": "dec"}
        parts = extract["date"].split()
        parts[0] = parts[0].zfill(2)
        parts[1] = meses.get(parts[1].lower(), parts[1])
        return " ".join(parts)

    def add_data():
        values = ["0"] * len(dates)
        values[0] = player_complete_name
        for point in points:
            date_to_find = helper.datetime.strptime(extract_date(point), "%d %b %Y").strftime("%d/%m/%Y")
            for date in dates:
                if date == date_to_find:
                    values[dates.index(date)] = point["value"]
                    break
        return values

    script_element = driver.find_element(helper.By.XPATH, "/html/body/script[14]")
    script_content = script_element.get_attribute("text")
    value_content = script_content.split("playerVideoOffset")[0].split(";")[1].strip()

    # Transform the "Valor" table into a JSON so that it can be later store into a CSV.
    json_str = value_content[value_content.index("(") + 1:-1]
    data = helper.json.loads(json_str)
    points = data["points"]

    reset = False
    dates = ["Nombre"]
    vals = [player_complete_name]

    with lock:
        try:
            with open(helper.players_market_info_file, "r", encoding = "utf-8") as f:
                temp_file = helper.csv.reader(f)
                temp_list = list(temp_file)
            corrected = extract_date(points[-1])
            new_date = helper.datetime.strptime(corrected, "%d %b %Y").strftime("%d/%m/%Y")
            if temp_list[0][-1] != new_date:
                temp_list[0].append(new_date)
            dates = temp_list[0]
            if player_exists(temp_list, player_complete_name):
                for i in temp_list[1:]:
                    if i[0] == player_complete_name:
                        if temp_list[0][-1] != new_date and len(i) != len(temp_list[0]):
                            i.append(points[-1]["value"])
                        break
            else:
                temp_vals = add_data()
                temp_list.append(temp_vals)
            vals = [i for i in temp_list[1:] if i[0] == player_complete_name][0]
        except FileNotFoundError:
            reset = True

        if reset:
            corrected = extract_date(points[-1])
            date_today = helper.datetime.strptime(corrected, "%d %b %Y").strftime("%m/%d/%Y")
            date_year = (helper.datetime.strptime(corrected, "%d %b %Y") -
                         helper.timedelta(days = 365)).strftime("%m/%d/%Y")
            date_range = helper.pandas.date_range(start = date_year, end = date_today, freq = "D")
            dates = ["Nombre"] + date_range.strftime("%d/%m/%Y").to_list()
            vals = add_data()

    return dates, vals


def process_row(fila):

    mapping = dict(zip(spanish_map_list, english_list))

    datos_procesados = ["0"] * (len(english_list))

    aplicar_mapeo, i = False, 0
    for valor in fila:
        if " ".join(str(valor).split(" ")[:-1]).lower() in spanish_checklist and \
                not all(ext in str(valor) for ext in ["2023", ":"]):
            aplicar_mapeo = True
        elif all(ext in str(valor) for ext in ["2023", ":"]):
            datos_procesados[int(english_list.index("Timestamp"))] = str(valor)
        if " ".join(str(valor).split(" ")[:-1]).lower() == "valoración" or str(valor).lower() == "nan" or \
                all(ext in str(valor) for ext in ["2023", ":"]):
            yeet = True
        else:
            yeet = False

        if not yeet:
            if aplicar_mapeo:
                columna = " ".join(str(valor).split(" ")[:-1]).lower()
                column = mapping.get(columna.lower(), columna)
                if str(valor).split(" ")[-1] == "0.1":
                    pass
                if column in english_list:
                    datos_procesados[int(english_list.index(column))] = str(valor).split(" ")[-1]
                else:
                    print(columna)
                    print(column)
            else:
                datos_procesados[i] = str(valor)
                i += 1

    return datos_procesados


def scrape_fantasy_players_game_week(driver, player_complete_name, position, value, points, average, matches, goals,
                                     cards, player_url):
    first_box = driver.find_element(helper.By.CLASS_NAME, "boxes-2")
    second_box = first_box.find_elements(helper.By.CLASS_NAME, "box-records")[1]

    pattern = r"(\d{2}/\d{2}.*?)\n(\d,\d+)"
    matches = helper.re.findall(pattern, second_box.text)

    # Crea las sublistas deseadas
    processed_average = [[match[0], match[1]] for match in matches]
    temporal_averages = []
    for result in processed_average:
        temporal_averages.append(" ".join(result))

    # Find the points box.
    players_game_weeks = driver.find_elements(helper.By.CLASS_NAME, "btn-player-gw")

    # Go through each game week
    temp_list = []
    for player_game_week in players_game_weeks:
        # Define an array where all the information will be stored in order to save everything into the CSV
        # later, first element is the full name of the player.
        player_game_week_data = [player_complete_name, position]

        # Get the data of which game week has the statics happened.
        game_week = player_game_week.find_element(helper.By.CLASS_NAME, "gw")

        played = True
        player_gw = None
        try:
            player_gw = player_game_week.find_element(helper.By.CLASS_NAME, "score")
        except helper.NoSuchElementException:
            played = False
        sleep(0.4)
        if played:
            intercept = True
            while intercept:
                try:
                    gw_button = helper.wait_click(driver, player_gw, 6)
                    gw_button.click()
                    intercept = False
                except helper.TimeoutException:
                    print("Timeout: ", player_game_week_data)
                    helper.write_to_csv(helper.timeout_file, False, [player_url], "a")
                except helper.ElementClickInterceptedException:
                    print("Intercepted: ", player_game_week_data)
                    sleep(6)
                    intercept = True

            sleep(0.2)
            team_id = {1: "Athletic Club", 2: "Atlético", 3: "Barcelona", 4: "Betis", 5: "Celta", 9: "Getafe",
                       10: "Granada", 11: "Las Palmas", 14: "Rayo Vallecano", 15: "Real Madrid", 16: "Real Sociedad",
                       17: "Sevilla", 19: "Valencia", 20: "Villareal", 21: "Almería", 48: "Alavés", 50: "Osasuna",
                       222: "Girona", 408: "Mallorca", 499: "Cádiz"}
            sub_player = driver.find_element(helper.By.CLASS_NAME, "sub-player")
            get_team = sub_player.find_element(helper.By.CLASS_NAME, "team-logo").\
                get_attribute("src").split(".png")[0].split("/")[-1]
            player_match = driver.find_element(helper.By.CLASS_NAME, "player-match")
            left = player_match.find_element(helper.By.CLASS_NAME, "left")
            right = player_match.find_element(helper.By.CLASS_NAME, "right")
            left_team = left.find_element(helper.By.CLASS_NAME, "team-logo").\
                get_attribute("src").split(".png")[0].split("/")[-1]
            right_team = right.find_element(helper.By.CLASS_NAME, "team-logo").\
                get_attribute("src").split(".png")[0].split("/")[-1]
            if get_team == left_team:
                opposing_team = team_id.get(int(right_team))
            else:
                opposing_team = team_id.get(int(left_team))
            own_team = team_id.get(int(get_team))
            player_game_week_data.append(own_team)
            player_game_week_data.append(opposing_team)
            # Append the game week to the data array.
            if "j" in game_week.text.lower():
                player_game_week_data.append(game_week.text[1:])
            elif "gw" in game_week.text.lower():
                player_game_week_data.append(game_week.text[2:])
            stats_sports_providers_div = driver.find_element(helper.By.CLASS_NAME, "providers")
            stats_sports_providers = stats_sports_providers_div.find_elements(helper.By.CLASS_NAME, "points")

            suma = 0
            for stats in stats_sports_providers:
                stats_filtered = stats.text.replace(",", ".")
                suma += int(stats_filtered)
            player_game_week_data.append(suma // 4)
            for stats in stats_sports_providers:
                stats_filtered = stats.text.replace(",", ".")
                player_game_week_data.append(stats_filtered)

            player_game_week_data.extend([value, points, average, matches, goals, cards])

            # Click on player "View more stats" button.
            player_view_more_stats = helper.wait_click(
                driver, (helper.By.XPATH, '//*[@id="popup-content"]/div[4]/div/button'), 5)
            player_view_more_stats.click()

            sleep(0.15)

            player_stats = driver.find_element(helper.By.XPATH, "/html/body/div[4]/div[1]/div/div[2]/table")
            player_stats_breakdown = player_stats.find_elements(helper.By.TAG_NAME, "tr")

            for player in player_stats_breakdown:
                player_filter = player.text.replace(",", ".")
                player_game_week_data.append(player_filter)

            for i in temporal_averages:
                player_game_week_data.append(i)

            # Add a timestamp to the data array.
            formatted_date_time = helper.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            player_game_week_data.append(formatted_date_time)
            processed_data = process_row(player_game_week_data)
            temp_list.append(processed_data)

            sleep(0.15)
            close_player_game_week = helper.wait_click(driver, (helper.By.XPATH, '//*[@id="popup"]/button'), 4)
            close_player_game_week.click()

    return temp_list


def process_urls(am, av, aw, header, ucf):
    driver = helper.login_fantasy_mundo_deportivo()
    try:
        helper.skip_button(driver, (helper.By.CLASS_NAME, "btn-tutorial-skip"))
    except (helper.NoSuchElementException, helper.ElementClickInterceptedException, helper.TimeoutException):
        # Element not found, we just continue.
        pass
    for url in ucf:
        driver.get(url[0])
        # ------ Store players metadata ------
        meta_data, position, player_complete_name = scrape_fantasy_players_meta_data(driver)
        am.append(meta_data)
        # print(player_complete_name)
        # ------ Store players value table ------
        head, values = scrape_fantasy_players_value_table(driver, player_complete_name)
        av.append(values)
        header.append(head)
        # ------ Store players game week ------
        gw = scrape_fantasy_players_game_week(driver, player_complete_name, position, meta_data[0], meta_data[1],
                                              meta_data[2], meta_data[3], meta_data[4], meta_data[5], url)
        if gw:
            aw.append(gw)
    driver.quit()


def scrape_players_stats_fantasy():

    url_csv_file = helper.read_player_url()
    if helper.os.path.exists(helper.timeout_file):
        helper.os.remove(helper.timeout_file)
    segments = [url_csv_file[i:(i + (math.ceil(len(url_csv_file) / 3)))] for i in range
                (0, len(url_csv_file), (math.ceil(len(url_csv_file) / 3)))]

    url_part1 = segments[0]
    url_part2 = segments[1]
    url_part3 = segments[2]

    all_meta, all_value, all_week, header = [], [], [], []
    all_meta1, all_value1, all_week1, header1 = [], [], [], []
    all_meta2, all_value2, all_week2, header2 = [], [], [], []
    all_meta3, all_value3, all_week3, header3 = [], [], [], []

    thread1 = threading.Thread(target = process_urls, args = (all_meta1, all_value1, all_week1, header1, url_part1))
    thread2 = threading.Thread(target = process_urls, args = (all_meta2, all_value2, all_week2, header2, url_part2))
    thread3 = threading.Thread(target = process_urls, args = (all_meta3, all_value3, all_week3, header3, url_part3))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    # Displaying the contents of the CSV file
    all_meta_lists = [all_meta1, all_meta2, all_meta3]
    all_value_lists = [all_value1, all_value2, all_value3]
    all_week_lists = [all_week1, all_week2, all_week3]

    for meta_list, value_list, week_list in zip(all_meta_lists, all_value_lists, all_week_lists):
        all_meta.extend(meta_list)
        all_value.extend(value_list)
        all_week.extend(week_list)
    if helper.os.path.exists(helper.timeout_file):
        process_urls(helper.read_timeout_url(), all_meta, all_value, all_week, header3)
    o_all_meta = sorted(all_meta, key = lambda x: x[0])
    o_all_value = sorted(all_value, key = lambda x: x[0])
    o_all_week = sorted(all_week, key = lambda x: (x[0][0], x[0][1:]))
    helper.write_to_csv(helper.players_meta_data_file, players_meta_data_header, o_all_meta, "w")
    helper.write_to_csv(helper.players_market_info_file, header1[0], o_all_value, "w")
    helper.write_to_csv(helper.players_game_week_stats_file, english_list, False, "w")
    for p in o_all_week:
        p.reverse()
        for week in p:
            helper.write_to_csv(helper.players_game_week_stats_file, False, [week], "a")


if __name__ == "__main__":
    it = helper.datetime.now()
    scrape_players_stats_fantasy()
    for file in helper.all_folders:
        helper.scrape_backup(file, helper.backup_folder)
    helper.delete_profile()
    print(str(helper.datetime.now() - it))
