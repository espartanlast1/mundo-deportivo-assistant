import csv
import json
import http.client
import os
from datetime import datetime


# Open a local store json file to get the API Credentials for the API-Football API key.
with open('config.json') as config_file:
    config = json.load(config_file)

api_football = config['api-football']

# Code given by the API-Football documentation to connect to their API.
conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': api_football
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
csv_file_path = "standings-la-liga.csv"
file_exists = os.path.exists(csv_file_path)

# Writing data to CSV file
with open(csv_file_path, 'a' if file_exists else 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    if not file_exists:
        writer.writerow(header)
        # Write team data
    writer.writerows(team_data_list)