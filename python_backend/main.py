import tools.card_importer as card_importer
from tools.mox_scraper import scrape_mox
from tools.order_builder import Order_Builder
from utils.response_to_df import flatten_store
import pandas as pd
from pprint import pprint
import sys

#TODO: Config file for shipping costs
#TODO: Handle private

def main():
    # load cards from purchase_list.json
    wanted_cards_df: pd.DataFrame = card_importer.load_cards_from_json()
    pprint(wanted_cards_df)
    stores_list: list = scrape_mox(wanted_cards_df)
    stores_df: pd.DataFrame = flatten_store(stores_list)
    stores_df.to_csv("unopt_order.csv")

    sorted_order: Order_Builder = Order_Builder(stores_df=stores_df, wanted_cards=wanted_cards_df)
    print(sorted_order.get_stores_def())
    sorted_order_df: pd.DataFrame = sorted_order.optimize_order()
    sorted_order_df.to_csv('order.csv', index=False)
    compared: pd.DataFrame  = sorted_order.compare_cards()
    compared.to_csv('compared.csv', index=False)
    pprint(compared)
    # pprint(stores_df)
    # build order
    # optimize

def post_api_call():
    wanted_cards_df: pd.DataFrame = card_importer.load_cards_from_json()
    sorted_order_df: pd.DataFrame = pd.read_csv('order.csv')
    order_builder: Order_Builder() = Order_Builder()
    order_builder.set_stores_df(sorted_order_df)
    order_builder.set_wanted_df(wanted_cards_df)
    compared: pd.DataFrame = order_builder.compare_cards()
    compared.to_csv('compared.csv', index=False)
    pprint(compared)

if __name__ == "__main__":
    main()

    # if str(sys.argv[1]) == 'p':
    #     post_api_call()
    # else:
    #     main()