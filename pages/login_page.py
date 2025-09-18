from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
    
    def open(self):
        self.driver.get("https://www.saucedemo.com/")
        return self
    
    def enter_username(self, username):
        self.type_text(self.USERNAME_INPUT, username)
        return self
    
    def enter_password(self, password):
        self.type_text(self.PASSWORD_INPUT, password)
        return self
    
    def click_login(self):
        self.click(self.LOGIN_BUTTON)
        from .inventory_page import InventoryPage
        return InventoryPage(self.driver)
    
    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        return self.click_login()
    
    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_message_displayed(self):
        return self.is_displayed(self.ERROR_MESSAGE)