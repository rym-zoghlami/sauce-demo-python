from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class CartPage(BasePage):
    # Locators CORRIGÉS
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    REMOVE_BUTTON = (By.XPATH, "//button[contains(@id, 'remove')]")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_TITLE = (By.CLASS_NAME, "title")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_cart_items(self):
        """Get all cart items with explicit wait"""
        time.sleep(2)  # Attendre le chargement
        try:
            items = self.find_elements(self.CART_ITEMS)
            print(f"📦 Articles dans le panier: {len(items)}")
            return items
        except:
            print("❌ Aucun article trouvé dans le panier")
            return []
    
    def get_item_names(self):
        items = self.find_elements(self.ITEM_NAME)
        names = [item.text for item in items]
        print(f"📝 Noms des articles: {names}")
        return names
    
    def get_item_prices(self):
        items = self.find_elements(self.ITEM_PRICE)
        prices = [float(item.text.replace('$', '')) for item in items]
        print(f"💰 Prix des articles: {prices}")
        return prices
    
    def remove_item(self, item_index=0):
        remove_buttons = self.find_elements(self.REMOVE_BUTTON)
        if item_index < len(remove_buttons):
            self.driver.execute_script("arguments[0].click();", remove_buttons[item_index])
            print(f"✅ Article {item_index} supprimé")
            time.sleep(2)
        return self
    
    def continue_shopping(self):
        """Continue shopping and return to inventory"""
        print("🔄 Retour à l'inventaire...")
        
        button = self.find_element(self.CONTINUE_SHOPPING_BUTTON)
        self.driver.execute_script("arguments[0].click();", button)
        
        # Attendre la navigation
        time.sleep(2)
        
        # Vérifier l'URL
        current_url = self.driver.current_url
        print(f"URL après retour: {current_url}")
        
        from pages.inventory_page import InventoryPage
        return InventoryPage(self.driver)
    
    def checkout(self):
        """Start checkout process"""
        print("💰 Démarrage du checkout...")
        
        button = self.find_element(self.CHECKOUT_BUTTON)
        self.driver.execute_script("arguments[0].click();", button)
        
        # Attendre la navigation
        time.sleep(2)
        
        # Vérifier l'URL
        current_url = self.driver.current_url
        print(f"URL après checkout: {current_url}")
        
        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)
    
    def is_empty(self):
        empty = len(self.get_cart_items()) == 0
        print(f"🛒 Panier vide: {empty}")
        return empty
    
    def get_cart_title(self):
        title = self.get_text(self.CART_TITLE)
        print(f"🏷️ Titre panier: {title}")
        return title