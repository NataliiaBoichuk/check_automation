import pytest
import logging as log
from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener


log.basicConfig(filename='test.log',
                format='%(asctime)s: %(levelname)s: %(message)s',
                level=log.DEBUG)


class MyListener(AbstractEventListener):
    def before_navigate_to(self, url, driver):
        log.info(f"Before navigate to {url}")

    def after_navigate_to(self, url, driver):
        log.info(f"After navigate to {url}")

    def before_find(self, by, value, driver):
        log.info(f"Before find {value} by {by}")

    def after_find(self, by, value, driver):
        log.info(f"After find {value} by {by}")

    def before_click(self, element, driver):
        log.info(f"Before click {element}")

    def after_click(self, element, driver):
        log.info(f"After click {element}")

    def before_quit(self, driver):
        log.info(f"Quitting the browser with url: {driver.current_url}")

    def after_quit(self, driver):
        log.info(f"Quit the browser. Have a nice day :)")

    def on_exception(self, exception, driver):
        log.exception(f"{exception}")


@pytest.fixture
def browser(request):
    driver = webdriver.Chrome()
    browser = EventFiringWebDriver(driver, MyListener())
    yield browser
    browser.quit()
