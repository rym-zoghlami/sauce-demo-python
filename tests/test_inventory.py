import allure
import pytest
from pages.inventory_page import InventoryPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class TestInventory:
    
    @allure.feature("Inventory")
    @allure.story("Display products")
    def test_display_products(self, login, inventory_page):
        """Test that products are displayed on the inventory page"""
        with allure.step("Verify products are displayed"):
            assert inventory_page.get_products_count() > 0
    
    @allure.feature("Inventory")
    @allure.story("Add item to cart")
    def test_add_item_to_cart(self, login, inventory_page):
        """Test adding an item to the cart"""
        with allure.step("Add item to cart"):
            initial_count = inventory_page.get_cart_count()
            inventory_page.add_item_to_cart()
            
        with allure.step("Wait for cart update and verify"):
            # Attendre que le panier se mette à jour
            try:
                WebDriverWait(inventory_page.driver, 10).until(
                    lambda driver: inventory_page.get_cart_count() == initial_count + 1
                )
            except:
                # Debug: afficher le compte actuel du panier
                print(f"Expected: {initial_count + 1}, Got: {inventory_page.get_cart_count()}")
                print(f"Page title: {inventory_page.driver.title}")
                raise
            
            assert inventory_page.get_cart_count() == initial_count + 1
    
    @allure.feature("Inventory")
    @allure.story("Remove item from cart")
    def test_remove_item_from_cart(self, login, inventory_page):
        """Test removing an item from the cart"""
        with allure.step("Add then remove item from cart"):
            # D'abord ajouter un article
            inventory_page.add_item_to_cart()
            
            # Attendre l'ajout
            WebDriverWait(inventory_page.driver, 10).until(
                lambda driver: inventory_page.get_cart_count() == 1
            )
            
            # Maintenant retirer l'article
            inventory_page.remove_item_from_cart()
            
        with allure.step("Wait for cart update and verify"):
            # Attendre la suppression
            try:
                WebDriverWait(inventory_page.driver, 10).until(
                    lambda driver: inventory_page.get_cart_count() == 0
                )
            except:
                print(f"Cart count after removal: {inventory_page.get_cart_count()}")
                raise
            
            assert inventory_page.get_cart_count() == 0
    
    @allure.feature("Inventory") 
    @allure.story("Sort products low to high")
    def test_sort_products_low_high(self, login, inventory_page):
        """Test sorting products by price low to high"""
        with allure.step("Sort products by price low to high"):
            inventory_page.sort_products("lohi")
            
        with allure.step("Verify products are sorted correctly"):
            prices = inventory_page.get_product_prices()
            assert prices == sorted(prices)
    
    @allure.feature("Inventory")
    @allure.story("Go to cart")
    def test_go_to_cart(self, login, inventory_page):
        """Test navigating to the cart page"""
        with allure.step("Navigate to cart page"):
            cart_page = inventory_page.go_to_cart()
            
        with allure.step("Verify cart page is displayed"):
            try:
                WebDriverWait(inventory_page.driver, 10).until(
                    EC.title_contains("Cart")
                )
            except:
                print(f"Current page title: {inventory_page.driver.title}")
                raise
            
            assert "cart" in inventory_page.driver.current_url.lower()