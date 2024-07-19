import listHandler as lh
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import pandas as pd
import re
import time

from selenium.webdriver.chrome.options import Options   # for testing

WEBSITE = 'https://sameday.costco.ca/store/costco-canada/storefront'


def get_driver():
    chromedriver_autoinstaller.install()

    # for testing; keeps window open after script finishes
    chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(WEBSITE)
    driver.maximize_window()
    return driver


# take list of 3 spans containing price and returns float
#   e.g. [<span>$</span>, <span>5</span>, <span>25</span> -> '5.25'
# OR a 1-string list like ['$12.34'] and returns float --> 12.34
def format_price(price_chars: list):
    if len(price_chars) == 1:
        return float(price_chars[0][1:])
    else:
        return float(price_chars[1].text + '.' + price_chars[2].text)

def to_grams(amount: str):
    # Regex patterns to match 'A x B kg' or 'A x B g'
    patterns = {
        'kg': re.compile(r'(\d+\.?\d*)\s*(?:x\s*(\d+\.?\d*))?\s*kg', re.IGNORECASE),
        'g': re.compile(r'(\d+\.?\d*)\s*(?:x\s*(\d+\.?\d*))?\s*g', re.IGNORECASE),
        'lb': re.compile(r'(\d+\.?\d*)\s*(?:x\s*(\d+\.?\d*))?\s*lb', re.IGNORECASE),
        # TODO: add volume units
    }

    # Check and convert the input string
    for unit, pattern in patterns.items():
        match = pattern.match(amount)
        if match:
            quantity = float(match.group(1)) if match.group(1) else 1
            value = float(match.group(2)) if match.group(2) else 1

            if unit == 'kg':
                return quantity * value * 1000
            elif unit == 'g':
                return quantity * value
            elif unit == 'lb':
                return quantity * value * 453.592


class PriceFinder:
    def __init__(self, filename: str):
        self.slh = lh.ShoppingListHandler()
        self.list = self.slh.get_list(filename)
        self.data = self.gather_items_data()

    def display(self):
        print(self.data)

    def gather_items_data(self):
        driver = get_driver()
        search_bar_xpath = '//input[@id="search-bar-input"]'
        data = []

        for index, row in self.list.data.iterrows():
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, search_bar_xpath)))
            search_bar = driver.find_element(By.XPATH, search_bar_xpath)

            search_bar.send_keys(Keys.CONTROL + "a")
            search_bar.send_keys(Keys.DELETE)

            search_bar.send_keys(row['name'])
            search_bar.send_keys(Keys.RETURN)

            list_container_xpath = '//ul[@class="e-egal4z"]'
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, list_container_xpath)))
            list_containers = driver.find_elements(By.XPATH, list_container_xpath)

            df = pd.DataFrame(columns=['name', 'price', 'amount'])

            for item_list in list_containers:
                items_xpath = './/li//div[@class="e-13udsys"]'
                items = item_list.find_elements(By.XPATH, items_xpath)
                for item in items:
                    name_xpath = './/div[@class="e-i41pyq"]//h2[@class="e-147kl2c"]'
                    price_div_xpath = './/span[@class="e-1ip314g"]'
                    amount_xpath = './/div[@class="e-zjik7"]//div'
                    full_price_xpath = './/p[@class="e-vn9fl5"]//span[@class="e-azp9o7"]'   # for items on sale

                    name = item.find_element(By.XPATH, name_xpath).text
                    #TODO: add synonyms for each item e.g. bread -> bun(s), sourdough, baguette
                    if row['name'].lower() in name.lower():
                        # print(item.find_element(By.XPATH, name_xpath).text)

                        price_div = item.find_element(By.XPATH, price_div_xpath)
                        price_digits = price_div.find_elements(By.XPATH, './/span')
                        price = format_price(price_digits)

                        try:
                            full_price_digits = item.find_element(By.XPATH, full_price_xpath).text
                            full_price = format_price([full_price_digits])
                        except NoSuchElementException:
                            full_price = price

                        try:
                            amount_str = item.find_element(By.XPATH, amount_xpath).text
                            amount = to_grams(amount_str)
                        except NoSuchElementException:
                            amount = None

                        discount = full_price - price

                        record = [name, price, amount, discount]
                        data.append(record)

            result = pd.DataFrame(data, columns=['name', 'price', 'amount', 'discount'])

        return result
