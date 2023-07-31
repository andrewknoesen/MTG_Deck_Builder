import json
import logging
from flask_restful import Api, Resource, reqparse

from api.handlers.database.base_classes.postgres_base import PostgresBase


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | get_card_name_from_oracle.py | %(message)s'
)

class GetNameFromOracle(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('oracle_id', type=str)
        
        args = parser.parse_args()

        logging.info(f"Recieved: {args}")

        params: dict = dict({})

        logging.info(f"Sending params: id:{args['oracle_id']}")

        try:
            postgres = PostgresBase()
            result = postgres.get_card_from_oracle(oracle_id=args['oracle_id'],)
            return dict({
                'statusCode': 200,
                'result': result
            })
        except:
            return '500'

        # return response.json()

