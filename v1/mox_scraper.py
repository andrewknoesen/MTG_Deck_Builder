import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib

pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', None)  # or 199

def get_id(exact_card: str):
    # https://mox.rouxtaccess.com/api/card/search?name=Evolved%20Sleeper&uniqueName=1

    search_parameters = {  # Parameters for api. Key must match documents
        "name": exact_card,
        "uniqueName": True,
    }

    mox_response = requests.get(
        url="https://mox.rouxtaccess.com/api/card/search", params=search_parameters)

    print(mox_response)

    data = mox_response.json()

    # print(data['data'])
    return int(data['data'][0]['id'])


def get_retailers(id: int, name: str):
    retailers = requests.post(
        f"https://mox.rouxtaccess.com/api/card/{id}/scrape/queued?include=retailer")

    # print(retailers.json())
    retail = {}
    private = {}
    for item in retailers.json()['data']:

        if '?' not in item['priceRead']:
            retail[item['id']] = {
                'name': name,
                'name_long': item['name'],
                'cost': float(item['priceRead'][1:].replace(",", "")),
                'qty': item['stock'],
                'supplier': item['retailer']['name'],
                'link': item['link']
            }
        else:
            private[item['id']] = {
                'name': name,
                'name_long': item['name'],
                'cost': item['priceRead'],
                'qty': item['stock'],
                'supplier': item['retailer']['name'],
                'link': item['link']
            }

    print("###################################")
    print("Returned retailer:")
    print("###################################")
    pprint(retail)

    return {
        'retail': retail,
        'private': private
    }


def create_retailer_dict(compiled_retailers: list, cards: dict):
    retailer_dict = {}

    for items in compiled_retailers:

        for id, item in items.items():
            if item['supplier'] in retailer_dict.keys():

                retailer_dict[item['supplier']].append(
                    {
                        'id': id,
                        'cost': item['cost'],
                        'link': item['link'],
                        'name': item['name'],
                        'name_long': item['name_long'],
                        'qty': item['qty'],
                    }
                )

                # Sort list
                sorted_list = sorted(
                    retailer_dict[item['supplier']], key=lambda x: x['cost'])
                retailer_dict[item['supplier']] = sorted_list

            else:
                retailer_dict[item['supplier']] = [{
                    'id': id,
                    'cost': item['cost'],
                    'link': item['link'],
                    'name': item['name'],
                    'name_long': item['name_long'],
                    'qty': item['qty'],
                }]

        # print('#########################################################')
        # pprint(item)

    return retailer_dict


def flatten_stock(data):
    flattened_data = []
    for store, items in data.items():
        for item in items:
            item['store'] = store
            item['shipping'] = 90
            flattened_data.append(item)

    return pd.DataFrame(flattened_data)


def flatten_order(d):
    df = pd.DataFrame(list(d.items()), columns=['Item', 'Qty'])
    return df


def place_order(suppliers_df, order_df):
    print("###################################")
    print("Supplier DF")
    print("###################################")
    pprint(suppliers_df)
    print("###################################")
    print("Order Df")
    print("###################################")
    pprint(order_df)
    print("###################################")
    # Create a new dataframe to store the final order information
    final_order = pd.DataFrame(
        columns=["store", "Item", "Qty", "cost", "shipping"])
    # Iterate through the items in the order
    for index, row in order_df.iterrows():
        item = row["Item"]
        qty = row["Qty"]
        # Subset the suppliers dataframe to only include suppliers that have the item in stock
        item_suppliers = suppliers_df[(suppliers_df["name"] == item) & (
            suppliers_df["qty"] >= qty)]

        if item_suppliers.empty:
            # if there is no supplier has enough stock then we will split the order over multiple suppliers with items of the same name but different costs
            item_suppliers = suppliers_df[suppliers_df["name"] == item]
            item_suppliers = item_suppliers.sort_values(by=["cost"])
            remaining_qty = qty
            for _, supplier_row in item_suppliers.iterrows():
                if remaining_qty > 0:
                    if remaining_qty > supplier_row["qty"]:
                        order_qty = supplier_row["qty"]
                        remaining_qty -= order_qty
                    else:
                        order_qty = remaining_qty
                        remaining_qty = 0
                    temp_df = pd.DataFrame({"store": supplier_row["store"],
                                                      "Item": item,
                                                      "Link": supplier_row['link'],
                                                      "Qty": order_qty,
                                                      "cost": supplier_row["cost"],
                                                      "shipping": supplier_row["shipping"]}, index=[0])    
                    final_order = pd.concat([final_order,temp_df], ignore_index=True)
        # else:
        #     # sort by cost and take the first supplier
        #     item_suppliers = item_suppliers.sort_values(by=["cost"])
        #     supplier = item_suppliers.iloc[0]
        #     print("###################################")
        #     print(f'current entry : {index}')
        #     print("###################################")
        #     pprint(supplier)
        #     print("###################################")
        #     temp_df = pd.DataFrame({"store": supplier["store"],
        #                                     "Item": item,
        #                                     "Link": supplier_row['link'],
        #                                     "Qty": qty,
        #                                     "cost": supplier["cost"],
        #                                     "shipping": supplier["shipping"]}, index=[0])
            final_order = pd.concat([final_order,temp_df], ignore_index=True)
    print("###################################")
    print("Final order")
    print("###################################")
    pprint(final_order)
    print("###################################")
    return final_order


def calculate_order_cost(final_df):
    total_cost = 0
    suppliers = set()
    for i, row in final_df.iterrows():
        total_cost += row['cost']
        if row['store'] not in suppliers:
            total_cost += row['shipping']
            suppliers.add(row['store'])
    return total_cost


compiled_retailers = []
compiled_private = []
# cards = {
#     # 'Stomping Ground': 4,
#     'Windswept Heath': 3
#     # 'Karador, Ghost Chieftain': 1
#     }

with open("purchase_list.json") as json_file:
    cards = json.load(json_file)

cards_df = flatten_order(cards)
dict_len = len(cards.keys())
print("###################################")
print(f'Cards loaded: {dict_len}')
pprint(cards_df)
print("###################################")
count = 0
for card in cards.keys():
    
    id = get_id(card)

    compiled_retailers.append(get_retailers(id, card)['retail'])
    # compiled_private.append(get_retailers(id, card)['retail'])
    count+=1
    print("###################################")
    print(f'Completed: {count}/{dict_len}')
    print("###################################")

compiled_retailer_dict = create_retailer_dict(compiled_retailers, cards)

compiled_retailer_df = flatten_stock(compiled_retailer_dict)
print("###################################")
print("Compiled pre exec dict")
print("###################################")
pprint(compiled_retailer_dict)
print("###################################")

print("###################################")
print("Compiled pre exec df")
print("###################################")
pprint(compiled_retailer_df)
print("###################################")

order = place_order(compiled_retailer_df, cards_df)
order.to_csv("./order.csv", index=False)
print("###################################")
print("###################################")
print(f'Total cost: R {calculate_order_cost(order)}')
