import eel
import random
from datetime import datetime

from card_manager import CardManager
from deck_manager import DeckManager
import scraper as scraper
import ui as ui


dm = DeckManager()
cm = CardManager()

eel.init('ui')

@eel.expose
def get_decks():
    dm.add_decks(scraper.scrape_decks())
    
@eel.expose
def import_cards():
    print("Import called")
    cm.add_cards()

@eel.expose
def get_random_number():
    number = random.randint(1, 100)
    print(number)
    eel.prompt_alerts(number)

@eel.expose
def get_date():
    eel.prompt_alerts(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

@eel.expose
def get_ip():
    eel.prompt_alerts('127.0.0.1')

eel.start('index.html')

