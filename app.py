from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
# from api.HelloApiHandler import HelloApiHandler

# from api.handlers.tools.load_cards_json import LoadCardsJson
from api.handlers.tools.mox_scraper import MoxScraper
from api.handlers.scryfall.search.exact import ExactSearch
from api.handlers.scryfall.search.fuzzy import FuzzySearch
from api.handlers.scryfall.search.collection import CollectionSearch

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(MoxScraper, '/flask/scrape_mox')
api.add_resource(ExactSearch, '/flask/scryfall/exact')
api.add_resource(FuzzySearch, '/flask/scryfall/fuzzy')
api.add_resource(CollectionSearch, '/flask/scryfall/collection')