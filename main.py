from ListHandler import ShoppingListHandler
from PriceHandler import PriceHandler
from AnalysisHandler import AnalysisHandler
import pandas as pd


def output_totals(totals: pd.DataFrame):
    for index, row in totals.iterrows():
        output_format = f"{row['name_y']}"
        if row['organic']:
            output_format += " (ORGANIC"
            if row['discount'] > 0:
                output_format += ", ON SALE)"
            else:
                output_format += ")"
        elif row['discount'] > 0:
            output_format += " (ON SALE)"
        output_format += '\n'

        num_orders = int(row['total_amount_ordered'] / row['amount'])
        if num_orders == 1:
            output_format += f" {num_orders} order @ ${row['price']} each "
        else:
            output_format += f" {num_orders} orders @ ${row['price']} each "

        if row['difference'] > 0:
            output_format += f"| {row['difference']}{row['unit_y']} OVER requested amount\n"

        elif row['difference'] < 0:
            output_format += f"| {row['difference']}{row['unit_y']} UNDER requested amount\n"

        else:
            output_format += '\n'

        if row['discount'] > 0:
            output_format += f" TOTAL: ${row['discount']+row['total_price']} - {row['discount']:.2f} " \
                             f"= ${row['total_price']}"
        else:
            output_format += f" TOTAL: ${row['total_price']}"

        print(output_format)
        print()



def main():

    slh = ShoppingListHandler()
    # groceries = slh.create_list()
    # groceries.add_item('cheese', 500, 'g')

    groceries = slh.get_list('untitled.csv')
    prices = PriceHandler(groceries)
    analysis = AnalysisHandler(prices.data, shopping_list=groceries)

    options = analysis.calculate_best_options()
    totals = analysis.get_totals(options)
    output_totals(totals)


    # groceries.remove_item('bread')
    # groceries.display()
    # groceries.save()


    # print("\n--------------------------------------\nDEBUG:\n")
    # print("SLHandler:\n "
    #       "rootdir:", slh.cwd, "\n lists:", slh.lists, "\n num_lists:", slh.num_lists)
    #
    # print("PriceHandler:")
    # print(prices.data)
    #
    # print("AnalysisHandler:")
    # print(analysis.data)


if __name__ == '__main__':
    main()