from ListHandler import ShoppingListHandler
from PriceHandler import PriceHandler
from AnalysisHandler import AnalysisHandler


def main():

    slh = ShoppingListHandler()
    prices = PriceHandler('untitled.csv')
    analysis = AnalysisHandler(prices.data)



    # groceries = slh.get_list('untitled.csv')
    # groceries.add_item('ham', 300)
    # groceries.remove_item('bread')
    # groceries.display()
    # groceries.save()


    print("\n--------------------------------------\nDEBUG:\n")
    print("SLHandler:\n "
          "rootdir:", slh.cwd, "\n lists:", slh.lists, "\n num_lists:", slh.num_lists)

    print("PriceHandler:\n "
          "data:", prices.data)

    print("AnalysisHandler:\n "
          "data:", analysis.data)


if __name__ == '__main__':
    main()