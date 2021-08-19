import time
import pytest
from check_automation.pages.search_result_page import SearchResults


class TestSearchResults:
    link = ' http://prestashop-automation.qatestlab.com.ua/ru/'
    search_word = 'dress'

    def test_total_items(self, browser):
        page = SearchResults(browser, TestSearchResults.link)
        page.open()

        page.go_to_search_result(TestSearchResults.search_word)
        time.sleep(1)

        page.should_be_total_items()

    def test_currency_is_dollar(self, browser):
        page = SearchResults(browser, TestSearchResults.link)
        page.open()
        page.choose_dollar()

        page.go_to_search_result(TestSearchResults.search_word)
        time.sleep(1)

        page.should_be_current_currency()

    def test_sorted_desc_price(self, browser):
        page = SearchResults(browser, TestSearchResults.link)
        page.open()
        page.choose_dollar()

        page.go_to_search_result(TestSearchResults.search_word)
        page.sorting_desc_price()

        page.should_be_sorted_desc_price()

    def test_discount_items_have_all_elements(self, browser):
        page = SearchResults(browser, TestSearchResults.link)
        page.open()
        page.choose_dollar()

        page.go_to_search_result(TestSearchResults.search_word)
        time.sleep(1)

        page.should_be_have_three_el_discount_items()

    def test_correct_calculate_price_with_discount(self, browser):
        page = SearchResults(browser, TestSearchResults.link)
        page.open()
        page.choose_dollar()

        page.go_to_search_result(TestSearchResults.search_word)
        time.sleep(1)

        page.should_be_calculated_correctly_with_discount()
