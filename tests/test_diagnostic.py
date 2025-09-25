import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def test_diagnostic_site_access(driver):
    """Test de diagnostic pour vérifier l'accès au site"""
    print("=== TEST DIAGNOSTIC ===")
    
    # 1. Charger la page
    print("1. Chargement de la page...")
    driver.get("https://www.saucedemo.com/")
    print(f"   URL actuelle: {driver.current_url}")
    print(f"   Titre de la page: {driver.title}")
    
    # 2. Vérifier le titre
    print("2. Vérification du titre...")
    WebDriverWait(driver, 20).until(EC.title_contains("Swag Labs"))
    assert "Swag Labs" in driver.title
    print("   ✓ Titre correct")
    
    # 3. Vérifier les champs de login
    print("3. Vérification des champs de login...")
    
    username_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )
    print("   ✓ Champ username trouvé")
    
    password_field = driver.find_element(By.ID, "password")
    print("   ✓ Champ password trouvé")
    
    login_button = driver.find_element(By.ID, "login-button")
    print("   ✓ Bouton login trouvé")
    
    # 4. Vérifier que les champs sont interactifs
    print("4. Vérification de l'interactivité...")
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-name")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "password")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login-button")))
    print("   ✓ Tous les éléments sont interactifs")
    
    # 5. Tester un login simple
    print("5. Test de login...")
    username_field.send_keys("standard_user")
    password_field.send_keys("secret_sauce")
    login_button.click()
    
    # 6. Vérifier la redirection
    print("6. Vérification de la redirection...")
    WebDriverWait(driver, 15).until(EC.url_contains("inventory"))
    assert "inventory" in driver.current_url
    print("   ✓ Redirection vers l'inventaire réussie")
    
    print("=== DIAGNOSTIC TERMINÉ AVEC SUCCÈS ===")