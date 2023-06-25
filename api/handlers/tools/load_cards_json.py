import logging
from flask_restful import Api, Resource, reqparse

from python_backend.tools.card_importer import load_cards_from_json

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | load_cards_json.py | %(message)s'
)

class LoadCardsJson(Resource):
    def get(self):
        return{
            'status': 200,
            'message': "SUCCESS"
        }
    
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
            final_ret = {"status": "Success", "data_frame": load_cards_from_json(cards=cards)}
        else:
            messafinal_ret = {"status": "Success", "data_frame": "No cards given"}
        
        # final_ret = {"status": "Success", "data_frame": load_cards_from_json(cards=cards)}

        return final_ret