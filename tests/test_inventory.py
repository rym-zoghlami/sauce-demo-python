import allure
import pytest
import time

class TestInventory:
    
    @allure.feature("Inventory")
    @allure.story("Display products")
    def test_display_products(self, inventory_page):
        """Test that products are displayed on the inventory page"""
        product_count = inventory_page.get_products_count()
        print(f"📊 Produits affichés: {product_count}")
        assert product_count > 0
    
    @allure.feature("Inventory")
    @allure.story("Add item to cart")
    def test_add_item_to_cart(self, inventory_page):
        """Test adding an item to the cart"""
        initial_count = inventory_page.get_cart_count()
        print(f"🛒 Compteur initial: {initial_count}")
        
        inventory_page.add_item_to_cart(0)
        
        # Attendre et vérifier
        time.sleep(3)
        final_count = inventory_page.get_cart_count()
        print(f"🛒 Compteur final: {final_count}")
        
        assert final_count == initial_count + 1, f"Attendu: {initial_count + 1}, Obtenu: {final_count}"
    
    @allure.feature("Inventory")
    @allure.story("Remove item from cart")
    def test_remove_item_from_cart(self, inventory_page):
        """Test removing an item from the cart"""
        # Ajouter un article
        inventory_page.add_item_to_cart(0)
        time.sleep(2)
        
        count_after_add = inventory_page.get_cart_count()
        print(f"🛒 Après ajout: {count_after_add}")
        assert count_after_add == 1
        
        # Retirer l'article
        inventory_page.remove_item_from_cart(0)
        time.sleep(3)
        
        final_count = inventory_page.get_cart_count()
        print(f"🛒 Après suppression: {final_count}")
        assert final_count == 0
    
    @allure.feature("Inventory") 
    @allure.story("Sort products low to high")
    def test_sort_products_low_high(self, inventory_page):
        """Test sorting products by price low to high"""
        inventory_page.sort_products("lohi")
        
        prices = inventory_page.get_product_prices()
        print(f"📈 Prix triés: {prices}")
        assert prices == sorted(prices)
    
    @allure.feature("Inventory")
    @allure.story("Go to cart")
    def test_go_to_cart(self, inventory_page):
        """Test navigating to the cart page"""
        # Ajouter un article
        inventory_page.add_item_to_cart(0)
        time.sleep(2)
        
        cart_page = inventory_page.go_to_cart()
        time.sleep(2)
        
        # Vérifier la page panier
        current_url = cart_page.driver.current_url
        print(f"🌐 URL panier: {current_url}")
        assert "cart" in current_url
        
        # Vérifier le titre
        cart_title = cart_page.get_cart_title()
        assert "cart" in cart_title.lower()