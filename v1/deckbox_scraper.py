import requests


def get_deckbox_inventory(username: str):
    params={
        "page": 1,
        "sort_by": "name",
        "order": "asc",
    }
    
    exact_response = requests.get(url=f'https://deckbox-api.herokuapp.com/api/users/{username}/inventory', params = params)

    data = exact_response.json()

    return data

print(get_deckbox_inventory('David101'))