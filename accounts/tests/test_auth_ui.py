"""
Tests UI avec Selenium - Authentification
Tests automatisés de l'interface utilisateur
"""
import pytest
import time
from selenium import webdriver
from .test_constants import TEST_PASSWORD, TEST_EMAIL, TEST_USERNAME, SUBMIT_BUTTON_SELECTOR, PROFILE_URL_PATH, CONTENT_REQUIRED_MESSAGE
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from .test_data import VALID_REGISTER_DATA, VALID_LOGIN_DATA, INVALID_LOGIN_DATA
from .test_constants import TEST_PASSWORD, TEST_USERNAME, SUBMIT_BUTTON_SELECTOR


@pytest.mark.ui
@pytest.mark.slow
class SeleniumAuthTests(StaticLiveServerTestCase):
    """Tests UI Selenium pour l'authentification"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration du navigateur"""
        super().setUpClass()
        
        # Options Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Mode sans interface
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            # Essayer d'installer ChromeDriver
            driver_path = ChromeDriverManager().install()
            service = Service(executable_path=driver_path)
            cls.driver = webdriver.Chrome(service=service, options=chrome_options)
            cls.driver.implicitly_wait(10)
        except Exception as e:
            # Si ça échoue, essayer sans service explicite
            try:
                cls.driver = webdriver.Chrome(options=chrome_options)
                cls.driver.implicitly_wait(10)
            except Exception as e2:
                # Dernier recours : mode debug
                print(f"Erreur ChromeDriver: {e}")
                print(f"Erreur fallback: {e2}")
                raise Exception("ChromeDriver non disponible sur ce système")
    
    @classmethod
    def tearDownClass(cls):
        """Fermer le navigateur"""
        cls.driver.quit()
        super().tearDownClass()
    
    def wait_for_element(self, by, value, timeout=10):
        """Attendre qu'un élément soit présent"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    
    # ===== TC-AUTH-01-UI : Inscription via interface =====
    def test_ui_register_success(self):
        """
        TC-AUTH-01-UI: Test d'inscription complet via Selenium
        
        Étapes:
        1. Ouvrir la page d'inscription
        2. Remplir tous les champs
        3. Soumettre le formulaire
        4. Vérifier la redirection et la création du compte
        """
        # 1. Naviguer vers la page d'inscription
        self.driver.get(f'{self.live_server_url}/accounts/register/')
        
        # 2. Attendre le chargement de la page
        self.wait_for_element(By.NAME, 'username')
        
        # 3. Remplir le formulaire (Step 1 - Personal Info)
        import uuid
        unique_email = f'testuser_{uuid.uuid4().hex[:8]}@artygen.com'
        
        self.driver.find_element(By.NAME, 'first_name').send_keys('Test')
        self.driver.find_element(By.NAME, 'last_name').send_keys('User')
        self.driver.find_element(By.NAME, 'email').send_keys(unique_email)
        
        # Utiliser un format de date compatible avec le widget HTML5 date
        birthdate_field = self.driver.find_element(By.NAME, 'birthdate')
        birthdate_field.clear()
        birthdate_field.send_keys('15/01/1995')  # Format DD/MM/YYYY
        
        self.driver.find_element(By.NAME, 'cin').send_keys('12345678')
        
        # 4. Cliquer sur "Next" pour passer au step 2
        next_button = self.driver.find_element(By.ID, 'nextBtn')
        next_button.click()
        time.sleep(1)
        
        # 5. Remplir Step 2 - Account Info
        self.driver.find_element(By.NAME, 'username').send_keys('testuser_ui')
        self.driver.find_element(By.NAME, 'password1').send_keys(TEST_PASSWORD)
        self.driver.find_element(By.NAME, 'password2').send_keys(TEST_PASSWORD)
        
        # Sélectionner le rôle
        from selenium.webdriver.support.ui import Select
        role_select = Select(self.driver.find_element(By.NAME, 'role'))
        role_select.select_by_value('user')
        
        # 6. Passer au step 3
        next_button = self.driver.find_element(By.ID, 'nextBtn')
        next_button.click()
        time.sleep(1)
        
        # 7. Step 3 - Artistic Info (optionnel)
        self.driver.find_element(By.NAME, 'art_style').send_keys('Abstract Digital')
        self.driver.find_element(By.NAME, 'art_interests').send_keys('colors, emotions')
        
        # 8. Attendre que le bouton Submit soit visible
        self.wait_for_element(By.ID, 'submitBtn')
        time.sleep(1)
        
        # 9. Soumettre le formulaire
        submit_button = self.driver.find_element(By.ID, 'submitBtn')
        # Vérifier que le bouton est visible
        assert submit_button.is_displayed(), "Le bouton Submit devrait être visible"
        submit_button.click()
        
        # 10. Attendre la redirection
        time.sleep(3)
        
        # 11. Vérifications
        current_url = self.driver.current_url
        
        # Vérifier dans la base de données
        user_exists = User.objects.filter(username='testuser_ui').exists()
        
        # Après inscription, l'utilisateur est redirigé vers la page d'accueil (/)
        assert current_url.endswith('/') or '/home/' in current_url, \
            f"Redirection incorrecte: {current_url}"
            
        assert user_exists, "L'utilisateur devrait être créé dans la base de données"
        
        print("✅ TC-AUTH-01-UI PASSED: Inscription UI réussie")
    
    # ===== TC-AUTH-03-UI : Connexion via interface =====
    def test_ui_login_success(self):
        """
        TC-AUTH-03-UI: Test de connexion via Selenium
        
        Étapes:
        1. Créer un utilisateur en base
        2. Accéder à la page de login
        3. Remplir et soumettre le formulaire
        4. Vérifier la redirection et la session
        """
        # 1. Créer un utilisateur de test
        User.objects.create_user(
            username='testlogin',
            email='testlogin@artygen.com',
            password=TEST_PASSWORD
        )
        
        # 2. Naviguer vers la page de login
        self.driver.get(f'{self.live_server_url}/accounts/login/')
        
        # 3. Attendre le chargement
        username_field = self.wait_for_element(By.NAME, 'username')
        
        # 4. Remplir le formulaire
        username_field.send_keys('testlogin')
        self.driver.find_element(By.NAME, 'password').send_keys(TEST_PASSWORD)
        
        # 5. Soumettre
        login_button = self.driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON_SELECTOR)
        login_button.click()
        
        # 6. Attendre la redirection
        time.sleep(2)
        
        # 7. Vérifications
        current_url = self.driver.current_url
        assert PROFILE_URL_PATH in current_url, f"Devrait être sur /profile/, mais sur: {current_url}"
        
        # Vérifier que le username apparaît sur la page
        page_content = self.driver.page_source
        assert 'testlogin' in page_content, "Le username devrait apparaître sur la page"
        
        print("✅ TC-AUTH-03-UI PASSED: Connexion UI réussie")
    
    # ===== TC-AUTH-04-UI : Connexion avec mauvais mot de passe =====
    def test_ui_login_wrong_password(self):
        """
        TC-AUTH-04-UI: Test d'échec de connexion
        
        Étapes:
        1. Créer un utilisateur
        2. Tenter de se connecter avec mauvais mot de passe
        3. Vérifier le message d'erreur
        """
        # 1. Créer un utilisateur
        User.objects.create_user(
            username='testfail',
            email='testfail@artygen.com',
            password='CorrectPass123!@#'
        )
        
        # 2. Aller sur la page de login
        self.driver.get(f'{self.live_server_url}/accounts/login/')
        
        # 3. Remplir avec mauvais mot de passe
        self.driver.find_element(By.NAME, 'username').send_keys('testfail')
        self.driver.find_element(By.NAME, 'password').send_keys('WrongPassword123')
        
        # 4. Soumettre
        self.driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON_SELECTOR).click()
        time.sleep(2)
        
        # 5. Vérifier qu'on reste sur /login/
        current_url = self.driver.current_url
        assert '/login/' in current_url, "Devrait rester sur la page de login"
        
        # 6. Vérifier le message d'erreur
        page_content = self.driver.page_source.lower()
        assert 'invalid' in page_content or 'incorrect' in page_content, \
            "Un message d'erreur devrait être affiché"
        
        print("✅ TC-AUTH-04-UI PASSED: Erreur de connexion gérée correctement")
    
    # ===== TC-AUTH-05-UI : Déconnexion =====
    def test_ui_logout(self):
        """
        TC-AUTH-05-UI: Test de déconnexion
        
        Étapes:
        1. Se connecter
        2. Cliquer sur déconnexion
        3. Vérifier la redirection
        """
        # 1. Créer et connecter un utilisateur
        User.objects.create_user(
            username='testlogout',
            password=TEST_PASSWORD
        )
        
        # Se connecter via UI
        self.driver.get(f'{self.live_server_url}/accounts/login/')
        self.driver.find_element(By.NAME, 'username').send_keys('testlogout')
        self.driver.find_element(By.NAME, 'password').send_keys(TEST_PASSWORD)
        self.driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON_SELECTOR).click()
        time.sleep(2)
        
        # 2. Trouver et cliquer sur le bouton de déconnexion
        logout_link = self.driver.find_element(By.LINK_TEXT, 'Logout')
        logout_link.click()
        time.sleep(2)
        
        # 3. Vérifier la redirection
        current_url = self.driver.current_url
        # Après déconnexion, l'utilisateur est redirigé vers la page d'accueil (/)
        assert current_url.endswith('/') or '/home/' in current_url, \
            f"Devrait être redirigé après déconnexion: {current_url}"
        
        print("✅ TC-AUTH-05-UI PASSED: Déconnexion UI réussie")


# ===== Commandes pour exécuter =====
"""
# Tous les tests UI
pytest accounts/tests/test_auth_ui.py -v -m ui

# Un test spécifique
pytest accounts/tests/test_auth_ui.py::SeleniumAuthTests::test_ui_login_success -v

# Avec affichage du navigateur (retirer --headless dans le code)
"""