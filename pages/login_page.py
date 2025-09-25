from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 15)  # Augmenter le timeout
    
    def open(self):
        """Ouvrir la page de login avec attente explicite"""
        self.driver.get("https://www.saucedemo.com/")
        
        # Attendre que la page soit complètement chargée
        try:
            self.wait.until(EC.title_contains("Swag Labs"))
            self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
            self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT))
            self.wait.until(EC.presence_of_element_located(self.LOGIN_BUTTON))
            print("✓ Page de login chargée avec succès")
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            print(f"URL actuelle: {self.driver.current_url}")
            print(f"Titre de la page: {self.driver.title}")
            raise
        return self
    
    def enter_username(self, username):
        """Saisir le nom d'utilisateur avec vérification"""
        element = self.find_element(self.USERNAME_INPUT)
        element.clear()
        element.send_keys(username)
        return self
    
    def enter_password(self, password):
        """Saisir le mot de passe avec vérification"""
        element = self.find_element(self.PASSWORD_INPUT)
        element.clear()
        element.send_keys(password)
        return self
    
    def click_login(self):
        """Cliquer sur le bouton login"""
        self.click(self.LOGIN_BUTTON)
        return self
    
    def login(self, username, password):
        """Méthode de login complète avec gestion des erreurs"""
        print(f"Tentative de login avec: {username}")
        
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        
        # Attendre le résultat du login
        try:
            # Si login réussi, on devrait être redirigé vers l'inventaire
            self.wait.until(lambda driver: "inventory" in driver.current_url or "error" in driver.current_url)
            
            if "inventory" in self.driver.current_url:
                print("✓ Login réussi - Redirection vers l'inventaire")
                from pages.inventory_page import InventoryPage
                return InventoryPage(self.driver)
            else:
                print("✗ Login échoué - Reste sur la page de login")
                return self
                
        except Exception as e:
            print(f"Erreur lors du login: {e}")
            return self
    
    def get_error_message(self):
        """Récupérer le message d'erreur"""
        try:
            return self.get_text(self.ERROR_MESSAGE)
        except:
            return "Aucun message d'erreur trouvé"
    
    def is_error_message_displayed(self):
        """Vérifier si un message d'erreur est affiché"""
        return self.is_displayed(self.ERROR_MESSAGE)
    
    def wait_for_login_page(self):
        """Attendre que la page de login soit complètement chargée"""
        self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
        self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT))
        return self