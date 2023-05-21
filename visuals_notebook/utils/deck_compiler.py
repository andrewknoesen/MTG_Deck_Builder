import pandas as pd
import requests

# import deck_importer as di


class DeckCompiler():
    def __init__(self) -> None:
        pass

    def get_scryfall(self, deck_list: pd.DataFrame):
        url: str = 'https://api.scryfall.com/cards/collection'

        data = []

        for card in deck_list['card']:
            data.append(dict({
                'name': card
            }))

        page_size: int = 74  # includes 0 so size-1
        # print(data)
        print(f'Number of cards: {len(data)}')
        responses = []
        cards = []

        columns = ['card', 'highres_image', 'mana_cost', 'cmc', 'type_line',
                   'oracle_text', 'colors', 'color_identity', 'produced_mana', 'keywords', 'legalities']
        response_df = pd.DataFrame(columns=columns)

        for i in range(0, len(data), page_size):

            pay_load = dict({
                'identifiers': data[i:i+page_size]
            })

            response = requests.post(url=url, json=pay_load)

            for card in response.json()['data']:
                # print(card['name'])
                
                mana = 'None'
                if 'produced_mana' in card.keys():
                    mana = card['produced_mana']
                
                df_entry = [card['name'], card['highres_image'], card['mana_cost'], card['cmc'], card['type_line'],
                            card['oracle_text'], card['colors'], card['color_identity'], mana, card['keywords'], card['legalities']]
                response_df.loc[len(response_df)] = df_entry

        df1= (pd.merge(deck_list, response_df, on=['card']))
        # print(df1)
        return df1


# def main():
#     importer = di.DeckImporter()
#     compiler = DeckCompiler()

#     df = importer.mtga_importer(
#         path='./../decks/commander/deck.txt', format='commander')
#     compiler.get_scryfall(df)


# if __name__ == '__main__':
#     main()
