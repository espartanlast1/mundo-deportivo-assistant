import json
import http.client

with open('config.json') as config_file:
    config = json.load(config_file)

api_football = config['api-football']

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': api_football
    }

conn.request("GET", "/standings?league=140&season=2023", headers=headers)

res = conn.getresponse()
data = res.read()

# Decode the data and load it as a JSON object
json_data = json.loads(data.decode("utf-8"))

# Pretty print the JSON data
print(json.dumps(json_data, indent=2))