import json
import logging
from flask_restful import Api, Resource, reqparse

from api.handlers.database.base_classes.postgres_base import PostgresBase


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | delete_card_from_collection.py | %(message)s'
)

class DeleteFromCollection(Resource):
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('oracle_id', type=str)
        
        args = parser.parse_args()

        logging.info(f"Recieved: {args}")

        params: dict = dict({})

        logging.info(f"Sending params: id:{args['oracle_id']}")

        try:
            postgres = PostgresBase()
            postgres.delete_card_from_collection(oracle_id=args['oracle_id'])
            return '200'
        except:
            return '500'

        # return response.json()

