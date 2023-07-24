import logging
from flask_restful import Api, Resource, reqparse
import requests

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | fuzzy.py | %(message)s'
)

url_base: str = "https://api.scryfall.com"
path: str = "/cards/autocomplete"

class FuzzySearch(Resource):
    def post(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('card', type=str)

        args = parser.parse_args()

        params: dict = dict({})

        params['q'] = args['card']

        response=requests.get(url=f'{url_base}{path}',params=params)

        return response.json()

