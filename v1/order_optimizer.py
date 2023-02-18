import pandas as pd

def place_order(suppliers_df, items_df):
  # create a new dataframe to store the final order
  order_df = pd.DataFrame(columns=['item', 'supplier', 'quantity', 'cost'])

  # initialize a dictionary to store the total shipping cost for each supplier
  total_shipping_costs = {}

  # loop through each item in the items dataframe
  for index, item in items_df.iterrows():
    # get the list of suppliers that have the item in stock
    item_suppliers = suppliers_df[suppliers_df['item'] == item['item']]

    # sort the suppliers by the cost of shipping
    item_suppliers = item_suppliers.sort_values(by='shipping_cost')

    # initialize variables to track the total cost and quantity of the item
    total_cost = 0
    total_quantity = 0
    order_quantity = item['order_quantity']

    # loop through each supplier and add as much of the item as we can afford
    for supplier_index, supplier in item_suppliers.iterrows():
      # calculate the maximum quantity we can afford to buy from this supplier
      max_quantity = int((order_quantity - total_quantity) / (item['cost'] + supplier['shipping_cost']))

      # if the supplier has enough stock to meet the demand, buy the full amount
      if max_quantity >= order_quantity:
        # add the shipping cost for this supplier to the total_shipping_costs dictionary if it's not already there
        if supplier['supplier'] not in total_shipping_costs:
          total_shipping_costs[supplier['supplier']] = supplier['shipping_cost']
        # add the item to the order_df with the correct cost, including the shipping cost from the supplier
        order_df = order_df.append({'item': item['item'], 'supplier': supplier['supplier'], 'quantity': order_quantity, 'cost': item['cost'] + total_shipping_costs[supplier['supplier']]}, ignore_index=True)
        break
      # otherwise, buy as much as we can and move on to the next supplier
      else:
        # add the shipping cost for this supplier to the total_shipping_costs dictionary if it's not already there
        if supplier['supplier'] not in total_shipping_costs:
          total_shipping_costs[supplier['supplier']] = supplier['shipping_cost']
        # add the item to the order_df with the correct cost, including the shipping cost from the supplier
        order_df = order_df.append({'item': item['item'], 'supplier': supplier['supplier'], 'quantity': max_quantity, 'cost': item['cost'] + total_shipping_costs[supplier['supplier']]}, ignore_index=True)
        total_quantity += max_quantity
        total_cost += max_quantity * (item['cost'] + total_shipping_costs[supplier['supplier']])

  return order_df
