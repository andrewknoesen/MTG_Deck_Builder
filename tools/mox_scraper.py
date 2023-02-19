import pandas as pd
import requests

def get_id(exact_card: str):
    # https://mox.rouxtaccess.com/api/card/search?name=Evolved%20Sleeper&uniqueName=1

    search_parameters = {  # Parameters for api. Key must match documents
        "name": exact_card,
        "uniqueName": True,
    }

    mox_response = requests.get(
        url="https://mox.rouxtaccess.com/api/card/search", params=search_parameters)

    print(mox_response)
    print(f"Card: {exact_card}")

    data = mox_response.json()

    # print(data['data'])
    return int(data['data'][0]['id'])

def get_retailers(id: int, name: str):
    retailers = requests.post(
        f"https://mox.rouxtaccess.com/api/card/{id}/scrape/queued?include=retailer")

    # print(retailers.json())
    retail = {}
    private = {}
    for item in retailers.json()['data']:

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
    print(retail)

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
    for card in cards_df['Item']:
        
        id = get_id(card)

        compiled_retailers.append(get_retailers(id, card)['retail'])
        # compiled_private.append(get_retailers(id, card)['retail'])
        count+=1
        print("###################################")
        print(f'Completed: {count}/{dict_len}')
        print("###################################")



    return compiled_retailers