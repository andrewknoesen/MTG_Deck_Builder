from pprint import pprint
import pandas as pd


class Order_Builder:
    
    def __init__(self, wanted_cards: pd.DataFrame = pd.DataFrame(), stores_df: pd.DataFrame = pd.DataFrame()) -> None:
        # if (wanted_cards == None or stores_df == None): 
        #     raise Exception("Arguments can not be None")      
        self.wanted_cards: pd.DataFrame = wanted_cards
        self.stores_df: pd.DataFrame = stores_df
        
    def set_stores_df(self, stores_df: pd.DataFrame) -> None:
        self.stores_df: pd.DataFrame = stores_df
        # pprint(self.stores_df)
    def get_stores_def(self) -> pd.DataFrame:
        return self.stores_df

    def set_wanted_df(self, wanted_df: pd.DataFrame) -> None:
        self.wanted_cards: pd.DataFrame = wanted_df
        # pprint(self.wanted_cards)
    def get_wanted_df(self) -> pd.DataFrame:
        return self.wanted_cards

    def compare_cards(self) -> pd.DataFrame:
        summary_store_df: pd.DataFrame = self.stores_df.groupby(['name']).sum(['qty'])
        wanted_copy_df = self.wanted_cards.copy()

        # merge the two dataframes on the name column
        pprint(self.wanted_cards)
        merged_df = pd.merge(wanted_copy_df, summary_store_df, on=['name'], how='left', suffixes=('_df1', '_df2'))
        
        # drop rows where the quantity in the first dataframe is greater than the quantity in the second dataframe
        drop_idx = merged_df.query('qty_df2 > qty_df1').index
        wanted_copy_df.drop(drop_idx, inplace=True)    

        return wanted_copy_df
    
    
    def optimize_order(self) -> pd.DataFrame:
        print(self.stores_df.keys())
        sorted_stores: pd.DataFrame = self.stores_df.sort_values(['name','cost'])
        return sorted_stores
         
