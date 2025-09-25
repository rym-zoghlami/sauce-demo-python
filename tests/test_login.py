import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

@allure.feature("Login Tests")
class TestLogin:
    
    @allure.title("Test de connexion au site")
    def test_site_connectivity(self, driver):
        """Test que le site est accessible"""
        with allure.step("Chargement de la page de login"):
            driver.get("https://www.saucedemo.com/")
            
            # Attendre le chargement complet
            WebDriverWait(driver, 20).until(
                EC.title_contains("Swag Labs")
            )
            
            # Vérifier les éléments essentiels
            username_field = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "user-name"))
            )
            password_field = driver.find_element(By.ID, "password")
            login_button = driver.find_element(By.ID, "login-button")
            
            assert username_field.is_displayed()
            assert password_field.is_displayed()
            assert login_button.is_displayed()
            
            print("✓ Site accessible et éléments trouvés")
    
    @allure.title("Test de login réussi")
    def test_successful_login(self, login_page):
        """Test login avec utilisateur valide"""
        with allure.step("Login avec utilisateur standard"):
            inventory_page = login_page.login("standard_user", "secret_sauce")
            
        with allure.step("Vérification de la redirection"):
            # Attendre la redirection
            WebDriverWait(login_page.driver, 15).until(
                EC.url_contains("inventory")
            )
            
            # Vérifier l'URL et le titre
            assert "inventory" in login_page.driver.current_url
            assert "Swag Labs" in login_page.driver.title
            
            # Vérifier que nous avons bien un objet InventoryPage
            from pages.inventory_page import InventoryPage
            assert isinstance(inventory_page, InventoryPage)
            
            # Vérifier que des produits sont affichés
            product_count = inventory_page.get_products_count()
            assert product_count > 0
            print(f"✓ Login réussi - {product_count} produits affichés")
    
    @allure.title("Test utilisateur bloqué")
    def test_locked_user_login(self, login_page):
        """Test login avec utilisateur bloqué"""
        with allure.step("Login avec utilisateur bloqué"):
            result_page = login_page.login("locked_out_user", "secret_sauce")
            
        with allure.step("Vérification du message d'erreur"):
            # Devrait rester sur la page de login
            assert "saucedemo.com" in login_page.driver.current_url
            assert "inventory" not in login_page.driver.current_url
            
            # Vérifier le message d'erreur
            assert login_page.is_error_message_displayed()
            
            error_message = login_page.get_error_message()
            print(f"Message d'erreur: {error_message}")
            assert "locked" in error_message.lower()
            print("✓ Message d'erreur correct pour utilisateur bloqué")
    
    @allure.title("Test identifiants invalides")
    def test_invalid_credentials(self, login_page):
        """Test login avec identifiants invalides"""
        with allure.step("Login avec identifiants invalides"):
            result_page = login_page.login("invalid_user", "wrong_password")
            
        with allure.step("Vérification de l'erreur"):
            assert login_page.is_error_message_displayed()
            
            error_message = login_page.get_error_message()
            expected_keywords = ["username", "password", "match", "do not"]
            assert any(keyword in error_message.lower() for keyword in expected_keywords)
            print("✓ Message d'erreur pour identifiants invalides")
    
    @allure.title("Test champs vides")
    def test_empty_credentials(self, login_page):
        """Test sans saisir d'identifiants"""
        with allure.step("Clic sur login sans identifiants"):
            login_page.click_login()
            
        with allure.step("Vérification de l'erreur"):
            # Devrait rester sur la page de login
            assert "saucedemo.com" in login_page.driver.current_url
            
            assert login_page.is_error_message_displayed()
            error_message = login_page.get_error_message()
            assert "required" in error_message.lower()
            print("✓ Message d'erreur pour champs vides")
    
    @allure.title("Test username vide")
    def test_empty_username(self, login_page):
        """Test avec username vide"""
        with allure.step("Saisie du mot de passe seulement"):
            login_page.enter_password("secret_sauce")
            login_page.click_login()
            
        with allure.step("Vérification de l'erreur"):
            assert login_page.is_error_message_displayed()
            error_message = login_page.get_error_message()
            print(f"Message d'erreur: {error_message}")
            print("✓ Erreur détectée pour username vide")
    
    @allure.title("Test password vide")
    def test_empty_password(self, login_page):
        """Test avec password vide"""
        with allure.step("Saisie du username seulement"):
            login_page.enter_username("standard_user")
            login_page.click_login()
            
        with allure.step("Vérification de l'erreur"):
            assert login_page.is_error_message_displayed()
            error_message = login_page.get_error_message()
            print(f"Message d'erreur: {error_message}")
            print("✓ Erreur détectée pour password vide")