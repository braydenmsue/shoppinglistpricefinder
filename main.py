import listHandler as lh
import priceHandler as ph


def main():

    slh = lh.ShoppingListHandler()

    pf = ph.PriceFinder('untitled.csv')
    data = pf.gather_items_data()
    print(data)


    # groceries = slh.get_list('untitled.csv')
    # groceries.add_item('ham', 300)
    # groceries.remove_item('bread')
    # groceries.display()
    # groceries.save()


    print("\n--------------------------------------\nDEBUG:\n")
    print("SLHandler:\n "
          "rootdir:", slh.cwd, "\n lists:", slh.lists, "\n num_lists:", slh.num_lists)


if __name__ == '__main__':
    main()