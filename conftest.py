import pytest
import logging as log
from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


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


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")


@pytest.fixture(autouse=True)
def browser(request):
    browser_name = request.config.getoption('browser')

    if browser_name == 'firefox':
        driver = webdriver.Firefox(executable_path=GeckoDriverManager(version='91.0.2').install())
    else:
        driver = webdriver.Chrome(executable_path='//c/chromedriver')

    browser = EventFiringWebDriver(driver, MyListener())

    yield browser
    browser.quit()
