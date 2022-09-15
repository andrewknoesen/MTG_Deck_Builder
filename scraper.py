import requests
import re
import eel
from bs4 import BeautifulSoup
import scraper as scraper


def is_deck(href):
    return href and re.compile("deck").search(href)

def update_progress(text):
    # eel.get_decks_eel(text)
    # eel.prompt_alerts(text)
    eel.display_progress(text)
    # print(text)

def scrape_decks(URL):
    print("Retrieving decks...")

    goldfish = "https://www.mtggoldfish.com" 
    # dl_test = "https://www.mtggoldfish.com/deck/download/5077614" # URL For download test
    result = ""
    decks = []
    
    # test = requests.get(dl_test)
    # soup_test = BeautifulSoup(test.content, "html.parser")
    
    # print(soup_test)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.find("table", class_="table table-striped")

    # print(elements.prettify())
    links = elements.find_all("a", href=is_deck)
    deck_count = len(links)
    curr_count = 0
    retrieved_decks = ""

    for element in links:

        retrieved_decks += f"\n{element.text}"
        response = requests.get(f"{goldfish}/deck/download/{str(element['href']).split('/')[-1]}")
        cards = str(BeautifulSoup(response.content, "html.parser")).split('\r\n\r\n')
        deck = {
            "name" : element.text,
            "mainboard" : [cards[0].split("\r\n")],
            "sideboard" : [cards[1].split("\r\n")]
        }

        decks.append(deck)

        curr_count += 1
        # print(f"{curr_count}/{deck_count} complete...\n{retrieved_decks}")
        # eel.display_progress(f"{curr_count}/{deck_count} complete...\n{retrieved_decks}")
        update_progress(f"{curr_count}/{deck_count} complete...\n{retrieved_decks}")

       
    return decks 

