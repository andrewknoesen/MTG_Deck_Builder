import requests
import pandas as pd

from CustomLogger.CustomLogger import log_message, log_error, log_info


class MoxScraper:

    url_base: str = "https://moxmonolith.com/card"
    # retailers: list = [2, 3, 4, 6, 11, 13, 15, 16, 18, 19, 20, 21, 26, 34, 36]
    # retailers: list = [2, 3, 4, 11, 13, 15, 18, 19, 20, 21, 22, 23, 24, 25, 26, 32, 33, 34, 35, 37, 39, 40, 41, 42, 43, 44, 45, 46, 48, 51]
    retailers: list = [2, 3, 4, 11, 13, 15, 18, 19, 20, 21, 26, 34, 41, 44, 43, 51, 42]

    def __init__(self) -> None:
        pass

    def get_id(self, card_name: str) -> int | None:

        search_parameters = {
            "name": card_name,
        }

        mox_response = requests.get(
            url=f"{MoxScraper.url_base}/search", params=search_parameters
        )

        if mox_response.status_code == 200:
            for item in mox_response.json()["cards"]:
                if item["name"] == card_name:
                    return item["id"]
        log_error(
            f"{card_name}: \n Query params: {search_parameters} \n {mox_response.json()}"
        )
        return None  # Return None if the item is not found

    def get_cards(self, card_id: int) -> list[dict] | None:
        params = {"retailers[]": MoxScraper.retailers}

        mox_response = requests.get(
            url=f"{MoxScraper.url_base}/{card_id}/products", params=params
        )
        try:
            response_code = mox_response.status_code
            log_message(f"Response code: {response_code}")

            try:
                if "application/json" in mox_response.headers.get("Content-Type", ""):
                    response_body = mox_response.json()
                    # log_message(f"Response body: {response_body}")
                else:
                    log_message("Response is not JSON")
                    log_message(f"Raw response: {mox_response.text}")
            except ValueError as e:
                log_error(f"Failed to parse JSON response: {e}")

        except Exception as e:
            log_error(f"An error occurred: {e}")
        # log_message(f"Response code: {mox_response.status_code} \n Response body: {mox_response.text()}")

        if mox_response.status_code == 200:
            log_message(f"API Response: {mox_response.json()['products']}")
            return mox_response.json()["products"]
        else:
            log_error(f"{card_id}: \n Query params: {params} \n {mox_response.json()}")
            return None

    def scrape_mox(self, card_name: str) -> list[dict] | None:

        id: None | int = self.get_id(card_name)

        if id is not None:
            log_message(f"Querying for {card_name}")
            return self.get_cards(id)
        else:
            return None

    def scrape_mox_df(self, card_name):
        try:
            return_df = pd.json_normalize(self.scrape_mox(card_name))
            return_df["name"] = card_name
            return return_df
        except:
            return pd.DataFrame()

    def convert_price(self, x):
        try:
            return f"R{x/100:.2f}"
        except Exception as e:
            (f"Error converting value: {e}")
            return x  # Return original value if conversion fails

    def format_for_retailer(self, df: pd.DataFrame):
        if df.empty:
            return df

        columns = ["id", "name", "price", "stock", "retailer_name"]

        log_info(df)
        df["price"] = df["price"].apply(lambda x: self.convert_price(x))

        return df[columns]


if __name__ == "__main__":
    scraper = MoxScraper()
    print(scraper.format_for_retailer(scraper.scrape_mox_df("Evolved Sleeper")))
