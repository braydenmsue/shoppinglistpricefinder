import listHandler as lh

def main():

    #   https://sameday.costco.ca/store/costco-canada/storefront
    slh = lh.ShoppingListHandler()
    # slh.create_list()
    # slh.create_list()
    # slh.create_list()

    groceries = slh.get_list('untitled')
    groceries.add_item('bread', 500)
    # groceries.remove_item('bread')
    groceries.display()
    groceries.save()


    # DEBUG
    print("SLHandler----------------------------\n "
          "rootdir:", slh.cwd, "\n lists:", slh.lists, "\n num_lists:", slh.num_lists)


if __name__ == '__main__':
    main()