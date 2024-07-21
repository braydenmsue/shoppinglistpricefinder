import pandas as pd

class AnalysisHandler:
    def __init__(self, df: pd.DataFrame):
        self.data = df
        self.clean_data()

    def clean_data(self):
        # cleaning
        self.data = self.data.dropna(subset=['price', 'amount', 'unit'])
        self.data = self.data.drop_duplicates()
        self.data = self.data.reset_index(drop=True)