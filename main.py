import card_importer
from mox_scraper import scrape_mox
from response_to_df import flatten_store
import pandas as pd
from pprint import pprint

def main():
    # load cards from purchase_list.json
    cards = card_importer.load_cards_from_json()
    print(cards)
    stores_list = scrape_mox(cards)
    stores_df = flatten_store(stores_list)
    pprint(stores_df)
    # scrape
    # load into df
    # optimize
    pass


if __name__ == "__main__":
    main()