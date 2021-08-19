import pytest
from check_automation.pages.base_page import BasePage


def test_currency_should_be_current(browser):
    link = 'http://prestashop-automation.qatestlab.com.ua/ru/'
    page = BasePage(browser, link)
    page.open()
    page.should_be_current_currency()
