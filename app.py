from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
#comment this on deployment
# from api.HelloApiHandler import HelloApiHandler

# from api.handlers.tools.load_cards_json import LoadCardsJson
from api.handlers.tools.mox_scraper import MoxScraper
from api.handlers.scryfall.search.exact import ExactSearch
from api.handlers.scryfall.search.fuzzy import FuzzySearch
from api.handlers.scryfall.search.collection import CollectionSearch

from api.handlers.database.handlers.upsert_collection import UpsertCollection
from api.handlers.database.handlers.upsert_collection_from_name import UpsertCollectionFromName 
from api.handlers.database.handlers.delete_from_collection import DeleteFromCollection
from api.handlers.database.handlers.get_card_name_from_oracle import GetNameFromOracle
from api.handlers.database.handlers.get_oracle_from_card_name import GetOracleFromName

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
app.debug = True
CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", methods=['POST', 'PUT', 'GET', 'DELETE'], defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(MoxScraper, '/flask/scrape_mox')
api.add_resource(ExactSearch, '/flask/scryfall/exact')
api.add_resource(FuzzySearch, '/flask/scryfall/fuzzy')
api.add_resource(CollectionSearch, '/flask/scryfall/collection')

api.add_resource(UpsertCollection, '/flask/postgres/upsert_collection')
api.add_resource(UpsertCollectionFromName, '/flask/postgres/upsert_collection_from_name')
api.add_resource(DeleteFromCollection, '/flask/postgres/delete_from_collection')
api.add_resource(GetNameFromOracle, '/flask/postgres/get_card_from_oracle')
api.add_resource(GetOracleFromName, '/flask/postgres/get_oracle_from_name')