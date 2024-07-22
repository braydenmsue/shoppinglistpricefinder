from ListHandler import ShoppingListHandler
from PriceHandler import PriceHandler
from AnalysisHandler import AnalysisHandler


def main():

    slh = ShoppingListHandler()
    # groceries = slh.create_list()
    groceries = slh.get_list('untitled.csv')
    # groceries.add_item('cheese', 500, 'g')

    prices = PriceHandler(groceries)
    analysis = AnalysisHandler(prices.data, shopping_list=groceries.data)


    # groceries.remove_item('bread')
    # groceries.display()
    # groceries.save()


    print("\n--------------------------------------\nDEBUG:\n")
    print("SLHandler:\n "
          "rootdir:", slh.cwd, "\n lists:", slh.lists, "\n num_lists:", slh.num_lists)

    print("PriceHandler:")
    print(prices.data)

    print("AnalysisHandler:")
    print(analysis.data)


if __name__ == '__main__':
    main()