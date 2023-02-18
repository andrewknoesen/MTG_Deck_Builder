from collections import defaultdict
from genericpath import exists
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

    def add_cards(self, window_ref: str = 'Choose CSV'):
        root = Tk()
        root.title(window_ref)
        root.withdraw()
        root.wm_attributes('-topmost', 1) # without that it wil go behind all others apps
        file = fd.askopenfilename(parent=root, filetypes=(("CSV Files","*.csv"),))

        # holder = pd.read_csv(file).set_index('Card_Name').T.to_dict()
        holder = pd.read_csv(file).T.to_dict('list')

        # card_list: list = []
        # for k,v in holder.items():
        #     card_list.append(holder[k][0])

        # D = defaultdict(list)
        # for i,item in enumerate(card_list):
        #     D[item].append(i)
        # D = {k:v for k,v in D.items() if len(v)>1}

        D = {}
        for i,item in holder.items():
            if item[0] in D.keys(): 
                D[item[0]] += int(item[1])
            else:
                D[item[0]] = int(item[1])
        # print(json.dumps(D, indent=4))
        self.cards = {**self.cards,**D}

        # df = pd.DataFrame(self.cards).T.reset_index()
        # df.columns.values[0] = "Card_Name"
        # df.to_csv(card_csv, header=True, index=False)

        # print(self.cards)

        # eel.show_decks_eel(json.dumps(self.cards))

    def get_cards(self):
        return self.cards