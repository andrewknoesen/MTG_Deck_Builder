import json
import sys
import time
import pandas as pd
from pprint import pprint
import requests


def get_id(exact_card: str):
    # https://mox.rouxtaccess.com/api/card/search?name=Evolved%20Sleeper&uniqueName=1

    search_parameters = {  # Parameters for api. Key must match documents
        "name": exact_card,
        "uniqueName": True,
    }

    mox_response = requests.get(
        url="https://mox.rouxtaccess.com/api/card/search", params=search_parameters)
    
    while "<!DOCTYPE html>" in mox_response.text:
        print("server error")
        time.sleep(5)
        mox_response = requests.get(
        url="https://mox.rouxtaccess.com/api/card/search", params=search_parameters)
    

    data = mox_response.json()

    print("###################################")
    print(f"Returned retailer Raw for card {exact_card}:")
    print("###################################")
    pprint(data)
    print("###################################")
    print("###################################")

    # print(data['data'])
    return int(data['data'][0]['id'])


def get_retailers(id: int, name: str):
    endpoint: str = f"https://mox.rouxtaccess.com/api/card/{id}/scrape/queued?include=retailer"
    retailers: requests.Response = requests.post(endpoint)
    
    while "<!DOCTYPE html>" in retailers.text :
        print("server error")
        time.sleep(5)
        retailers = requests.post(endpoint)

    compiled_reatilers: list = retailers.json()['data']

    for i in range(2, retailers.json()['meta']['pagination']['total_pages'] + 1):
        retailers_page = requests.post(
            f'https://mox.rouxtaccess.com/api/card/{id}/scrape/queued?include=retailer&page={i}')

        while "<!DOCTYPE html>" in retailers_page.text :
            print("server error")
            time.sleep(5)
            retailers_page = requests.post(
            f'https://mox.rouxtaccess.com/api/card/{id}/scrape/queued?include=retailer&page={i}')

        for item in retailers_page.json()['data']:
            compiled_reatilers.append(item)

    print("###################################")
    print("Returned retailer Raw:")
    print(f"Endpoint: {endpoint}")
    print("###################################")
    pprint(compiled_reatilers)
    print("###################################")
    print("###################################")
    retail = {}
    private = {}
    for item in compiled_reatilers:
        print(item)
        response_card_name: str = item['name'].split(' - ')[0].split(' [')[0].split(' (')[0]
        if name == response_card_name:
            if '?' not in item['priceRead']:
                retail[item['id']] = {
                    'name': name,
                    'name_long': item['name'],
                    'cost': float(item['priceRead'][1:].replace(",", "")),
                    'qty': item['stock'],
                    'supplier': item['retailer']['name'],
                    'link': item['link']
                }
            else:
                private[item['id']] = {
                    'name': name,
                    'name_long': item['name'],
                    'cost': item['priceRead'],
                    'qty': item['stock'],
                    'supplier': item['retailer']['name'],
                    'link': item['link']
                }

    print("###################################")
    print("Returned retailer:")
    print("###################################")
    pprint(retail)

    return {
        'retail': retail,
        'private': private
    }


def clean_up(cards: list) -> list:
    pass


def scrape_mox(cards_df: pd.DataFrame) -> list:

    print("###################################")
    print(f'Scraping')
    print(cards_df)
    print("###################################")
    compiled_retailers = []

    dict_len = len(cards_df.index)
    print("###################################")
    print(f'Cards loaded: {dict_len}')
    print(cards_df)
    print("###################################")
    count = 0
    for card in cards_df['name']:

        id = get_id(card)

        compiled_retailers.append(get_retailers(id, card)['retail'])
        # compiled_private.append(get_retailers(id, card)['retail'])
        count += 1
        print("###################################")
        print(f'Completed: {count}/{dict_len}')
        print("###################################")

    return compiled_retailers

