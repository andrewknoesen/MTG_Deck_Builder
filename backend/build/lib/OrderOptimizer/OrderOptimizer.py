import pandas as pd
import pulp as pl

from time import sleep
from MoxScraper.MoxScraper import MoxScraper
import pandas as pd


class OrderOptimizer:
    def __init__(self) -> None:
        self.shipping_cost = {
            'D20Battleground': 90,
            'Greedy Gold': 100,
            'Sword & Board': 80,
            'Luckshack': 20,
            'Geek Home Deckbox': 0,
            'Dracoti': 120,
            'The Warren': 0,
            'The Stone Dragon': 100,
            'Mirage Gaming': 100,
            'TopDeck': 70,
            'UnderworldConnections': 0,
            'TCG Trader': 100,
            'Untapped Lands': 100,
            'Battle Bunker Paarl': 0,
            'D20Battleground': 90,
            'Big Bang Shop': 100
        }

    def optimize(self, df: pd.DataFrame, orders: list[dict]):
        error: bool = False
        error = not self.validate_order_dict(orders)

        if error:
            return None

        card_df = df.copy()
        card_df['name'] = card_df['name'].astype(str) + '-' + card_df['id'].astype(str)
        card_df = card_df.drop('id', axis=1)
        card_df['price'] = card_df['price'].str.replace('R', '').astype(float)
        card_df = card_df.dropna(subset=['price'])

        # Convert to dictionary
        cost = {(row['name'], row['retailer_name']): row['price']
                for _, row in card_df.iterrows()}
        stock = {(row['name'], row['retailer_name']): row['stock']
                 for _, row in card_df.iterrows()}

        # Apply filter for available stock
        cards = self.filter_cards(orders=orders, df=df)

        problem = pl.LpProblem("Magic_Magic", pl.LpMinimize)

        M = 10000   

        selected_indicator = pl.LpVariable.dicts(
            "card_store_qty",
            set(cost.keys()),
            cat=pl.constants.LpInteger
        )

        # Binary variables for shipping cost conditions
        shipping_indicator = pl.LpVariable.dicts(
            "shipping_indicator",
            set(cost.keys()),
            cat=pl.LpBinary
        )

        for card in cards:
            problem += pl.lpSum([selected_indicator[(c, s)] for c, s in selected_indicator.keys()
                                if c.rsplit('-', 1)[0] == card['name']]) >= card['qty']

        for key in stock.keys():
            problem += selected_indicator[key] <= stock[key]

            # Add Big M constraints for shipping costs
            problem += selected_indicator[key] <= M * shipping_indicator[key]
            problem += selected_indicator[key] >= shipping_indicator[key]
            problem += shipping_indicator[key] <= 1

        objective_terms = []

        for key in cost.keys():
            # item costs
            objective_terms.append(selected_indicator[key] * cost[key])
            # Add shipping costs
            objective_terms.append(
                shipping_indicator[key] * self.shipping_cost[key[1]])

        problem += pl.lpSum(objective_terms)

        status = problem.solve(pl.PULP_CBC_CMD())

        return_str = ""
        return_str += f"Status: {pl.LpStatus[status]}"
        total_cost = 0

        return_str += '\n# --------------------------------- purchases -------------------------------- #\n'
        for var in selected_indicator:
            if selected_indicator[var].varValue > 0:
                return_str += f"{var}: {selected_indicator[var].varValue} at R{cost[var]} each --> R{selected_indicator[var].varValue * cost[var]}\n"
                total_cost += selected_indicator[var].varValue * cost[var]

        return_str += '\n# --------------------------------- shipping --------------------------------- #\n'
        for var in shipping_indicator:
            if shipping_indicator[var].varValue > 0:
                return_str += f"{var}: R{shipping_indicator[var].varValue * self.shipping_cost[var[1]]}\n"
                total_cost += shipping_indicator[var].varValue * \
                    self.shipping_cost[var[1]]

        return_str += '\n# -------------------------------- breakdown -------------------------------- #\n'
        for var in shipping_indicator:
            if shipping_indicator[var].varValue > 0:
                return_str += f"{var}: R{(selected_indicator[var].varValue * cost[var]) + shipping_indicator[var].varValue * self.shipping_cost[var[1]]}\n"

        return_str += '\n# ----------------------------------- total ---------------------------------- #\n'
        return_str += f"Total Cost: {total_cost}"

        return return_str

    def filter_cards(self, orders: list[dict], df: pd.DataFrame) -> list[dict]:
        """This function filters the cards that are available and adjusts the order list to only cards that are available.

        Args:
            orders (list[dict]): list of dictionaries containing the order
            df (pd.DataFrame): dataframe that contains the available stock

        Returns:
            list[dict]: list of dictionaries for the order that is achievable based off of what stock is available
        """
        cards = []

        for order in orders:
            amount = sum(df[df["name"] == order['name']]["stock"])
            if amount < order['qty']:
                cards.append({
                    'name': order['name'],
                    'qty': amount
                })
            else:
                cards.append({
                    'name': order['name'],
                    'qty': order['qty']
                })

        return cards

    def validate_order_dict(self, order: list[dict]) -> bool:
        """Checks to see if this list of dictionaries is of the expected structure. 
        Will return true if the list is valid

        Args:
            order (list[dict]): List of dictionaries containing the orders

        Returns:
            bool: Whether the list is valid or not
        """
        # ----------------------- Check if the input is a list ----------------------- #
        if not isinstance(order, list):
            return False

        # ----------------- Define the required keys and their types ----------------- #
        required_keys = {
            'name': str,
            'qty': int
        }

        # -------------------- Iterate over each item in the list -------------------- #
        for item in order:
            # --------------------- Check if the item is a dictionary -------------------- #
            if not isinstance(item, dict):
                return False

            # ----- Check if all required keys are present and have the correct type ----- #
            for key, expected_type in required_keys.items():
                if key not in item or not isinstance(item[key], expected_type):
                    return False

        # ---------------------- If all checks pass, return True --------------------- #
        return True

    def validate_scraped_df(self, df: pd.DataFrame) -> bool:
        pass


