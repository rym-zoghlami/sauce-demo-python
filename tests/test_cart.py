import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@allure.feature("Cart Tests")
class TestCart:
    
    @allure.title("Test affichage des articles du panier")
    def test_cart_items_display(self, inventory_page):
        """Test que les articles sont affichés dans le panier"""
        print("=== Début du test ===")
        
        # Ajouter 2 articles avec attente entre les deux
        inventory_page.add_item_to_cart(0)
        print(f"Compteur après 1er article: {inventory_page.get_cart_count()}")
        
        # Attente pour que le premier article soit bien ajouté
        time.sleep(1)
        
        inventory_page.add_item_to_cart(1)
        print(f"Compteur après 2ème article: {inventory_page.get_cart_count()}")
        
        # Vérifier que le compteur est bien à 2
        assert inventory_page.get_cart_count() == 2, f"Compteur devrait être 2, mais est {inventory_page.get_cart_count()}"
        
        # Navigation manuelle vers le panier
        print("Navigation manuelle vers le panier...")
        inventory_page.driver.get("https://www.saucedemo.com/cart.html")
        
        # Vérifier l'URL
        print(f"URL actuelle: {inventory_page.driver.current_url}")
        assert "cart" in inventory_page.driver.current_url.lower()
        
        # Utiliser directement les méthodes de base_page pour vérifier
        from pages.cart_page import CartPage
        cart_page = CartPage(inventory_page.driver)
        
        # Vérifier le titre de la page
        cart_title = cart_page.get_text((By.CLASS_NAME, "title"))
        print(f"Titre de la page: {cart_title}")
        
        # Attendre que les articles soient chargés
        WebDriverWait(cart_page.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
        )
        
        # Vérifier les articles
        items = cart_page.get_cart_items()
        print(f"Nombre d'articles trouvés: {len(items)}")
        
        # Debug : afficher les noms des articles
        if items:
            item_names = cart_page.get_item_names()
            print(f"Noms des articles: {item_names}")
        
        assert len(items) == 2, f"Expected 2 items, but found {len(items)}"
        print("=== Test réussi ===")
    
    @allure.title("Test suppression d'article depuis le panier")
    def test_remove_item_from_cart_page(self, inventory_page):
        """Test suppression d'un article depuis la page panier"""
        # Ajouter un article
        inventory_page.add_item_to_cart(0)
        
        # Navigation manuelle vers le panier
        inventory_page.driver.get("https://www.saucedemo.com/cart.html")
        
        from pages.cart_page import CartPage
        cart_page = CartPage(inventory_page.driver)
        
        # Attendre que la page panier soit chargée
        WebDriverWait(cart_page.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
        )
        
        # Vérifier qu'il y a un article
        assert len(cart_page.get_cart_items()) == 1
        
        # Supprimer l'article avec JavaScript pour plus de fiabilité
        remove_buttons = cart_page.find_elements((By.CSS_SELECTOR, "button.cart_button"))
        if remove_buttons:
            cart_page.driver.execute_script("arguments[0].click();", remove_buttons[0])
        
        # Attendre que l'article soit supprimé avec une attente plus simple
        time.sleep(2)  # Attente simple pour le mode headless
        
        # Vérifier que le panier est vide
        final_count = len(cart_page.get_cart_items())
        assert final_count == 0, f"Expected 0 items, but found {final_count}"
    
    @allure.title("Test continuation shopping")
    def test_continue_shopping(self, inventory_page):
        """Test retour à l'inventaire"""
        # Ajouter un article
        inventory_page.add_item_to_cart(0)
        
        # Navigation manuelle vers le panier
        inventory_page.driver.get("https://www.saucedemo.com/cart.html")
        
        from pages.cart_page import CartPage
        cart_page = CartPage(inventory_page.driver)
        
        # Attendre que la page panier soit chargée
        WebDriverWait(cart_page.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
        )
        
        # Retourner à l'inventaire en utilisant le bouton avec JavaScript
        continue_button = cart_page.find_element((By.ID, "continue-shopping"))
        cart_page.driver.execute_script("arguments[0].click();", continue_button)
        
        # Attendre le retour à l'inventaire
        time.sleep(2)  # Attente simple
        
        # Vérifier qu'on est de retour sur l'inventaire
        current_url = inventory_page.driver.current_url
        assert "inventory" in current_url, f"Expected inventory in URL, got: {current_url}"
        assert "Products" in inventory_page.get_products_title()
    
    @allure.title("Test checkout")
    def test_checkout(self, inventory_page):
        """Test démarrage du checkout"""
        # Ajouter un article
        inventory_page.add_item_to_cart(0)
        
        # Navigation manuelle vers le panier
        inventory_page.driver.get("https://www.saucedemo.com/cart.html")
        
        from pages.cart_page import CartPage
        cart_page = CartPage(inventory_page.driver)
        
        # Attendre que la page panier soit chargée
        WebDriverWait(cart_page.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
        )
        
        # Démarrer le checkout avec JavaScript
        checkout_button = cart_page.find_element((By.ID, "checkout"))
        cart_page.driver.execute_script("arguments[0].click();", checkout_button)
        
        # Attendre le chargement de la page checkout
        time.sleep(2)
        
        # Vérifier qu'on est sur la page checkout
        from pages.checkout_page import CheckoutPage
        checkout_page = CheckoutPage(inventory_page.driver)
        
        # Vérifier l'URL plutôt que l'élément (plus fiable)
        current_url = inventory_page.driver.current_url
        assert "checkout" in current_url, f"Expected checkout in URL, got: {current_url}"
    
    @allure.title("Test panier vide")
    def test_empty_cart(self, inventory_page):
        """Test comportement avec panier vide"""
        # Navigation manuelle vers le panier
        inventory_page.driver.get("https://www.saucedemo.com/cart.html")
        
        from pages.cart_page import CartPage
        cart_page = CartPage(inventory_page.driver)
        
        # Vérifier que le panier est empty
        assert cart_page.is_empty()
        
        # Vérifier le titre
        cart_title = cart_page.get_text((By.CLASS_NAME, "title"))
        assert "Your Cart" in cart_title or "Cart" in cart_title