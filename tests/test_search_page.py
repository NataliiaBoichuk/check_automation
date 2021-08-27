from check_automation.pages.search_result_page import SearchResults
import allure


class TestSearchResults:
    link = ' http://prestashop-automation.qatestlab.com.ua/ru/'
    search_word = 'dress'

    @allure.description("this test compares the number of items and the counter value on the search page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_total_items(self, browser):
        page = SearchResults(browser, TestSearchResults.link)
        page.open()

        page.go_to_search_result(TestSearchResults.search_word)

        page.should_be_total_items()

    @allure.description("this test checks that the price of all displayed search results is displayed in dollars")
    @allure.severity(allure.severity_level.MINOR)
    def test_currency_is_dollar(self, browser):
        page = SearchResults(browser, TestSearchResults.link)
        page.open()
        page.choose_dollar()

        page.go_to_search_result(TestSearchResults.search_word)

        page.should_be_current_currency()

    @allure.description("this test checks that the items are sorted by price decrease, "
                        "the sorting uses the price without discount.")
    @allure.severity(allure.severity_level.MINOR)
    def test_sorted_desc_price(self, browser):
        page = SearchResults(browser, TestSearchResults.link)
        page.open()
        page.choose_dollar()

        page.go_to_search_result(TestSearchResults.search_word)

        page.should_be_sorted_desc_price()

    @allure.description("this test checks that the discounted items have a percentage discount "
                        "along with the price before and after the discount. ")
    @allure.severity(allure.severity_level.NORMAL)
    def test_discount_items_have_all_elements(self, browser):
        page = SearchResults(browser, TestSearchResults.link)
        page.open()
        page.choose_dollar()

        page.go_to_search_result(TestSearchResults.search_word)

        page.should_be_have_three_el_discount_items()

    @allure.description("this test checks that the price before and after the discount "
                        "is the same as the specified discount amount.")
    @allure.severity(allure.severity_level.MINOR)
    def test_correct_calculate_price_with_discount(self, browser):
        page = SearchResults(browser, TestSearchResults.link)
        page.open()
        page.choose_dollar()

        page.go_to_search_result(TestSearchResults.search_word)

        page.should_be_calculated_correctly_with_discount()
