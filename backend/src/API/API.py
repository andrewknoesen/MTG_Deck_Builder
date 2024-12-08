import logging
from time import sleep
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger
import pandas as pd
from Scryfall.Scryfall import Scryfall
from OrderOptimizer.OrderOptimizer import OrderOptimizer
from MoxScraper.MoxScraper import MoxScraper
import uvicorn
from API.config import LOG_CONFIG, HOST, PORT, DISABLE_PACKAGE_LOGGING

logging.config.fileConfig(LOG_CONFIG, disable_existing_loggers=DISABLE_PACKAGE_LOGGING)
logger = logging.getLogger(__name__)

scraper = MoxScraper()
optimizer = OrderOptimizer()
scryfall = Scryfall()

app = FastAPI(
    swagger_ui_parameters={
        "filter": True,
        "syntaxHighlight.theme": "arta",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
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


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log request details
    logger.info(f"Request: {request.method} {request.url}")

    # Process the request and get the response
    response = await call_next(request)

    # Log response details (optional)
    logger.info(f"Response status: {response.status_code}")

    return response


@app.get("/get_card_autocomplete")
async def get_card_autocomplete(query: str):
    return scryfall.search(query)


@app.post("/optimize_custom_order")
async def optimize_custom_order(body: dict):
    return_df = pd.DataFrame()
    is_valid = validate_order_structure(body)

    if not is_valid:
        return {"status": 500, "Message": "Invalid structure"}

    for item in body["order"]:
        df = scraper.format_for_retailer(scraper.scrape_mox_df(item["name"]))
        if not df.empty:
            return_df = pd.concat([return_df, df], ignore_index=True)

        sleep(1)

    report = optimizer.optimize(return_df, body["order"])

    return {"report": report}


@app.get("/get_card_image")
async def get_card_image(query: str):
    return scryfall.get_image(query)


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level=logging.INFO,
        log_config=str(LOG_CONFIG),
        use_colors=True,
    )
