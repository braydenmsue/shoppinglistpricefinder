import pandas as pd
import os

# class Item:
#     def __init__(self, i_id: int, name: str, amount: float):
#         self.i_id = i_id
#         self.name = name
#         self.amount = amount
#
#     def __str__(self):
#         return f'{self.name}: {self.amount}'


def convert_row(row):
    if row['unit'] == 'kg':
        row['required_amount'] *= 1000
        row['unit'] = 'g'
    elif row['unit'] == 'g':
        pass
    elif row['unit'] == 'lb':
        row['required_amount'] *= 453.592
        row['unit'] = 'g'
    elif row['unit'] == 'oz':
        row['required_amount'] *= 28.3495
        row['unit'] = 'g'
    elif row['unit'] == 'ml':
        pass
    elif row['unit'] == 'l':
        row['required_amount'] *= 1000
        row['unit'] = 'ml'

    return row


class ShoppingList:
    def __init__(self, filename: str, data: pd.DataFrame):
        self.filename = filename
        self.data = data

    def convert_units(self):
        self.data = self.data.apply(convert_row, axis=1)

    def add_item(self, name: str, amount: float, unit: str):
        if type(amount) != int and type(amount) != float:
            return None

        if name in self.data['name'].values:
            self.data.loc[self.data['name'] == name, 'required_amount'] += amount
        else:
            record = {'name': name, 'required_amount': amount, 'unit': unit}
            self.data = self.data._append(record, ignore_index=True)
        return 1

    def remove_item(self, name: str):
        if name in self.data['name'].values:
            self.data = self.data[self.data['name'] != name]
            return 1
        return None

    def num_items(self):
        return len(self.data)

    def display(self):
        print(self.data)

    def save(self):
        self.data.to_csv(os.path.join(os.getcwd(), 'lists', self.filename), index=False)


class ShoppingListHandler:
    def __init__(self):
        self.cwd = os.getcwd()
        self.lists = self.get_filenames()
        self.num_lists = self.get_num_lists()

    def get_filenames(self):
        path = os.path.join(self.cwd, 'lists')
        result = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return result

    def get_num_lists(self):
        return len(self.lists)

    def create_list(self, filename: str = 'untitled.csv'):

        while filename in self.lists:
            if filename[-5].isdigit():
                original_name = filename[:-6]
                filename = f'{original_name}_{int(filename[-5]) + 1}.csv'
            else:
                original_name = filename[:-4]
                filename = f'{original_name}_1.csv'

        path = os.path.join(self.cwd, 'lists', filename)
        self.lists.append(filename)
        self.num_lists = self.get_num_lists()

        data = pd.DataFrame(columns=['name', 'required_amount', 'unit'])
        data.to_csv(path, index=False)

    def get_list(self, filename: str):
        if filename in self.lists:
            data = pd.read_csv(os.path.join(self.cwd, 'lists', filename))
        else:
            print("ERROR: List not found.")
            return -1

        return ShoppingList(filename, data)
