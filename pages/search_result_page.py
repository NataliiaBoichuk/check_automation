import logging as log
import time
from babel.numbers import parse_decimal
from .base_page import BasePage
from .locators import SearchResultsPageLocators, BasePageLocators


class SearchResults(BasePage):
    def sorting_desc_price(self):
        self.browser.find_element(*SearchResultsPageLocators.FILTER_DROPDOWN).click()
        self.browser.find_element(*SearchResultsPageLocators.SORTING_PRICE_DESC).click()
        time.sleep(2)

    def should_be_total_items(self):
        time.sleep(2)
        log.info("Before find element with count of items")
        assert self.browser.find_element(*SearchResultsPageLocators.ITEMS_NUMBER).text, \
            "The text with the number of items - not found"
        total_text = self.browser.find_element(*SearchResultsPageLocators.ITEMS_NUMBER).text
        log.info("Before find list of items")
        list_items = self.browser.find_elements(*SearchResultsPageLocators.LIST_DIV_PRICES_ITEMS)
        log.info('Before assert element with count items and exactly amount of items')
        assert len(list_items) == int(total_text.split(' ')[-1][:-1])

    def should_be_current_currency(self):
        log.info("Before find current currency on main page")
        currency = self.browser.find_element(*BasePageLocators.CURRENCY).text.split(' ')[-1]
        log.info("Before find list with prices of items")
        items_prices = self.browser.find_elements(*SearchResultsPageLocators.LIST_PRICES_ITEMS)
        for index, el in enumerate(items_prices):
            log.info("Before assert current currency and items currency")
            assert currency == el.text.split()[-1], \
                f"The currency of item number {index + 1} is {el.text.split()[-1]} " \
                f"and does not match the current {currency}"

    def should_be_sorted_desc_price(self):
        prices = []
        log.info("Before find list with all prices of items")
        prices_items = self.browser.find_elements(*SearchResultsPageLocators.LIST_DIV_PRICES_ITEMS)

        for el in prices_items:
            log.info("Before find the number of prices of an item")
            prices_item = el.find_elements_by_tag_name('span')
            if len(prices_item) == 1:
                prices.append(parse_decimal(prices_item[0].text.split('&')[0][:-2], locale='de'))
            else:
                log.info("Before find a regular price for a product")
                regular_price = el.find_element(*SearchResultsPageLocators.ITEM_REGULAR_PRICE).text
                prices.append(parse_decimal(regular_price.split('&')[0][:-2], locale='de'))

        for index in range(1, len(prices)):
            if prices[index] > prices[index-1]:
                return False
        return True

    def should_be_have_three_el_discount_items(self):
        log.info("Before find list with all prices of items")
        prices_items = self.browser.find_elements(*SearchResultsPageLocators.LIST_DIV_PRICES_ITEMS)

        for el in prices_items:
            log.info("Before find the number of prices of an item")
            prices_item = el.find_elements_by_tag_name('span')

            if len(prices_item) > 1:
                log.info("Before assert a regular price is displayed on the item")
                assert el.find_element(*SearchResultsPageLocators.ITEM_REGULAR_PRICE).is_displayed(), \
                    'The product has no price without a discount'
                log.info("Before assert a price is displayed on the item")
                assert el.find_element(*SearchResultsPageLocators.ITEM_DISCOUNT_PERCENTAGE).is_displayed(), \
                    'The product has no discount'
                log.info("Before assert a discount is displayed on the item")
                assert el.find_element(*SearchResultsPageLocators.ITEM_PRICE).is_displayed(), \
                    'The product has no price'

    def should_be_calculated_correctly_with_discount(self):
        log.info("Before find list with all prices of items")
        prices_items = self.browser.find_elements(*SearchResultsPageLocators.LIST_DIV_PRICES_ITEMS)

        for el in prices_items:
            log.info("Before find the number of prices of an item")
            prices_item = el.find_elements_by_tag_name('span')

            if len(prices_item) > 1:
                log.info("Before finding the value of the regular price of a product")
                regular_price = parse_decimal(
                    el.find_element(*SearchResultsPageLocators.ITEM_REGULAR_PRICE).text.split('&')[0][:-2], locale='de')

                log.info("Before finding the value of the price of a product")
                current_price = parse_decimal(
                    el.find_element(*SearchResultsPageLocators.ITEM_PRICE).text.split('&')[0][:-2], locale='de')

                log.info("Before finding the value of a discount of a product")
                discount = float(el.find_element(*SearchResultsPageLocators.ITEM_DISCOUNT_PERCENTAGE).text[1:-1])

                log.info("Before assert the value of the price is correct")
                assert float("{:.2f}".format(current_price)) == round(float(regular_price) * (100 - discount) / 100, 2), \
                    f"The price is not correct in the item with regular price -{regular_price} and discount - {discount}"
