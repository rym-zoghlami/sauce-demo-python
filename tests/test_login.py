import pytest
import allure
from pages.login_page import LoginPage

@allure.feature("Login Tests")
class TestLogin:
    
    @allure.title("Test de login réussi")
    def test_successful_login(self, login_page):
        """Test login avec utilisateur valide"""
        inventory_page = login_page.login("standard_user", "secret_sauce")
        assert "Products" in inventory_page.get_products_title()

    @allure.title("Test utilisateur bloqué")
    def test_locked_user_login(self, login_page):
        """Test login avec utilisateur bloqué"""
        login_page.login("locked_out_user", "secret_sauce")
        error_message = login_page.get_error_message()
        assert "locked out" in error_message.lower()

    @allure.title("Test identifiants invalides")
    def test_invalid_credentials(self, login_page):
        """Test login avec identifiants invalides"""
        login_page.login("invalid_user", "wrong_password")
        assert login_page.is_error_message_displayed()
        error_message = login_page.get_error_message()
        expected_keywords = ["Username", "password", "match", "do not"]
        assert any(keyword in error_message for keyword in expected_keywords)

    @allure.title("Test username valide mais password invalide")
    def test_valid_username_invalid_password(self, login_page):
        """Test avec username valide mais password incorrect"""
        login_page.login("standard_user", "wrong_password")
        assert login_page.is_error_message_displayed()

    @allure.title("Test username invalide mais password valide")
    def test_invalid_username_valid_password(self, login_page):
        """Test avec username incorrect mais password valide"""
        login_page.login("invalid_user", "secret_sauce")
        assert login_page.is_error_message_displayed()

    @allure.title("Test champs vides")
    def test_empty_credentials(self, login_page):
        """Test sans saisir d'identifiants"""
        login_page.click_login()
        assert login_page.is_error_message_displayed()
        assert "required" in login_page.get_error_message().lower()

    @allure.title("Test username vide")
    def test_empty_username(self, login_page):
        """Test avec username vide"""
        login_page.enter_password("secret_sauce")
        login_page.click_login()
        assert login_page.is_error_message_displayed()

    @allure.title("Test password vide")
    def test_empty_password(self, login_page):
        """Test avec password vide"""
        login_page.enter_username("standard_user")
        login_page.click_login()
        assert login_page.is_error_message_displayed()