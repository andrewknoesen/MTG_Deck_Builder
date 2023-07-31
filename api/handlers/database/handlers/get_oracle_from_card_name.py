import json
import logging
from flask_restful import Api, Resource, reqparse

from api.handlers.database.base_classes.postgres_base import PostgresBase


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | get_card_name_from_oracle.py | %(message)s'
)

class GetOracleFromName(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('card', type=str)
        
        args = parser.parse_args()

        logging.info(f"Recieved: {args}")

        params: dict = dict({})

        logging.info(f"Sending params: card:{args['card']}")

        try:
            postgres = PostgresBase()
            result = postgres.get_oracle_from_card(card=args['card'],)
            return dict({
                'statusCode': 200,
                'result': result
            })
        except:
            return '500'

        # return response.json()

