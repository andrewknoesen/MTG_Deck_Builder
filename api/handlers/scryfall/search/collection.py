import json
import logging
from flask_restful import Api, Resource, reqparse
import requests

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | colelction.py | %(message)s'
)

url_base: str = "https://api.scryfall.com"
path: str = "/cards/collection"

class CollectionSearch(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cards', type=dict)
        
        args = parser.parse_args()

        logging.info(f"Recieved: {args}")

        params: dict = dict({})

        params['identifiers'] = args['cards']

        logging.info(f"Sending params: {params}")

        response=requests.post(url=f'{url_base}{path}',json=params['identifiers'])

        return response.json()

