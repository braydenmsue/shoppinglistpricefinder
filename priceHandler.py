import listHandler as lh
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

WEBSITE = 'https://sameday.costco.ca/store/costco-canada/storefront'


def get_driver(self):
    chromedriver_autoinstaller.install()

    driver = webdriver.Chrome()
    driver.get(WEBSITE)
    driver.maximize_window()
    return driver


class PriceFinder:
    def __init__(self, filename: str):
        self.slh = lh.ShoppingListHandler()
        self.list = self.slh.get_list(filename)
        self.items = {}

    def gather_items_data(self):
        driver = get_driver()
        search_bar_xpath = '//input[@id="search-bar-input"]'

        for index, row in self.list.data.iterrows():
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, search_bar_xpath)))
            search_bar = driver.find_element(By.XPATH, search_bar_xpath)

            search_bar.clear()
            search_bar.send_keys(row['name'])
            search_bar.send_keys(Keys.RETURN)

            # TODO: determine blocks of page to scrape (under 'Results for "____"' header)





    def close_driver(self):
        self.driver.quit()

