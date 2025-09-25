from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutPage(BasePage):
    # Locators
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def enter_first_name(self, first_name):
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        return self
    
    def enter_last_name(self, last_name):
        self.type_text(self.LAST_NAME_INPUT, last_name)
        return self
    
    def enter_postal_code(self, postal_code):
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        return self
    
    def continue_to_overview(self):
        self.click(self.CONTINUE_BUTTON)
        return self
    
    def cancel_checkout(self):
        self.click(self.CANCEL_BUTTON)
        from pages.cart_page import CartPage
        return CartPage(self.driver)
    
    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)