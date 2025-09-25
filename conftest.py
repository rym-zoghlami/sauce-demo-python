import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import sys

# Ajouter le chemin des pages au PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'pages'))
from pages.login_page import LoginPage

@pytest.fixture(scope="function")
def driver():
    """
    Fixture principale pour initialiser et fermer le driver WebDriver
    Optimisé pour GitHub Actions et développement local
    """
    chrome_options = Options()
    
    # Configuration pour GitHub Actions (headless)
    if os.getenv('GITHUB_ACTIONS') == 'true':
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        print("🚀 Mode GitHub Actions détecté - Configuration headless")
    else:
        # Mode développement local (avec interface)
        chrome_options.add_argument("--window-size=1920,1080")
        print("💻 Mode développement local - Avec interface graphique")
    
    # Options communes
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Désactiver les logs inutiles
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Gestion du ChromeDriver
    try:
        # Essayer d'abord avec webdriver-manager pour une meilleure compatibilité
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ ChromeDriver installé via webdriver-manager")
    except Exception as e:
        print(f"⚠️  webdriver-manager échoué, utilisation du ChromeDriver système: {e}")
        # Fallback: utiliser le ChromeDriver du système
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Configuration du driver
    driver.implicitly_wait(10)
    driver.maximize_window()
    
    # Masquer l'automation
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    print(f"🌐 Driver initialisé - Headless: {chrome_options.arguments.count('--headless') > 0}")
    
    yield driver
    
    # Nettoyage après le test
    print("🧹 Nettoyage du driver...")
    try:
        driver.quit()
        print("✅ Driver fermé avec succès")
    except Exception as e:
        print(f"⚠️  Erreur lors de la fermeture du driver: {e}")

@pytest.fixture
def login_page(driver):
    """
    Fixture pour la page de login avec chargement automatique
    """
    print("📄 Initialisation de la page de login...")
    page = LoginPage(driver)
    
    # Ouvrir la page avec gestion d'erreurs
    try:
        page.open()
        
        # Attendre que la page soit complètement chargée
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        wait.until(EC.presence_of_element_located((By.ID, "password")))
        wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
        
        print("✅ Page de login chargée avec succès")
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement de la page de login: {e}")
        print(f"📄 URL actuelle: {driver.current_url}")
        print(f"🏷️ Titre de la page: {driver.title}")
        raise
    
    return page

@pytest.fixture
def login(login_page):
    """
    Fixture pour effectuer un login automatique
    Retourne la page d'inventaire après connexion
    """
    print("🔐 Début du processus de login...")
    
    try:
        # Login avec l'utilisateur standard
        inventory_page = login_page.login("standard_user", "secret_sauce")
        
        # Vérifier que le login a réussi
        WebDriverWait(login_page.driver, 15).until(
            EC.url_contains("inventory")
        )
        
        print("✅ Login réussi - Redirection vers l'inventaire")
        return inventory_page
        
    except Exception as e:
        print(f"❌ Erreur lors du login: {e}")
        print(f"🌐 URL actuelle: {login_page.driver.current_url}")
        raise

@pytest.fixture
def inventory_page(login):
    """
    Fixture pour la page d'inventaire (après login)
    """
    print("📦 Retour de la fixture inventory_page")
    return login

@pytest.fixture(scope="session")
def allure_environment():
    """
    Configuration de l'environnement pour les rapports Allure
    """
    environment = {
        "Browser": "Chrome",
        "Python Version": sys.version.split()[0],
        "OS": os.name,
        "CI": "GitHub Actions" if os.getenv('GITHUB_ACTIONS') == 'true' else "Local"
    }
    
    # Écrire le fichier d'environnement Allure
    with open('allure-results/environment.properties', 'w') as f:
        for key, value in environment.items():
            f.write(f"{key}={value}\n")
    
    return environment

# Hooks pytest pour une meilleure gestion des tests
def pytest_runtest_setup(item):
    """Avant chaque test"""
    test_name = item.name
    print(f"\n🎬 Début du test: {test_name}")

