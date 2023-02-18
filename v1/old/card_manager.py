import json
import random
import pandas as pd
import eel
from tkinter import filedialog as fd
from tkinter import Tk, messagebox
import os


card_csv = "Card_List.csv"

class CardManager:
    def __init__(self):
        try:
            self.cards = pd.read_csv(card_csv).set_index('Card_Name').T.to_dict()
        except:
            self.cards = {}

    def add_cards(self):
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1) # without that it wil go behind all others apps
        file = fd.askopenfilename(parent=root, filetypes=(("CSV Files","*.csv"),))
        
        holder = pd.read_csv(file).set_index('Card_Name').T.to_dict()

        self.cards = {**self.cards,**holder}

        df = pd.DataFrame(self.cards).T.reset_index()
        df.columns.values[0] = "Card_Names"
        df.to_csv(card_csv, header=True, index=False)

        print(self.cards)

        eel.show_decks_eel(json.dumps(self.cards))

    def get_cards(self):
        return self.decks