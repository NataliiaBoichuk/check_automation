import logging as log
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .locators import BasePageLocators


class BasePage:
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url
        self.web_driver_wait = WebDriverWait(self.browser, timeout=10)

    def open(self):
        self.browser.get(self.url)
        self.browser.maximize_window()

    def wait_for_element(self, how, what, timeout=4):
        try:
            self.wait_not_stale(how, what)
            element = self.web_driver_wait.until(EC.visibility_of_element_located((how, what)))
        except TimeoutException:
            return
        return element

    def wait_for_all_elements(self, how, what, timeout=4):
        try:
            elements = self.web_driver_wait.until(EC.visibility_of_all_elements_located((how, what)))
        except TimeoutException:
            return
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

    def _wait_inner_elements(self, web_element, how, what):
        elements = web_element.find_elements(how, what)
        for el in elements:
            self.web_driver_wait.until(lambda _: self.is_not_stale(el))
        return elements

    def wait_inner_elements(self, web_element, how, what):
        return self.web_driver_wait.until(lambda _: self._wait_inner_elements(web_element, how, what))

    def choose_dollar(self):
        log.info("before finding and clicking on the dropdown button of currencies")
        self.wait_for_element(*BasePageLocators.CURRENCY_DROPDOWN).click()

        log.info("before finding and clicking on the dollar currency button")
        self.wait_for_element(*BasePageLocators.CHOOSE_DOLLAR).click()

    def go_to_search_result(self, enter_word):
        log.info("before finding search field")
        search_field = self.wait_for_element(*BasePageLocators.SEARCH_INPUT)

        log.info(f"before entering a {enter_word} in the search field")
        search_field.send_keys(str(enter_word))

        log.info("before clicking a submit button and redirect to search page")
        self.wait_for_element(*BasePageLocators.SEARCH_INPUT_BTN).click()

    def should_be_current_currency(self):
        log.info("Before find the currency of the site")
        currency = self.wait_for_element(*BasePageLocators.CURRENCY).text.split(' ')[-1]

        log.info("before find a list of popular products")
        items_prices = self.wait_for_all_elements(*BasePageLocators.LIST_PRICES_POPULAR_ITEMS)

        for index, el in enumerate(items_prices):
            log.info("before assert the currency of the site and the currency of the product")
            assert currency in el.text, f"The currency of item number {index + 1} is {el.text} " \
                                        f"and does not match the current {currency}"
