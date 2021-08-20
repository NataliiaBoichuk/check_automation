import logging as log
from babel.numbers import parse_decimal
from selenium.webdriver.common.by import By
from .base_page import BasePage
from .locators import SearchResultsPageLocators, BasePageLocators


def take_price(el):
    return el.text.split('&')[0][:-2]


class SearchResults(BasePage):

    def sorting_desc_price(self):
        self.wait_for_element(*SearchResultsPageLocators.FILTER_DROPDOWN).click()
        self.wait_for_element(*SearchResultsPageLocators.SORTING_PRICE_DESC).click()

    def should_be_total_items(self):
        log.info("Before find element with count of items")
        assert self.wait_for_element(*SearchResultsPageLocators.ITEMS_NUMBER).text, \
            "The text with the number of items - not found"

        # return "Товаров: x.", where 'x' is count of items
        total_text = self.wait_for_element(*SearchResultsPageLocators.ITEMS_NUMBER).text

        log.info("Before find list of items")
        # return list with all items on page
        list_items = self.wait_for_all_elements(*SearchResultsPageLocators.LIST_DIV_PRICES_ITEMS)

        log.info('Before assert element with count items and exactly amount of items')
        assert len(list_items) == int(total_text.split(' ')[-1][:-1])

    def should_be_current_currency(self):
        log.info("Before find current currency on main page")
        currency = self.wait_for_element(*BasePageLocators.CURRENCY).text.split(' ')[-1]

        log.info("Before find list with prices of items")
        items_prices = self.wait_for_all_elements(*SearchResultsPageLocators.LIST_PRICES_ITEMS)

        for index, el in enumerate(items_prices):
            log.info("Before assert current currency and items currency")
            assert currency in el.text, f"The currency of item number {index + 1} is {el.text} " \
                                        f"and does not match the current {currency}"

    def should_be_sorted_desc_price(self):
        prices = []

        self.sorting_desc_price()
        log.info("Before find list with all prices of items")
        prices_items = self.wait_for_all_elements(*SearchResultsPageLocators.LIST_DIV_PRICES_ITEMS)

        for index in range(len(prices_items)):

            log.info("Before find the number of prices of an item")
            div_prices = self.wait_for_element(By.CSS_SELECTOR,
                                               f'article:nth-child({index + 1}) .product-price-and-shipping')
            prices_item = self.wait_inner_elements(div_prices, By.TAG_NAME, 'span')

            if len(prices_item) > 1:
                log.info("Before find a regular price for a product")
                regular_price = div_prices.find_element(*SearchResultsPageLocators.ITEM_REGULAR_PRICE)
                prices.append(parse_decimal(take_price(regular_price), locale='de'))

            else:
                log.info("Before find a simple price for a product")
                simple_price = div_prices.find_element(*SearchResultsPageLocators.ITEM_PRICE)
                prices.append(parse_decimal(take_price(simple_price), locale='de'))

        for i in range(1, len(prices)):
            assert float(prices[i]) <= float(prices[i - 1]), f"Price item {i + 1} is higher than price item {i}"

    def should_be_have_three_el_discount_items(self):
        log.info("Before find list with all prices of items")
        prices_items = self.wait_for_all_elements(*SearchResultsPageLocators.LIST_DIV_PRICES_ITEMS)

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
        prices_items = self.wait_for_all_elements(*SearchResultsPageLocators.LIST_DIV_PRICES_ITEMS)

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
