import pytest
import allure
from selenium.webdriver.common.by import By
from pages.inventory_page import InventoryPage

@allure.feature("Inventory Tests")
class TestInventory:
    
    @allure.title("Test affichage des produits")
    def test_display_products(self, inventory_page):
        """Test que les produits sont affichés"""
        items = inventory_page.get_inventory_items()
        assert len(items) > 0
    
    @allure.title("Test ajout au panier")
    def test_add_item_to_cart(self, inventory_page):
        """Test ajout d'un produit au panier"""
        initial_count = inventory_page.get_cart_count()
        inventory_page.add_item_to_cart(0)
        assert inventory_page.get_cart_count() == initial_count + 1
    
    @allure.title("Test suppression du panier")
    def test_remove_item_from_cart(self, inventory_page):
        """Test suppression d'un article du panier depuis l'inventory"""
        # Ajouter un article
        inventory_page.add_item_to_cart(0)
        
        # Vérifier qu'il est ajouté
        assert inventory_page.get_cart_count() == 1
        
        # Le retirer depuis l'inventory
        inventory_page.remove_item_from_cart(0)
        
        # Vérifier qu'il est supprimé
        assert inventory_page.get_cart_count() == 0
    
    @allure.title("Test tri des produits par prix croissant")
    def test_sort_products_low_high(self, inventory_page):
        """Test le tri des produits par prix croissant"""
        prices_before = inventory_page.get_item_prices()
        inventory_page.sort_products("lohi")
        prices_after = inventory_page.get_item_prices()
        assert prices_after == sorted(prices_before)
    
    @allure.title("Test navigation vers panier")
    def test_go_to_cart(self, inventory_page):
        """Test navigation vers le panier"""
        # Ajouter un produit au panier d'abord
        inventory_page.add_item_to_cart(0)
        
        # Aller au panier
        cart_page = inventory_page.go_to_cart()
        
        # Vérifier le titre de la page
        cart_title = cart_page.get_cart_title()
        assert "Your Cart" in cart_title
        
        # Vérifier qu'il y a au moins un article
        items = cart_page.get_cart_items()
        assert len(items) > 0