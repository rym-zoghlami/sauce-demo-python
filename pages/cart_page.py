from selenium.webdriver.common.by import By
from .base_page import BasePage

class CartPage(BasePage):
    # Locators
    CONTINUE_SHOPPING_BUTTON = (By.XPATH, "//button[contains(text(), 'Continue Shopping')]")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    QUANTITY = (By.CLASS_NAME, "cart_quantity")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button.cart_button")
    #CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_TITLE = (By.CLASS_NAME, "title")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
    
    def get_cart_items(self):
        return self.find_elements(self.CART_ITEMS)
    
    def get_item_names(self):
        items = self.find_elements(self.ITEM_NAME)
        return [item.text for item in items]
    
    def get_item_prices(self):
        items = self.find_elements(self.ITEM_PRICE)
        return [float(item.text.replace('$', '')) for item in items]
    
    def remove_item(self, item_index=0):
        remove_buttons = self.find_elements(self.REMOVE_BUTTON)
        if item_index < len(remove_buttons):
            remove_buttons[item_index].click()
        return self
    
    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        from .inventory_page import InventoryPage
        return InventoryPage(self.driver)
    
    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        from .checkout_page import CheckoutPage
        return CheckoutPage(self.driver)
    
    def is_empty(self):
        return len(self.get_cart_items()) == 0
    
    def get_cart_title(self):
        return self.get_text(self.CART_TITLE)
    
    def is_displayed(self, locator):
        return super().is_displayed(locator)