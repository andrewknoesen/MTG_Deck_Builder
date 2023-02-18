import json
import pandas as pd

def load_cards_from_json():
    
    with open("purchase_list.json") as json_file:
        cards = json.load(json_file)

    df = pd.DataFrame(list(cards.items()), columns=['Item', 'Qty'])
    return df
    