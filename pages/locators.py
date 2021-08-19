from selenium.webdriver.common.by import By


class BasePageLocators:
    POPULAR_ITEMS = (By.CLASS_NAME, 'products')
    CURRENCY = (By.CLASS_NAME, '_gray-darker')
    CURRENCY_DROPDOWN = (By.CSS_SELECTOR, 'div.currency-selector a[data-target="#"]')
    CHOOSE_DOLLAR = (By.XPATH, '//a[text()="USD $"]')
    LIST_PRICES_POPULAR_ITEMS = (By.CLASS_NAME, 'price')
    SEARCH_INPUT = (By.NAME, 's')
    SEARCH_INPUT_BTN = (By.CSS_SELECTOR, 'button[type="submit"]')


class SearchResultsPageLocators:
    ITEMS_NUMBER = (By.CSS_SELECTOR, 'div.total-products p')
    LIST_PRICES_ITEMS = (By.CSS_SELECTOR, '.product-description .price')
    LIST_DIV_PRICES_ITEMS = (By.CLASS_NAME, 'product-price-and-shipping')
    FILTER_DROPDOWN = (By.CLASS_NAME, 'select-title')
    SORTING_PRICE_DESC = (By.XPATH, '//a[contains(@href, "price.desc")]')
    ITEM_REGULAR_PRICE = (By.CLASS_NAME, 'regular-price')
    ITEM_DISCOUNT_PERCENTAGE = (By.CLASS_NAME, 'discount-percentage')
    ITEM_PRICE = (By.CLASS_NAME, 'price')
