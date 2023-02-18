import requests
import re
import eel
from bs4 import BeautifulSoup
import scraper as scraper
import pandas

class DeckManager:
    def __init__(self):
       self.decks = []

    def add_decks(self, decks):
        self.decks.append(decks)
        eel.get_decks_eel(decks)

    def get_decks(self):
        return self.decks

    