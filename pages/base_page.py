from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)  # Timeout augmenté
    
    def find_element(self, locator, timeout=15):
        """Trouver un élément avec timeout personnalisable"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            raise NoSuchElementException(f"Element {locator} not found after {timeout}s")
    
    def find_elements(self, locator, timeout=15):
        """Trouver plusieurs éléments"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            return []
    
    def click(self, locator, timeout=15):
        """Cliquer sur un élément"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
    
    def type_text(self, locator, text, timeout=15):
        """Saisir du texte dans un champ"""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator, timeout=15):
        """Récupérer le texte d'un élément"""
        element = self.find_element(locator, timeout)
        return element.text
    
    def is_displayed(self, locator, timeout=10):
        """Vérifier si un élément est affiché"""
        try:
            element = self.find_element(locator, timeout)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    def wait_for_element(self, locator, timeout=15):
        """Attendre qu'un élément soit visible"""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_url_contains(self, text, timeout=15):
        """Attendre que l'URL contienne un texte"""
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )