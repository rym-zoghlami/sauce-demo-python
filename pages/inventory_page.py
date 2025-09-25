from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class InventoryPage(BasePage):
    # Locators CORRIGÉS - Utiliser les bons sélecteurs
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    # Sélecteurs CORRIGÉS pour Sauce Demo
    ADD_TO_CART_BUTTONS = (By.XPATH, "//button[contains(@id, 'add-to-cart')]")
    REMOVE_BUTTONS = (By.XPATH, "//button[contains(@id, 'remove')]")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    PAGE_TITLE = (By.CLASS_NAME, "title")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_cart_count(self):
        """Get the current cart count"""
        try:
            cart_badge = self.find_element(self.CART_BADGE)
            count = int(cart_badge.text)
            print(f"Compteur panier trouvé: {count}")
            return count
        except:
            print("Aucun badge panier trouvé (panier vide)")
            return 0
    
    def get_product_prices(self):
        """Get all product prices as floats"""
        price_elements = self.find_elements(self.PRODUCT_PRICES)
        prices = []
        for element in price_elements:
            price_text = element.text.replace('$', '').strip()
            prices.append(float(price_text))
        return prices
    
    def get_products_count(self):
        """Get number of products displayed"""
        return len(self.find_elements(self.PRODUCT_ITEMS))
    
    def add_item_to_cart(self, index=0):
        """Add item to cart by index"""
        # Attendre que les boutons soient chargés
        time.sleep(1)
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        print(f"Boutons 'Add to cart' trouvés: {len(buttons)}")
        
        if index < len(buttons):
            # Utiliser JavaScript pour cliquer (plus fiable)
            self.driver.execute_script("arguments[0].click();", buttons[index])
            print(f"✅ Article {index} ajouté au panier via JS")
            
            # Attendre la mise à jour du compteur
            time.sleep(2)
        else:
            print(f"❌ Index {index} hors limites")
        return self
    
    def remove_item_from_cart(self, index=0):
        """Remove item from cart by index"""
        # Attendre que les boutons Remove apparaissent
        time.sleep(1)
        buttons = self.find_elements(self.REMOVE_BUTTONS)
        print(f"Boutons 'Remove' trouvés: {len(buttons)}")
        
        if index < len(buttons):
            # Utiliser JavaScript pour cliquer
            self.driver.execute_script("arguments[0].click();", buttons[index])
            print(f"✅ Article {index} retiré du panier via JS")
            
            # Attendre la mise à jour
            time.sleep(2)
        else:
            print(f"❌ Index {index} hors limites")
        return self
    
    def sort_products(self, sort_type="az"):
        """Sort products by different criteria"""
        from selenium.webdriver.support.ui import Select
        dropdown = self.find_element(self.SORT_DROPDOWN)
        select = Select(dropdown)
        
        sort_options = {
            "az": "az",
            "za": "za", 
            "lohi": "lohi",
            "hilo": "hilo"
        }
        select.select_by_value(sort_options.get(sort_type, "az"))
        time.sleep(2)  # Attendre le tri
        return self
    
    def go_to_cart(self):
        """Navigate to cart page"""
        print("Navigation vers le panier...")
        
        # Trouver le lien du panier
        cart_link = self.find_element(self.CART_LINK)
        print(f"Lien panier trouvé: {cart_link.text}")
        
        # Cliquer avec JavaScript
        self.driver.execute_script("arguments[0].click();", cart_link)
        
        # Attendre la navigation
        time.sleep(2)
        
        # Vérifier l'URL
        current_url = self.driver.current_url
        print(f"URL après navigation: {current_url}")
        
        from pages.cart_page import CartPage
        return CartPage(self.driver)
    
    def get_products_title(self):
        """Get products page title"""
        return self.get_text(self.PAGE_TITLE)