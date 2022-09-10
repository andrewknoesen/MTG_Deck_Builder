from tkinter import *
import eel
import random
from datetime import datetime


import scraper as scraper
import ui as ui

URL = "https://www.mtggoldfish.com/deck_searches/create?utf8=%E2%9C%93&deck_search%5Bname%5D=&deck_search%5Bformat%5D=&deck_search%5Btypes%5D%5B%5D=&deck_search%5Btypes%5D%5B%5D=tournament&deck_search%5Btypes%5D%5B%5D=user&deck_search%5Bplayer%5D=&deck_search%5Bdate_range%5D=08%2F27%2F2022+-+09%2F10%2F2022&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bcard%5D=Temporary+Lockdown&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bquantity%5D=1&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Btype%5D=maindeck&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bcard%5D=&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bquantity%5D=1&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Btype%5D=maindeck&counter=2&commit=Search"


eel.init('ui')

@eel.expose
def get_decks():
    eel.display_output(scraper.get_decks(URL))

@eel.expose
def get_random_number():
    eel.prompt_alerts(random.randint(1, 100))

@eel.expose
def get_date():
    eel.prompt_alerts(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

@eel.expose
def get_ip():
    eel.prompt_alerts('127.0.0.1')

eel.start('index.html')