def pytest_runtest_teardown(item, nextitem):
    """Après chaque test"""
    test_name = item.name
    print(f"✅ Fin du test: {test_name}\n")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook pour capturer les screenshots en cas d'échec
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Prendre un screenshot en cas d'échec
        try:
            driver = item.funcargs.get('driver')
            if driver:
                screenshot_dir = "screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                
                test_name = item.name.replace("/", "_").replace("\\", "_")
                screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
                driver.save_screenshot(screenshot_path)
                print(f"📸 Screenshot sauvegardé: {screenshot_path}")
                
                # Attacher le screenshot au rapport Allure
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"screenshot_{test_name}",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"⚠️  Impossible de prendre un screenshot: {e}")

# Configuration pour les tests parallèles (pytest-xdist)
def pytest_configure(config):
    """Configuration pytest"""
    # Ajouter des marqueurs personnalisés
    config.addinivalue_line(
        "markers", "login: tests related to login functionality"
    )
    config.addinivalue_line(
        "markers", "inventory: tests related to inventory page"
    )
    config.addinivalue_line(
        "markers", "cart: tests related to cart functionality"
    )
    config.addinivalue_line(
        "markers", "slow: slow running tests"
    )

# Fixtures supplémentaires pour différents scénarios
@pytest.fixture
def locked_user_login(login_page):
    """Fixture pour login avec utilisateur bloqué"""
    print("🔒 Tentative de login avec utilisateur bloqué")
    result = login_page.login("locked_out_user", "secret_sauce")
    return result

@pytest.fixture
def problem_user_login(login_page):
    """Fixture pour login avec utilisateur problématique"""
    print("⚠️  Tentative de login avec utilisateur problématique")
    result = login_page.login("problem_user", "secret_sauce")
    return result

@pytest.fixture
def performance_glitch_user_login(login_page):
    """Fixture pour login avec utilisateur lent"""
    print("🐌 Tentative de login avec utilisateur lent")
    result = login_page.login("performance_glitch_user", "secret_sauce")
    return result

@pytest.fixture
def cart_with_items(inventory_page):
    """Fixture pour un panier avec des articles"""
    print("🛒 Ajout d'articles au panier...")
    
    # Ajouter 2 articles au panier
    inventory_page.add_item_to_cart(0)
    inventory_page.add_item_to_cart(1)
    
    # Vérifier l'ajout
    cart_count = inventory_page.get_cart_count()
    print(f"📦 Panier contient {cart_count} articles")
    
    return inventory_page

# Fixture pour les tests nécessitant une page spécifique
@pytest.fixture
def cart_page(inventory_page):
    """Fixture pour la page panier (avec navigation)"""
    print("📦 Navigation vers le panier...")
    cart_page = inventory_page.go_to_cart()
    
    # Vérifier la navigation
    WebDriverWait(inventory_page.driver, 10).until(
        EC.url_contains("cart")
    )
    
    print("✅ Navigation vers le panier réussie")
    return cart_page

@pytest.fixture
def checkout_page(cart_page):
    """Fixture pour la page checkout (avec navigation)"""
    print("💰 Navigation vers le checkout...")
    checkout_page = cart_page.checkout()
    
    # Vérifier la navigation
    WebDriverWait(cart_page.driver, 10).until(
        EC.url_contains("checkout")
    )
    
    print("✅ Navigation vers le checkout réussie")
    return checkout_page

# Configuration pour les temps d'attente adaptatifs
@pytest.fixture
def wait_short(driver):
    """Wait court (5 secondes)"""
    return WebDriverWait(driver, 5)

@pytest.fixture
def wait_medium(driver):
    """Wait moyen (10 secondes)"""
    return WebDriverWait(driver, 10)

@pytest.fixture
def wait_long(driver):
    """Wait long (20 secondes)"""
    return WebDriverWait(driver, 20)

print("✅ Configuration pytest chargée avec succès!")