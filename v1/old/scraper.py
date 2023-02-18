from typing import Dict, List
import requests
import re
import eel
from bs4 import BeautifulSoup
import datetime

base_url = "https://www.mtggoldfish.com/deck_searches/create?utf8=%E2%9C%93" 
deck_name = "&deck_search%5Bname%5D="
deck_format = "&deck_search%5Bformat%5D="
deck_type_user = "&deck_search%5Btypes%5D%5B%5D=user"
deck_type_tournament = "&deck_search%5Btypes%5D%5B%5D=tournament"
deck_type_base = "&deck_search%5Btypes%5D%5B%5D="
deck_player_base = "&deck_search%5Bplayer%5D="
# card_base_format = f"&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bcard%5D=&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bquantity%5D=1&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Btype%5D=maindeck&counter={counter}"

card_base_name = "&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bcard%5D="
card_base_quantity = "&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bquantity%5D="
card_base_board_loc = "&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Btype%5D=" 

def is_deck(href):
    return href and re.compile("deck").search(href)

def update_progress(text):
    eel.display_progress(text)

def goldfish_url_builder(cards: Dict, format, date_start: datetime, date_end:datetime, player = '', name = '', types: List[str] = []):
    '''
    date_start and date_end are date time formats
    
    card = {
        'card_name': qty
    }

    source = ['tournament','user']
    '''

    """

    https://www.mtggoldfish.com/deck_searches/create?utf8=%E2%9C%93&
    deck_search%5Bname%5D=elves&deck_search%5Bformat%5D=
    &deck_search%5Btypes%5D%5B%5D=
    &deck_search%5Btypes%5D%5B%5D=tournament
    &deck_search%5Btypes%5D%5B%5D=user
    &deck_search%5Bplayer%5D=
    &deck_search%5Bdate_range%5D=09%2F25%2F2022+-+10%2F09%2F2022
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bcard%5D=negate
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bquantity%5D=1
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Btype%5D=maindeck
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bcard%5D=
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bquantity%5D=1
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Btype%5D=maindeck
    &counter=4
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B2%5D%5Bcard%5D=Temper
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B2%5D%5Bquantity%5D=1
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B2%5D%5Btype%5D=sideboard
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B3%5D%5Bcard%5D=Herald+of+Anafenza
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B3%5D%5Bquantity%5D=3
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B3%5D%5Btype%5D=maindeck
    &commit=Search
    
    Name: rakdos, format: Pauper, tournament deck, no player given, no cards given
    https://www.mtggoldfish.com/deck_searches/create?utf8=%E2%9C%93
    &deck_search%5Bname%5D=rakdos
    &deck_search%5Bformat%5D=pauper
    &deck_search%5Btypes%5D%5B%5D=
    &deck_search%5Btypes%5D%5B%5D=tournament
    &deck_search%5Bplayer%5D=
    &deck_search%5Bdate_range%5D=09%2F17%2F2022+-+10%2F01%2F2022
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bcard%5D=
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bquantity%5D=1
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Btype%5D=maindeck
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bcard%5D=
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bquantity%5D=1
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Btype%5D=maindeck
    &counter=2
    &commit=Search
    
    Name: rakdos, Format: Pauper, tournament deck, no player given, Temporal Adept >= 4 in main, Negate >= in main, Lightning Bolt >= 1 in side 
    https://www.mtggoldfish.com/deck_searches/create?utf8=%E2%9C%93
    &deck_search%5Bname%5D=rakdos
    &deck_search%5Bformat%5D=pauper
    &deck_search%5Btypes%5D%5B%5D=
    &deck_search%5Btypes%5D%5B%5D=tournament
    &deck_search%5Bplayer%5D=
    &deck_search%5Bdate_range%5D=09%2F17%2F2022+-+10%2F01%2F2022
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bcard%5D=Temporal+Adept
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bquantity%5D=4
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Btype%5D=maindeck
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bcard%5D=
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bquantity%5D=1
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Btype%5D=maindeck
    &counter=4
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B2%5D%5Bcard%5D=Negate
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B2%5D%5Bquantity%5D=4
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B2%5D%5Btype%5D=maindeck
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B3%5D%5Bcard%5D=Lightning+Bolt
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B3%5D%5Bquantity%5D=1
    &deck_search%5Bdeck_search_card_filters_attributes%5D%5B3%5D%5Btype%5D=sideboard
    &commit=Search
    """
    counter = f"&counter={len(cards) + 1}"
    url = f"{deck_name}{name}{deck_format}{format}"
    
    types_url = deck_type_base
    for type in types:
        types_url += f"{deck_type_base}{type}"
    
    url += types_url
    url += f"{deck_player_base}{player}"

    cards_url = ''
    first = True
    for card in cards.keys():
        card = str(card).replace(' ','+')
        if first:
            cards_url += f"{card_base_name}{card}{card_base_quantity}1{card_base_board_loc}maindeck{counter}"
            first = False
        else:
            cards_url += f"{card_base_name}{card}{card_base_quantity}1{card_base_board_loc}maindeck"

    url += cards_url
    url += "&commit=Search"
    



    
def scrape_decks(URL):
    print("Retrieving decks...")

    goldfish = "https://www.mtggoldfish.com" 
    # dl_test = "https://www.mtggoldfish.com/deck/download/5077614" # URL For download test
    decks = []
    
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.find("table", class_="table table-striped")
    
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
        update_progress(f"{curr_count}/{deck_count} complete...\n{retrieved_decks}")

       
    return decks 

