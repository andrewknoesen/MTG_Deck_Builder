import card_importer
from mox_scraper import scrape_mox
from response_to_df import flatten_store
import pandas as pd
from pprint import pprint

#TODO: Handle more than 30 responses
#TODO: Show missing cards
#TODO: Config file for shipping costs
#TODO: Handle private

def main():
    # load cards from purchase_list.json
    cards = card_importer.load_cards_from_json()
    print(cards)
    stores_list = scrape_mox(cards)
    stores_df = flatten_store(stores_list)
    stores_df.to_csv('order.csv', index=False)
    pprint(stores_df)

    # scrape
    # load into df
    # optimize
    pass


if __name__ == "__main__":
    main()