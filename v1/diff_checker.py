from typing import Dict


def compare_cards(my_collection: Dict, deck_want: Dict):
    '''
    Dictionary structures:
    {
        card_name: qty
    }
    '''
    need: Dict = {}
    total_deck: int = 0
    total_need: int = 0

    for card, qty in deck_want.items():
        total_deck +=  qty
        if card in my_collection:
            qty_need: int = int(qty) - int(my_collection[card])
        else:
            qty_need: int = int(qty)

        if qty_need > 0:
            total_need += qty_need
            need[card] = qty_need
   
    return {
        'Percantage you have': 100.0-(100.0*float(total_need)/float(total_deck)),
        'Cards to get': need
        }


# have_test ={
#     'Card 1' : 2,
#     'Card 2' : 5
# }

# need_test = {
#     'Card 3': 2,
#     'Card 2': 2
# }

# print(compare_cards(have_test, need_test))