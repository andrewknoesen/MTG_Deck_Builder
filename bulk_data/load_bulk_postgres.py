import json
import pandas as pd
import psycopg
import requests
from api.handlers.database.base_classes.postgres_base import PostgresBase

class JsonToCsv:
    def __init__(self) -> None:
        pass

    def extract(self):
        result = requests.get('https://api.scryfall.com/bulk-data')
        print(result.keys())
        df = pd.DataFrame(result['data'])
        print(f'Number of entries: {len(df)}')
        return df

    def transform(self, df):
        return df

    def load(self, df: pd.DataFrame):
        postgres = PostgresBase()
        print('loading to postgres')
        postgres.update_bulk_table(df)

    def run(self):
        df = self.extract()
        df = self.transform(df)
        self.load(df)

def run():
    converter = JsonToCsv()
    converter.run()

if __name__ == '__main__':
    run()