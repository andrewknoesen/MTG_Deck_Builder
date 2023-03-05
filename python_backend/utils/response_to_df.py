from pprint import pprint
import pandas as pd

def create_retailer_dict(compiled_retailers: list):
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

def flatten_store(list_data):
    data = create_retailer_dict(list_data)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    pprint(list_data)
    flattened_data = []
    for store, items in data.items():
        for item in items:
            item['store'] = store
            item['shipping'] = 90
            flattened_data.append(item)

    return pd.DataFrame(flattened_data)