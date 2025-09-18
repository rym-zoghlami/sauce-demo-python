from selenium.webdriver.common.by import By
from .base_page import BasePage

class InventoryPage(BasePage):
    # Locators
    PRODUCTS_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button.btn_primary.btn_inventory")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button.btn_secondary.btn_small.btn_inventory")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
    
    def get_products_title(self):
        return self.get_text(self.PRODUCTS_TITLE)
    
    def get_inventory_items(self):
        return self.find_elements(self.INVENTORY_ITEMS)
    
    def get_item_names(self):
        items = self.find_elements(self.ITEM_NAME)
        return [item.text for item in items]
    
    def get_item_prices(self):
        items = self.find_elements(self.ITEM_PRICE)
        return [float(item.text.replace('$', '')) for item in items]
    
    def add_item_to_cart(self, item_index=0):
        add_buttons = self.find_elements(self.ADD_TO_CART_BUTTON)
        if item_index < len(add_buttons):
            add_buttons[item_index].click()
        return self
    
    def remove_item_from_cart(self, item_index=0):
        """Retire un article du panier"""
        # Sur Sauce Demo, le bouton change de texte après l'ajout
        # Essayez d'abord avec le sélecteur Remove
        try:
            remove_buttons = self.find_elements((By.XPATH, "//button[text()='Remove']"))
            if item_index < len(remove_buttons):
                remove_buttons[item_index].click()
        except:
            # Si pas de bouton Remove, recliquer sur le bouton Add
            add_buttons = self.find_elements(self.ADD_TO_CART_BUTTON)
            if item_index < len(add_buttons):
                add_buttons[item_index].click()
        return self
    
    def go_to_cart(self):
        self.click(self.CART_ICON)
        from .cart_page import CartPage
        return CartPage(self.driver)
    
    def sort_products(self, sort_option="az"):
        self.click(self.SORT_DROPDOWN)
        option_locator = (By.CSS_SELECTOR, f"option[value='{sort_option}']")
        self.click(option_locator)
        return self
    
    def get_cart_count(self):
        cart_icon = self.find_element(self.CART_ICON)
        text = cart_icon.text
        return int(text) if text else 0
    
    def is_displayed(self, locator):
        return super().is_displayed(locator)