def main():
    wants = [
        {
            'name': "Wild Growth",
            'qty': 3
        },
        {
            'name': "Malevolent Rumble",
            'qty': 3
        },
        {
            'name': "Mwonvuli Acid-Moss",
            'qty': 4
        },
        {
            'name': "Utopia Sprawl",
            'qty': 4
        },
        {
            'name': "Thermokarst",
            'qty': 4
        },
        {
            'name': "Annoyed Altisaur",
            'qty': 4
        },
        {
            'name': "Writhing Chrysalis",
            'qty': 4
        },
        {
            'name': "Arbor Elf",
            'qty': 4
        },
        {
            'name': "Eldrazi Repurposer",
            'qty': 4
        },
        {
            'name': "Avenging Hunter",
            'qty': 4
        },
        {
            'name': "Boarding Party",
            'qty': 4
        },
        {
            'name': "Wooded Ridgeline",
            'qty': 1
        },
        {
            'name': "Tamiyo's Safekeeping",
            'qty': 1
        },
        {
            'name': "Cast into the Fire",
            'qty': 1
        },
        {
            'name': "Relic of Progenitus",
            'qty': 3
        },
        {
            'name': "Breath Weapon",
            'qty': 3
        },
        {
            'name': "Gorilla Shaman",
            'qty': 1
        },
        {
            'name': "Deglamer",
            'qty': 4
        },
        {
            'name': "Weather the Storm",
            'qty': 2
        },
    ]

    return_df = pd.DataFrame()
    scraper = MoxScraper()
    optimizer = OrderOptimizer()

    for item in wants:
        df = scraper.format_for_retailer(scraper.scrape_mox_df(item['name']))
        if not df.empty:
            return_df = pd.concat([return_df, df], ignore_index=True)

        sleep(5)

    report = optimizer.optimize(return_df, wants)

    print(report)


if __name__ == "__main__":
    main()
