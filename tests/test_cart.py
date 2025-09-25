import pytest
import allure
import time

@allure.feature("Cart Tests")
class TestCart:
    
    @allure.title("Test affichage des articles du panier")
    def test_cart_items_display(self, inventory_page):
        """Test que les articles sont affichés dans le panier"""
        # Ajouter 2 articles
        inventory_page.add_item_to_cart(0)
        time.sleep(2)
        inventory_page.add_item_to_cart(1)
        time.sleep(2)
        
        # Vérifier le compteur
        cart_count = inventory_page.get_cart_count()
        print(f"🛒 Compteur avant navigation: {cart_count}")
        assert cart_count == 2
        
        # Aller au panier
        cart_page = inventory_page.go_to_cart()
        time.sleep(3)
        
        # Vérifier les articles
        items = cart_page.get_cart_items()
        assert len(items) == 2
        print("✅ 2 articles trouvés dans le panier")
    
    @allure.title("Test suppression d'article depuis le panier")
    def test_remove_item_from_cart_page(self, inventory_page):
        """Test suppression d'un article depuis la page panier"""
        # Ajouter un article
        inventory_page.add_item_to_cart(0)
        time.sleep(2)
        
        # Aller au panier
        cart_page = inventory_page.go_to_cart()
        time.sleep(3)
        
        # Vérifier et supprimer
        items_before = cart_page.get_cart_items()
        assert len(items_before) == 1
        
        cart_page.remove_item(0)
        time.sleep(3)
        
        # Vérifier suppression
        items_after = cart_page.get_cart_items()
        assert len(items_after) == 0
        print("✅ Article supprimé avec succès")
    
    @allure.title("Test continuation shopping")
    def test_continue_shopping(self, inventory_page):
        """Test retour à l'inventaire"""
        # Aller au panier
        cart_page = inventory_page.go_to_cart()
        time.sleep(3)
        
        # Retour à l'inventaire
        new_inventory_page = cart_page.continue_shopping()
        time.sleep(3)
        
        # Vérifier retour
        current_url = new_inventory_page.driver.current_url
        print(f"🌐 URL après retour: {current_url}")
        assert "inventory" in current_url
        print("✅ Retour à l'inventaire réussi")
    
    @allure.title("Test checkout")
    def test_checkout(self, inventory_page):
        """Test démarrage du checkout"""
        # Ajouter un article
        inventory_page.add_item_to_cart(0)
        time.sleep(2)
        
        # Aller au panier
        cart_page = inventory_page.go_to_cart()
        time.sleep(3)
        
        # Démarrer checkout
        checkout_page = cart_page.checkout()
        time.sleep(3)
        
        # Vérifier page checkout
        current_url = checkout_page.driver.current_url
        print(f"🌐 URL checkout: {current_url}")
        assert "checkout" in current_url
        print("✅ Checkout démarré avec succès")
    
    @allure.title("Test panier vide")
    def test_empty_cart(self, inventory_page):
        """Test comportement avec panier vide"""
        # Aller directement au panier
        from pages.cart_page import CartPage
        cart_page = CartPage(inventory_page.driver)
        cart_page.driver.get("https://www.saucedemo.com/cart.html")
        time.sleep(3)
        
        # Vérifier panier vide
        assert cart_page.is_empty()
        print("✅ Panier vide confirmé")