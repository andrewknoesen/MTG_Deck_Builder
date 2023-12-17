import requests
import pandas as pd

class MoxScraper:

    url_base: str = 'https://moxmonolith.com/card'
    retailers: list = [2, 3, 4, 6, 11, 13, 15, 16, 18, 19, 20, 21, 26, 34, 5]

    def __init__(self) -> None:
        pass

    def get_id(self, card_name: str) -> int | None:

        search_parameters = {
            "name": card_name,
        }

        mox_response = requests.get(
            url=f"{MoxScraper.url_base}/search", params=search_parameters)

        if mox_response.status_code == 200:
            for item in mox_response.json()['cards']:
                if item['name'] == card_name:
                    return item['id']
        return None  # Return None if the item is not found

    def get_cards(self, card_id: int) -> list[dict] | None:

        params = {
            'retailers[]': MoxScraper.retailers
        }

        mox_response = requests.get(
            url=f"{MoxScraper.url_base}/{card_id}/products",
            params=params
        )

        if mox_response.status_code == 200:
            return mox_response.json()['products']
        else: 
            return None
    
    def scrape_mox(self, card_name: str) -> list[dict] | None:
        
        id: None | int = self.get_id(card_name)

        if id is not None:
            return self.get_cards(id)
        else:
            return None
        
    def scrape_mox_df(self, card_name):
        return pd.json_normalize(self.scrape_mox(card_name))
        
if __name__ == '__main__':
    scraper = MoxScraper()
    print(scraper.scrape_mox_df('Evolved Sleeper'))