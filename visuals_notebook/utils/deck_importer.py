'''
Python class to import decks
'''

import pandas as pd
import numpy as np

class DeckImporter:
    
    def __init__(self) -> None:
        pass

    def commander_handler(self, deck_text: str) -> pd.DataFrame:
        '''
        Handler for commander decks
        '''

        columns = ['card', 'qty', 'commander']

        deck = pd.DataFrame(columns=columns)
        commander = True

        for line in deck_text:
                if line.strip('\n') != '':
                    line_split = line.strip('\n').split(maxsplit=1)
                    df_entry = [line_split[1], line_split[0], commander]
                    
                    deck.loc[len(deck)] = df_entry

                    if commander:
                        commander = False

        return deck

    def sixty_card_handler(self, deck_text: str) -> pd.DataFrame:
        '''
        Handler for 60 card format decks
        '''

        columns = ['card', 'qty', 'commander']

        deck = pd.DataFrame(columns=columns)

        for line in deck_text:
                if line.strip('\n') != '':
                    line_split = line.strip('\n').split(maxsplit=1)
                    df_entry = [line_split[1], line_split[0]]
                    
                    deck.loc[len(deck)] = df_entry

        return deck


    def mtga_importer(self, path: str, format: str) -> pd.DataFrame:
        print('Importing...')
        print(f'Path: {path}')
        deck_df = pd.DataFrame()

        with open(path) as deck_text:
            match format:
                case 'commander':
                    deck_df = self.commander_handler(deck_text)
                case _:
                    deck_df = self.sixty_card_handler(deck_text)

        return deck_df
    

# def main():
#     di = DeckImporter()
#     print(di.mtga_importer(path='./../decks/commander/deck.txt', format='commander'))

# if __name__ == '__main__':
#     main()