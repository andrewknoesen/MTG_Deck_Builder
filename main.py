import tools.card_importer as card_importer
from tools.mox_scraper import scrape_mox
from tools.order_builder import Order_Builder
from utils.response_to_df import flatten_store
import pandas as pd
from pprint import pprint

#TODO: Handle more than 30 responses
#TODO: Show missing cards
#TODO: Config file for shipping costs
#TODO: Handle private

def main():
    # load cards from purchase_list.json
    wanted_cards_df: pd.DataFrame = card_importer.load_cards_from_json()
    pprint(wanted_cards_df)
    stores_list: list = scrape_mox(wanted_cards_df)
    stores_df: pd.DataFrame = flatten_store(stores_list)

    sorted_order: Order_Builder = Order_Builder(stores_df=stores_df, wanted_cards=wanted_cards_df)
    sorted_order_df = sorted_order.optimize_order()
    sorted_order_df.to_csv('order.csv', index=False)
    # pprint(stores_df)
    # build order
    # optimize

if __name__ == "__main__":
    main()