import json
import pandas as pd
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | card_importer.py | %(message)s'
)

def load_cards_from_json_path(path: str = None):

    '''
    This module loads a card from a path and returns a datafram of the json data
    '''

    cards: dict = dict({})
    df:pd.DataFrame = pd.DataFrame()

    logging.info(f'load_cards_from_json_path(path: {type(path)}={path}) started')

    if path is None: 
        logging.error('File not found. Path is None')
        logging.error(f'Path: {path}')
        raise FileNotFoundError('No path passed to load_cards_from_json') 

    
    with open(path) as json_file:
        cards = json.load(json_file)

    if not cards:
        logging.error(f'No data loaded from path: {path}.')
        logging.error(f'Cards returned is {cards}')
        raise ImportError('File produces empty dict')  

    df = pd.DataFrame(list(cards.items()), columns=['name', 'qty'])
    logging.info(f'Returning df: \n {df.head}')
    return df

def load_cards_from_json(cards: dict = None):

    '''
    This module loads a card from a path and returns a datafram of the json data
    '''

    # cards: dict = dict({})
    df:pd.DataFrame = pd.DataFrame()

    logging.info(f'load_cards_from_json(cards: {type(cards)}={cards}) started')

    if cards is None: 
        logging.error('Empty dict')
        logging.error(f'cards: {cards}')
        raise KeyError('Empty dict passed to load_cards_from_json') 

    
    # with open(path) as json_file:
    #     cards = json.load(json_file)

    if not cards:
        logging.error(f'No data loaded from cards: {cards}.')
        logging.error(f'Cards returned is {cards}')
        raise ImportError('File produces empty dict')  

    df = pd.DataFrame(list(cards.items()), columns=['name', 'qty'])
    logging.info(f'Returning df: \n {df.head}')
    return df
    