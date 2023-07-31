import psycopg
import pandas as pd
import json
import requests
from sqlalchemy import create_engine


class PostgresBulk():
    def __init__(self) -> None:
        self.table_name = 'cards'

    def extract(self):

        base_result = requests.get('https://api.scryfall.com/bulk-data').json()
        result = requests.get(base_result['data'][0]['download_uri']).json()
        df = pd.DataFrame(result)
        print(f'Number of entries: {len(df)}')
        return df

    def transform(self, df: pd.DataFrame):
        df.fillna("", inplace=True)
        
        # Columns to flatten:
        columns = [
            'image_uris',
            'legalities',
            'prices',
            'related_uris',
            'purchase_uris',
            'preview',
        ]
       
        for col in columns:
            flattened_df = pd.json_normalize(df[col])
            flattened_df = flattened_df.add_prefix(f'{col}.')
            df = pd.concat([df.drop(columns=[col]), flattened_df], axis=1)
        # temp

        # df = df.drop(columns=['card_faces', 'all_parts'])
        df['all_parts'] = df['all_parts'].apply(lambda x: f'{x}')
        df['card_faces'] = df['card_faces'].apply(lambda x: f'{x}')
        return df

    def add_cards(self, conn):
        engine = create_engine('postgresql+psycopg://postgres@localhost:5432/mtg')
        df = self.extract()
        df = self.transform(df)
        df.to_sql('cards', engine, if_exists='append', index=False)

    def delete_card(self, cursor, oracle_id):
        pass

