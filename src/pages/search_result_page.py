import logging as log
from babel.numbers import parse_decimal
from selenium.webdriver.common.by import By
from .base_page import BasePage
from .locators import SearchResultsPageLocators


def give_price(el, locale='de'):
    """"
    return price of product
    """
    return float(parse_decimal(el.text.split('&')[0][:-2], locale=locale))


class SearchResults(BasePage):

    def sorting_desc_price(self):
        log.info("Looking for and clicking on the dropdown button of filter")
        self.wait_for_element(*SearchResultsPageLocators.FILTER_DROPDOWN).click()
        log.info("Looking for and clicking on the sort by decrease in price button in the dropdown menu")
        self.wait_for_element(*SearchResultsPageLocators.SORTING_PRICE_DESC).click()

    def should_be_total_items(self):
        log.info("Checking the availability of text by the number of search results")
        assert self.wait_for_element(*SearchResultsPageLocators.ITEMS_NUMBER).text, \
            "The text with the number of search results not found"

        # return "Товаров: x.", where 'x' is count of items
        total_text = self.wait_for_element(*SearchResultsPageLocators.ITEMS_NUMBER).text

        # return list with all items on page
        log.info("Searching for the number of items in the search results")
        list_items = self.wait_for_all_elements(*SearchResultsPageLocators.LIST_DIV_PRICES_ITEMS)

        # find the number of items
        count = len(list_items)

        log.info('Comparing the number of items and the counter value on the search results page')
        assert str(count) in total_text, f"The number of items and the counter value " \
                                         f"on the search results page do not match"

    def should_be_current_currency(self):
        log.info("Defining the current currency")
        currency = self.currency_symbol()

        log.info("Searching for a list of product prices in the search results")
        items_prices = self.wait_for_all_elements(*SearchResultsPageLocators.LIST_PRICES_ITEMS)

        for index, el in enumerate(items_prices):
            log.info("Comparison of the current currency with the currency in prices")
            assert currency in el.text, f"The currency of item number {index + 1} is {el.text} " \
                                        f"and does not match the current {currency}"

    def should_be_sorted_desc_price(self):
        # list with prices for comparison
        prices = []

        self.sorting_desc_price()

        # return a list of web elements that include a list of prices for the product
        log.info("Searching for a list of prices for item")
        prices_items = self.wait_for_all_elements(*SearchResultsPageLocators.LIST_DIV_PRICES_ITEMS)

        for index in range(len(prices_items)):

            log.info("Looking for a web element with product prices ")
            div_prices = self.wait_for_element(By.CSS_SELECTOR,
                                                   f'article:nth-child({index + 1}) .product-price-and-shipping')

            log.info("Looking for the number of prices for item")
            prices_item = self.wait_inner_elements(div_prices, By.TAG_NAME, 'span')

            if len(prices_item) > 1:
                log.info("Looking for the regular price(without discount) of the product")
                regular_price = div_prices.find_element(*SearchResultsPageLocators.ITEM_REGULAR_PRICE)
                prices.append(give_price(regular_price))

            else:
                log.info("Looking for the simple price of the product")
                simple_price = div_prices.find_element(*SearchResultsPageLocators.ITEM_PRICE)
                prices.append(give_price(simple_price))

        for i in range(1, len(prices)):
            assert prices[i] <= prices[i - 1], f"The price of the {i + 1} item is higher than price of the {i} item"

    def should_be_have_three_el_discount_items(self):
        log.info("Searching for a list of prices for item")
        prices_items = self.wait_for_all_elements(*SearchResultsPageLocators.LIST_DIV_PRICES_ITEMS)

        for el in prices_items:
            log.info("Looking for the number of prices for item")
            prices_item = el.find_elements_by_tag_name('span')

            if len(prices_item) > 1:
                log.info("Check if the price is displayed without a discount")
                assert el.find_element(*SearchResultsPageLocators.ITEM_REGULAR_PRICE).is_displayed(), \
                    'The product has no price without a discount'

                log.info("Check whether the product discount is displayed")
                assert el.find_element(*SearchResultsPageLocators.ITEM_DISCOUNT_PERCENTAGE).is_displayed(), \
                    'The product has no discount'

                log.info("Check if the price is displayed with a discount")
                assert el.find_element(*SearchResultsPageLocators.ITEM_PRICE).is_displayed(), \
                    'The product has no price with a discount'

    def should_be_calculated_correctly_with_discount(self):
        log.info("Searching for a list of prices for item")
        prices_items = self.wait_for_all_elements(*SearchResultsPageLocators.LIST_DIV_PRICES_ITEMS)

        for el in prices_items:
            log.info("Looking for the number of prices for item")
            prices_item = el.find_elements_by_tag_name('span')

            if len(prices_item) > 1:
                log.info("Looking for the regular price(without discount) of the product")
                regular_price = el.find_element(*SearchResultsPageLocators.ITEM_REGULAR_PRICE)

                log.info("Looking for the simple price of the product")
                current_price = el.find_element(*SearchResultsPageLocators.ITEM_PRICE)

                log.info("Looking for the discount of the product")
                discount = float(el.find_element(*SearchResultsPageLocators.ITEM_DISCOUNT_PERCENTAGE).text[1:-1])

                log.info("Checking that the discounted price is calculated correctly")
                assert give_price(current_price) == round(give_price(regular_price) * (100 - discount) / 100, 2), \
                    f"The price : {give_price(current_price)} is not correct in the item " \
                    f"with regular price : {give_price(regular_price)} and discount : {discount}"
