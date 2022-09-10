import requests
import re
import json
from bs4 import BeautifulSoup


def is_deck(href):
    return href and re.compile("deck").search(href)

def get_decks(URL):
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
    for element in links:
        result += str(element)
        result += "\n\n"

        print(f"Retrieving: {element.text}")
        response = requests.get(f"{goldfish}/deck/download/{str(element['href']).split('/')[-1]}")
        cards = str(BeautifulSoup(response.content, "html.parser")).split('\r\n\r\n')
        deck = {
            "name" : element.text,
            "mainboard" : [cards[0].split("\r\n")],
            "sideboard" : [cards[1].split("\r\n")]
        }

        decks.append(deck)

        curr_count += 1
        print(f"{curr_count}/{deck_count} complete...")
       
    return decks 

