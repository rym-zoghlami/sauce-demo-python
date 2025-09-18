import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser: chrome, firefox, headless")
    parser.addoption("--headless", action="store_true", default=False, help="Run in headless mode")

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    if browser.lower() == "chrome":
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
    else:
        pytest.skip("Unsupported browser")
    
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def login_page(driver):
    from pages.login_page import LoginPage
    page = LoginPage(driver)
    page.open()
    return page

@pytest.fixture
def inventory_page(login_page):
    return login_page.login("standard_user", "secret_sauce")

#@pytest.fixture
#def cart_page(inventory_page):
    #inventory_page.add_item_to_cart(0)
    #inventory_page.add_item_to_cart(1)
    #return inventory_page.go_to_cart()



@pytest.fixture
def cart_page(inventory_page):
    """Fixture pour un panier avec des articles"""
    # Ajouter des articles avec des attentes
    inventory_page.add_item_to_cart(0)
    
    # Attendre que le premier article soit ajouté
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    WebDriverWait(inventory_page.driver, 10).until(
        lambda driver: inventory_page.get_cart_count() > 0
    )
    
    inventory_page.add_item_to_cart(1)
    
    # Attendre que le deuxième article soit ajouté
    WebDriverWait(inventory_page.driver, 10).until(
        lambda driver: inventory_page.get_cart_count() > 1
    )
    
    return inventory_page.go_to_cart()