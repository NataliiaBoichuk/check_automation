import time
import logging as log
from .locators import BasePageLocators


class BasePage:
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def open(self):
        self.browser.get(self.url)
        self.browser.maximize_window()

    def choose_dollar(self):
        log.info("before finding and clicking on the dropdown button of currencies")
        self.browser.find_element(*BasePageLocators.CURRENCY_DROPDOWN).click()
        time.sleep(2)

        log.info("before finding and clicking on the dollar currency button")
        self.browser.find_element(*BasePageLocators.CHOOSE_DOLLAR).click()

    def go_to_search_result(self, enter_word):
        log.info("before finding search field")
        search_field = self.browser.find_element(*BasePageLocators.SEARCH_INPUT)

        log.info(f"before entering a {enter_word} in the search field")
        search_field.send_keys(str(enter_word))

        log.info("before clicking a submit button and redirect to search page")
        self.browser.find_element(*BasePageLocators.SEARCH_INPUT_BTN).click()
        time.sleep(2)

    def should_be_current_currency(self):
        log.info("Before find the currency of the site")
        currency = self.browser.find_element(*BasePageLocators.CURRENCY).text.split(' ')[-1]

        log.info("before find a list of popular products")
        items_prices = self.browser.find_elements(*BasePageLocators.LIST_PRICES_POPULAR_ITEMS)
        for index, el in enumerate(items_prices):
            log.info("before assert the currency of the site and the currency of the product")
            assert currency == el.text.split()[-1], f"The currency of item number {index+1} does not match the current"

