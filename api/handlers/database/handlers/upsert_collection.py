import json
import logging
from flask_restful import Api, Resource, reqparse

from api.handlers.database.base_classes.postgres_base import PostgresBase


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | upsert_collection.py | %(message)s'
)

class UpsertCollection(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('oracle_id', type=str)
        parser.add_argument('qty', type=int, default=1)
        
        args = parser.parse_args()

        logging.info(f"Recieved: {args}")

        params: dict = dict({})

        logging.info(f"Sending params: id:{args['oracle_id']}, qty:{args['qty']}")

        try:
            postgres = PostgresBase()
            postgres.upsert_collection(oracle_id=args['oracle_id'], qty=args['qty'])
            return '200'
        except:
            return '500'

        # return response.json()

