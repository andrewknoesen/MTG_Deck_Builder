from urllib import response
import requests
import json

# search_parameters = {                          #Parameters for api. Key must match documents
#     "q": "Vigor",
#     "unique": "cards",
#     "order": "name",
# }

# search_response = requests.get(url="https://api.scryfall.com/cards/search", params=search_parameters)
# search_response.raise_for_status()
# data = search_response.json()

# for item in data["data"]:
#     print(item['name'])

# with open("scryfall_output.json", "w") as outfile:
#     json.dump(data["data"][0]["name"], outfile)

def exact(query: str):
    exact_parameters={
        "exact": query,
    }
    
    exact_response = requests.get(url='https://api.scryfall.com/cards/named', params = exact_parameters)

    data = exact_response.json()

    return data

def autocomplete(query: str):
    search_parameters = {                          #Parameters for api. Key must match documents
        "q": query,
        "format": "json",
        "pretty": False,
        "include_extras": False,
    }

    auto_complete_response = requests.get(url="https://api.scryfall.com/cards/autocomplete", params=search_parameters)

    data = auto_complete_response.json()

    return data['data']


