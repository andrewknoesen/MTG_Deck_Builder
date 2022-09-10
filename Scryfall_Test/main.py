import requests
import json

parameters = {                          #Parameters for api. Key must match documents
    "q": "Lightning",
    "unique": "cards",
    "order": "name",
}

response = requests.get(url="https://api.scryfall.com/cards/search", params=parameters)
response.raise_for_status()

data = response.json()

for item in data["data"]:
    print(item['name'])

with open("scryfall_output.json", "w") as outfile:
    json.dump(data["data"][0]["name"], outfile)
