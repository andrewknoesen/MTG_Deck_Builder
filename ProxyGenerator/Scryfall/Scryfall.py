import requests
from PIL import Image
from io import BytesIO

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

    def get_image(self, card_name: str, set: str | None = None):
        params = {
            'fuzzy': f'++{card_name}',
            'fromat': 'image'
        }

        if set is not None:
            params['set'] = set

        scryfall_response = requests.get(
            url = f'{self.url_base}/cards/named', params=params
        )

        img_resp = requests.get(scryfall_response.json()['image_uris']['normal'])

        return Image.open(BytesIO(img_resp.content ))



if __name__ == "__main__":
    s = Scryfall()

    print(s.get_image('llanowar elves', 'gnt'))
