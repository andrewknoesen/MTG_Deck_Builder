from time import sleep
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from Scryfall.Scryfall import Scryfall
from OrderOptimizer.OrderOptimizer import OrderOptimizer
from MoxScraper.MoxScraper import MoxScraper

scraper = MoxScraper()
optimizer = OrderOptimizer()
scryfall = Scryfall()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://0.0.0.0:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def validate_order_structure(data):
    # Check if the top-level key 'order' exists and is a list
    if (
        not isinstance(data, dict)
        or "order" not in data
        or not isinstance(data["order"], list)
    ):
        return False

    # Iterate over each item in the 'order' list
    for item in data["order"]:
        # Check if each item is a dictionary
        if not isinstance(item, dict):
            return False

        # Check if each dictionary has the keys 'name' and 'qty'
        if "name" not in item or "qty" not in item:
            return False

        # Check if 'name' is a string and 'qty' is an integer
        if not isinstance(item["name"], str) or not isinstance(item["qty"], int):
            return False

    # If all checks pass, return True
    return True

# ############################################################################ #
#                                  API METHODS                                 #
# ############################################################################ #

@app.get("/get_card_autocomplete")
async def get_card_autocomplete(query: str):    
    return(scryfall.search(query))

@app.post("/optimize_custom_order")
async def optimize_custom_order(body: dict):
    return_df = pd.DataFrame()
    is_valid = validate_order_structure(body)
    
    if not is_valid:
        return {"status": 500, "Message": "Invalid structure"}

    for item in body['order']:
        df = scraper.format_for_retailer(scraper.scrape_mox_df(item['name']))
        if not df.empty:
            return_df = pd.concat([return_df, df], ignore_index=True)

        sleep(1)

    report = optimizer.optimize(return_df, body['order'])

    return {'report': report}

@app.get("/get_card_image")
async def get_card_image(query: str):
    return scryfall.get_image(query)

