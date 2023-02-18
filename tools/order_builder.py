import pandas as pd


class Order_Builder:
    def __init__(self, wanted_cards: pd.DataFrame, stores_df: pd.DataFrame) -> None:
        self.wanted_cards: pd.DataFrame = wanted_cards
        self.stores_df: pd.DataFrame = stores_df
