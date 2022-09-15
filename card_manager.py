import pandas as pd

class CardManager:
    def __init__(self, csv: str):
        self.cards_df = pd.read_csv(csv)