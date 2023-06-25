import logging
from flask_restful import Api, Resource, reqparse

from python_backend.tools import (
    mox_scraper as ms,
    card_importer as ci
)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | load_cards_json.py | %(message)s'
)

class MoxScraper(Resource):
    def post(self):
        logging.info(f'self: {self}')

        parser = reqparse.RequestParser()
        parser.add_argument('cards', type=dict)

        args = parser.parse_args()

        logging.info(f'args: {args}')
        # note, the post req from frontend needs to match the strings here (e.g. 'type and 'message')

        cards = args['cards']
        # ret_status, ret_msg = ReturnData(request_type, request_json)
        # currently just returning the req straight

        if cards:
            # message = "Your cards Requested: {}".format(cards)
            cards_df = ci.load_cards_from_json(cards=cards)
            final_ret = {"status": "Success", "data_frame": ms.scrape_mox(cards_df=cards_df)}
        else:
            messafinal_ret = {"status": "Success", "data_frame": "No cards given"}
        
        # final_ret = {"status": "Success", "data_frame": load_cards_from_json(cards=cards)}

        return final_ret