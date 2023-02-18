import json
from textwrap import indent
from typing import Collection
import scryfall_functions
from card_importer import CardManager
import diff_checker

# print(json.dumps(scryfall_functions.exact('Evolved Sleeper'), indent=4))

'''
Compare have and want.

scrape cards and return dict:
{
    card: {
        location: {
            cost: qty_available
        }
    }
}
'''

deck: CardManager = CardManager()

deck.add_cards('Choose deck you want (CSV)')

my_collection: CardManager = CardManager()

my_collection.add_cards('Choose your inventory (CSV)')

# print(f"Deck \n{json.dumps(deck.get_cards(), indent=4)}")
# print(f"Collection \n{json.dumps(my_collection.get_cards(), indent=4)}")

print(f"Cards needed \n{json.dumps(diff_checker.compare_cards(my_collection=my_collection.get_cards(), deck_want=deck.get_cards()), indent=4)}")
