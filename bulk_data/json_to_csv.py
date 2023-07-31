import json
import pandas as pd

class JsonToCsv:
    def __init__(self) -> None:
        pass

    def extract(self):
        with open('./oracle-cards.json') as f:
            df = pd.DataFrame(json.load(f))
        print(f'Number of entries: {len(df)}')
        return df

    def transform(self, df):
        return df

    def load(self, df: pd.DataFrame):
        df.to_csv('cards.csv')

    def run(self):
        df = self.extract()
        df = self.transform(df)
        self.load(df)

def run():
    converter = JsonToCsv()
    converter.run()

if __name__ == '__main__':
    run()