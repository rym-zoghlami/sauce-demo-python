from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class InventoryPage(BasePage):
    
    def get_cart_count(self):
        """Get the current cart count with explicit wait"""
        try:
            cart_badge = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
            )
            return int(cart_badge.text)
        except:
            # Si le badge n'existe pas, le panier est vide
            return 0
    
    def get_product_prices(self):
        """Get all product prices as floats"""
        price_elements = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        prices = []
        for element in price_elements:
            price_text = element.text.replace('$', '').strip()
            prices.append(float(price_text))
        return prices