import pandas as pd
import ListHandler as lH


class AnalysisHandler:
    def __init__(self, data: pd.DataFrame, shopping_list: pd.DataFrame):
        self.data = data
        self.shopping_list = shopping_list
        self.clean_data()

    def clean_data(self):
        # cleaning
        self.data = self.data.dropna(subset=['price', 'amount', 'unit'])
        self.data = self.data.drop_duplicates()
        self.data = self.data.reset_index(drop=True)