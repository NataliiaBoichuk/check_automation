import logging as log
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .locators import BasePageLocators


class BasePage:
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url
        self.web_driver_wait = WebDriverWait(self.browser, timeout=15,
                                             ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,))

    def open(self):
        self.browser.get(self.url)
        self.browser.maximize_window()

    def wait_for_element(self, how, what):
        try:
            self.wait_not_stale(how, what)
            element = self.web_driver_wait.until(EC.visibility_of_element_located((how, what)))
        except TimeoutException:
            return f"Failed to find an {what} {how}"
        return element

    def wait_for_all_elements(self, how, what):
        try:
            elements = self.web_driver_wait.until(EC.visibility_of_all_elements_located((how, what)))
        except TimeoutException:
            return f"Failed to find an {what} {how}"
        return elements

    def is_not_stale(self, web_element):
        try:
            web_element.is_enabled()
        except StaleElementReferenceException:
            return False
        return True

    def wait_not_stale(self, how, what):
        elements = self.web_driver_wait.until(EC.visibility_of_all_elements_located((how, what)))
        for el in elements:
            self.web_driver_wait.until(lambda _: self.is_not_stale(el))

    def choose_dollar(self):
        log.info("Looking for and clicking on the dropdown button of currencies")
        self.wait_for_element(*BasePageLocators.CURRENCY_DROPDOWN).click()
        log.info("Looking for and clicking on the dollar button in the dropdown menu")
        self.wait_for_element(*BasePageLocators.CHOOSE_DOLLAR).click()

    def go_to_search_result(self, enter_word):
        log.info("Looking for search fields")
        search_field = self.wait_for_element(*BasePageLocators.SEARCH_INPUT)

        log.info(f"Typing the word {enter_word} in the search bar")
        search_field.send_keys(str(enter_word))

        log.info("Looking and clicking on the search button")
        self.wait_for_element(*BasePageLocators.SEARCH_INPUT_BTN).click()

    def currency_symbol(self):
        """"
        Searches for the current currency symbol on the page
        """
        return self.wait_for_element(*BasePageLocators.CURRENCY).text.split(' ')[-1]

    def should_be_current_currency(self):
        log.info("Looking for the current currency symbol on the site")
        currency = self.currency_symbol()

        log.info("Searching for a list of product prices in the popular products")
        items_prices = self.wait_for_all_elements(*BasePageLocators.LIST_PRICES_POPULAR_ITEMS)

        for index, el in enumerate(items_prices):
            log.info("Comparing the currency of the site and the currency of the products")
            assert currency in el.text, f"The currency of item number {index + 1} is {el.text} " \
                                        f"and does not match the current {currency}"
