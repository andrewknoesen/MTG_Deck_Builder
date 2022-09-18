import pandas as pd
import eel
from tkinter import filedialog as fd
from tkinter import Tk, messagebox
import os




class CardManager:
    def __init__(self):
        self.cards_df = []

    def add_cards(self):



        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1) # without that it wil go behind all others apps
        file = fd.askopenfilename(parent=root, filetypes=(("CSV Files","*.csv"),))
        

        # filename = fd.askopenfilename()
        eel.import_cards_eel(file)
        # pd.read_csv(csv)
        # self.decks.append(csv_path)
        # eel.get_decks_eel(self.cards_df)

    def get_cards(self):
        return self.decks