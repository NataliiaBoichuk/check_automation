import allure
from check_automation.pages.base_page import BasePage


@allure.description("this test checks if the price of items in the 'Popular Items' section "
                    "matches the currency set in the header of the site")
@allure.severity(allure.severity_level.MINOR)
def test_currency_should_be_current(browser):
    link = 'http://prestashop-automation.qatestlab.com.ua/ru/'
    page = BasePage(browser, link)
    page.open()
    page.should_be_current_currency()
