import pandas as pd
import numpy as np
import ListHandler as lH


class AnalysisHandler:
    def __init__(self, data: pd.DataFrame, shopping_list: lH.ShoppingList):
        self.data = data
        self.shopping_list = shopping_list
        self.clean_data()
        self.price_per_unit()

    def clean_data(self):
        self.data = self.data.dropna(subset=['price', 'amount', 'unit'])
        self.data = self.data.drop_duplicates()
        self.data = self.data.reset_index(drop=True)

    def price_per_unit(self):
        self.data['price_per_unit'] = self.data['price'] / self.data['amount']
        return self.data

    def get_totals(self, options: pd.DataFrame):
        self.shopping_list.convert_units()
        options = options.reset_index(drop=True)
        totals = pd.merge(self.shopping_list.data, options, left_on='name', right_on='search_term', how='left')

        totals['orders_needed'] = np.ceil(totals['required_amount'] / totals['amount'])
        totals['total_amount_ordered'] = totals['orders_needed'] * totals['amount']
        totals['difference'] = totals['total_amount_ordered'] - totals['required_amount']
        totals['total_price'] = totals['orders_needed'] * totals['price']

        return totals

    def calculate_best_options(self, priority: str = 'price'):
        """
        TODO: more than just price per unit, need to check if the amount in a package lines up well with user's needs
        increase nlargest/smallest to 3-5 for more options, if there's an option where the amount is less than the
        difference, then add it to totals if adding that is cheaper than another order of the cheapest item
        """

        df = self.data
        if priority.lower == "price":
            df = df.groupby('search_term').apply(lambda x: x.nsmallest(1, 'price_per_unit'))

        elif priority.lower == "discount":
            df = df.groupby('search_term').apply(lambda x: x.nlargest(1, 'discount'))

        elif priority.lower == "organic":
            df = df[df['organic'] is True]  # Filter for organic products
            df = df.groupby('search_term').apply(lambda x: x.nsmallest(1, 'price_per_unit'))    # PPU of organic

        # otherwise, priority is the lowest price per unit
        else:
            df = df.groupby('search_term').apply(lambda x: x.nsmallest(1, 'price_per_unit'))

        return df
