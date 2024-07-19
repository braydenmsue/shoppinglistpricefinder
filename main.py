import listHandler as lh
import priceHandler as ph


def main():

    slh = lh.ShoppingListHandler()
    pf = ph.PriceFinder('untitled.csv')



    # groceries = slh.get_list('untitled.csv')
    # groceries.add_item('ham', 300)
    # groceries.remove_item('bread')
    # groceries.display()
    # groceries.save()


    print("\n--------------------------------------\nDEBUG:\n")
    print("SLHandler:\n "
          "rootdir:", slh.cwd, "\n lists:", slh.lists, "\n num_lists:", slh.num_lists)

    print("priceHandler:\n "
          "data:", pf.display())


if __name__ == '__main__':
    main()