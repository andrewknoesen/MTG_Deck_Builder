import requests

class Scryfall:
    def __init__(self) -> None:
        self.url_base: str = 'https://api.scryfall.com'


    def search(self, q: str):
        params = {
            "q": q
        }

        scryfall_response = requests.get(
            url=f"{self.url_base}/cards/autocomplete", params=params)
        
        return scryfall_response.json()['data']

if __name__ == "__main__":
    s = Scryfall()

    print(s.search('bob'))