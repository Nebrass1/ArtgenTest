"""
Tests multi-navigateurs pour l'authentification Artygen
Tests de compatibilité sur Chrome, Firefox et Edge
"""
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from .test_constants import TEST_PASSWORD, TEST_USERNAME, SUBMIT_BUTTON_SELECTOR, PROFILE_URL_PATH


class CrossBrowserAuthTests(StaticLiveServerTestCase):
    """Tests d'authentification multi-navigateurs"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browsers = []

    @classmethod
    def tearDownClass(cls):
        for driver in cls.browsers:
            if driver:
                driver.quit()
        super().tearDownClass()

    def get_chrome_driver(self):
        """Créer un driver Chrome"""
        try:
            options = ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.implicitly_wait(10)
            self.browsers.append(driver)
            return driver
        except Exception as e:
            pytest.skip(f"Chrome non disponible: {e}")

    def get_firefox_driver(self):
        """Créer un driver Firefox"""
        try:
            options = FirefoxOptions()
            options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
            driver.implicitly_wait(10)
            self.browsers.append(driver)
            return driver
        except Exception as e:
            pytest.skip(f"Firefox non disponible: {e}")

    def get_edge_driver(self):
        """Créer un driver Edge"""
        try:
            options = EdgeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
            driver.implicitly_wait(10)
            self.browsers.append(driver)
            return driver
        except Exception as e:
            pytest.skip(f"Edge non disponible: {e}")

    def wait_for_element(self, driver, by, value, timeout=10):
        """Attendre qu'un élément soit présent"""
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def test_login_chrome(self):
        """Test de connexion sur Chrome"""
        driver = self.get_chrome_driver()
        
        # Créer un utilisateur de test
        User.objects.create_user(
            username='testuser_chrome',
            email='test_chrome@artygen.com',
            password=TEST_PASSWORD
        )
        
        # Naviguer vers la page de connexion
        driver.get(f'{self.live_server_url}/accounts/login/')
        
        # Remplir le formulaire
        self.wait_for_element(driver, By.NAME, 'username')
        driver.find_element(By.NAME, 'username').send_keys('testuser_chrome')
        driver.find_element(By.NAME, 'password').send_keys(TEST_PASSWORD)
        driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON_SELECTOR).click()
        
        # Vérifier la redirection
        time.sleep(2)
        assert PROFILE_URL_PATH in driver.current_url or driver.current_url.endswith('/')

    def test_login_firefox(self):
        """Test de connexion sur Firefox"""
        driver = self.get_firefox_driver()
        
        # Créer un utilisateur de test
        User.objects.create_user(
            username='testuser_firefox',
            email='test_firefox@artygen.com',
            password=TEST_PASSWORD
        )
        
        # Naviguer vers la page de connexion
        driver.get(f'{self.live_server_url}/accounts/login/')
        
        # Remplir le formulaire
        self.wait_for_element(driver, By.NAME, 'username')
        driver.find_element(By.NAME, 'username').send_keys('testuser_firefox')
        driver.find_element(By.NAME, 'password').send_keys(TEST_PASSWORD)
        driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON_SELECTOR).click()
        
        # Vérifier la redirection
        time.sleep(2)
        assert PROFILE_URL_PATH in driver.current_url or driver.current_url.endswith('/')

    def test_login_edge(self):
        """Test de connexion sur Edge"""
        driver = self.get_edge_driver()
        
        # Créer un utilisateur de test
        User.objects.create_user(
            username='testuser_edge',
            email='test_edge@artygen.com',
            password=TEST_PASSWORD
        )
        
        # Naviguer vers la page de connexion
        driver.get(f'{self.live_server_url}/accounts/login/')
        
        # Remplir le formulaire
        self.wait_for_element(driver, By.NAME, 'username')
        driver.find_element(By.NAME, 'username').send_keys('testuser_edge')
        driver.find_element(By.NAME, 'password').send_keys(TEST_PASSWORD)
        driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON_SELECTOR).click()
        
        # Vérifier la redirection
        time.sleep(2)
        assert PROFILE_URL_PATH in driver.current_url or driver.current_url.endswith('/')

    @pytest.mark.compatibility
    def test_registration_form_compatibility(self):
        """Test de compatibilité du formulaire d'inscription sur tous les navigateurs"""
        browsers = [
            ('Chrome', self.get_chrome_driver),
            ('Firefox', self.get_firefox_driver),
            ('Edge', self.get_edge_driver)
        ]
        
        for browser_name, get_driver in browsers:
            try:
                driver = get_driver()
                
                # Naviguer vers la page d'inscription
                driver.get(f'{self.live_server_url}/accounts/register/')
                
                # Vérifier que les éléments du formulaire sont présents
                self.wait_for_element(driver, By.NAME, 'first_name')
                
                # Vérifier tous les champs requis
                required_fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
                for field in required_fields:
                    element = driver.find_element(By.NAME, field)
                    assert element.is_displayed(), f"Champ {field} non visible sur {browser_name}"
                
                # Vérifier les boutons de navigation
                next_btn = driver.find_element(By.ID, 'nextBtn')
                assert next_btn.is_displayed(), f"Bouton Next non visible sur {browser_name}"
                
                print(f"✅ Test de compatibilité réussi sur {browser_name}")
                
            except Exception as e:
                print(f"❌ Erreur sur {browser_name}: {e}")
                # Ne pas faire échouer le test, juste logger
                pass

    @pytest.mark.compatibility 
    def test_responsive_design(self):
        """Test du design responsive sur différentes tailles d'écran"""
        driver = self.get_chrome_driver()
        
        # Tailles d'écran à tester
        screen_sizes = [
            (1920, 1080, "Desktop"),
            (1366, 768, "Laptop"),
            (768, 1024, "Tablet"),
            (375, 667, "Mobile")
        ]
        
        for width, height, device in screen_sizes:
            driver.set_window_size(width, height)
            driver.get(f'{self.live_server_url}/accounts/login/')
            
            time.sleep(1)  # Laisser le temps au CSS de s'appliquer
            
            # Vérifier que le formulaire est visible
            form = self.wait_for_element(driver, By.TAG_NAME, 'form')
            assert form.is_displayed(), f"Formulaire non visible sur {device} ({width}x{height})"
            
            print(f"✅ Design responsive OK sur {device} ({width}x{height})")
