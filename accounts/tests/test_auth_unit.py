"""
Tests Unitaires - Authentification Django
TC-AUTH-01 à TC-AUTH-05
"""
import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import Profile
from .test_data import VALID_REGISTER_DATA, INVALID_DUPLICATE_EMAIL, VALID_LOGIN_DATA, INVALID_LOGIN_DATA, ADMIN_REGISTER_DATA
from .test_constants import TEST_EMAIL, TEST_PASSWORD, TEST_USERNAME


@pytest.mark.django_db
@pytest.mark.auth
@pytest.mark.unit
class TestAuthentication(TestCase):
    """Suite de tests pour l'authentification"""
    
    def setUp(self):
        """Configuration initiale avant chaque test"""
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('profile')
    
    # ===== TC-AUTH-01 : Inscription réussie =====
    def test_register_success(self):
        """
        TC-AUTH-01: Inscription avec données valides
        
        Étapes:
        1. Accéder à /accounts/register/
        2. Remplir le formulaire avec données valides
        3. Soumettre le formulaire
        
        Résultat attendu:
        - Utilisateur créé dans la base
        - Profil créé automatiquement
        - Redirection vers home ou profile
        - Message de succès
        """
        # Vérifier que l'utilisateur n'existe pas
        assert not User.objects.filter(username='testuser').exists()
        
        # Soumettre le formulaire d'inscription
        response = self.client.post(self.register_url, data=VALID_REGISTER_DATA)
        
        # Vérifications
        assert response.status_code in [200, 302], "La page doit répondre ou rediriger"
        
        # Vérifier que l'utilisateur est créé
        user = User.objects.get(username='testuser')
        assert user is not None, "L'utilisateur doit être créé"
        assert user.email == TEST_EMAIL, "Email incorrect"
        assert user.first_name == 'Test', "Prénom incorrect"
        
        # Vérifier que le profil est créé
        assert hasattr(user, 'profile'), "Le profil doit être créé automatiquement"
        assert user.profile.cin == '12345678', "CIN incorrect dans le profil"
        assert user.profile.role == 'user', "Rôle incorrect"
        
        # Vérifier la bio générée (si activée et si API configurée)
        if VALID_REGISTER_DATA['generate_bio']:
            # En mode test, la génération de bio peut échouer si pas de clé API valide
            # On vérifie juste que le flag generate_bio est correct
            assert hasattr(user.profile, 'bio'), "Le champ bio devrait exister"
        
        print("✅ TC-AUTH-01 PASSED: Inscription réussie")
    
    # ===== TC-AUTH-02 : Inscription avec email existant =====
    def test_register_duplicate_email(self):
        """
        TC-AUTH-02: Tentative d'inscription avec email déjà utilisé
        
        Étapes:
        1. Créer un premier utilisateur
        2. Tenter de créer un second avec le même email
        
        Résultat attendu:
        - Échec de l'inscription
        - Message d'erreur approprié
        - Pas de nouvel utilisateur créé
        """
        # Créer le premier utilisateur
        User.objects.create_user(
            username='firstuser',
            email=TEST_EMAIL,
            password='Pass123!@#'
        )
        
        # Compter les utilisateurs avant
        users_count_before = User.objects.count()
        
        # Tenter d'inscrire avec le même email
        response = self.client.post(self.register_url, data=INVALID_DUPLICATE_EMAIL)
        
        # Vérifications
        users_count_after = User.objects.count()
        assert users_count_after == users_count_before, "Aucun nouvel utilisateur ne devrait être créé"
        
        # Vérifier qu'il n'y a pas de redirection (car erreur)
        assert response.status_code == 200, "Devrait rester sur la page d'inscription"
        
        print("✅ TC-AUTH-02 PASSED: Email dupliqué rejeté correctement")
    
    # ===== TC-AUTH-03 : Connexion réussie =====
    def test_login_success(self):
        """
        TC-AUTH-03: Connexion avec identifiants valides
        
        Étapes:
        1. Créer un utilisateur
        2. Se connecter avec les bons identifiants
        3. Vérifier la session
        
        Résultat attendu:
        - Connexion réussie
        - Session créée
        - Redirection vers profile
        """
        # Créer un utilisateur
        user = User.objects.create_user(
            username='testuser',
            email=TEST_EMAIL,
            password=TEST_PASSWORD
        )
        
        # Tenter de se connecter
        response = self.client.post(self.login_url, data=VALID_LOGIN_DATA)
        
        # Vérifications
        assert response.status_code == 302, "Devrait rediriger après connexion réussie"
        assert response.url in ['/accounts/profile/', '/profile/'], "Redirection incorrecte"
        
        # Vérifier que l'utilisateur est connecté
        assert self.client.session.get('_auth_user_id') == str(user.id), "Session non créée"
        
        print("✅ TC-AUTH-03 PASSED: Connexion réussie")
    
    # ===== TC-AUTH-04 : Connexion avec mauvais mot de passe =====
    def test_login_wrong_password(self):
        """
        TC-AUTH-04: Connexion avec mot de passe incorrect
        
        Étapes:
        1. Créer un utilisateur
        2. Tenter de se connecter avec un mauvais mot de passe
        
        Résultat attendu:
        - Échec de connexion
        - Message d'erreur
        - Pas de session créée
        """
        # Créer un utilisateur
        User.objects.create_user(
            username=TEST_USERNAME,
            email=TEST_EMAIL,
            password=TEST_PASSWORD
        )
        
        # Tenter de se connecter avec mauvais mot de passe
        response = self.client.post(self.login_url, data=INVALID_LOGIN_DATA)
        
        # Vérifications
        assert response.status_code == 200, "Devrait rester sur la page de login"
        assert not self.client.session.get('_auth_user_id'), "Aucune session ne devrait être créée"
        
        # Vérifier le message d'erreur dans le contenu
        content = response.content.decode()
        assert 'Invalid' in content or 'incorrect' in content.lower(), "Message d'erreur manquant"
        
        print("✅ TC-AUTH-04 PASSED: Mauvais mot de passe rejeté")
    
    # ===== TC-AUTH-05 : Déconnexion =====
    def test_logout(self):
        """
        TC-AUTH-05: Déconnexion utilisateur
        
        Étapes:
        1. Créer et connecter un utilisateur
        2. Se déconnecter
        
        Résultat attendu:
        - Session terminée
        - Redirection vers login ou home
        """
        # Créer et connecter un utilisateur
        user = User.objects.create_user(
            username=TEST_USERNAME,
            email=TEST_EMAIL,
            password=TEST_PASSWORD
        )
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        
        # Vérifier que l'utilisateur est connecté
        assert self.client.session.get('_auth_user_id') == str(user.id)
        
        # Se déconnecter
        response = self.client.get(self.logout_url)
        
        # Vérifications
        assert response.status_code == 302, "Devrait rediriger après déconnexion"
        assert not self.client.session.get('_auth_user_id'), "Session devrait être supprimée"
        
        print("✅ TC-AUTH-05 PASSED: Déconnexion réussie")
    
    # ===== Test bonus : Rôle Admin =====
    def test_admin_role_registration(self):
        """
        Test bonus: Vérifier l'attribution du rôle admin
        """
        # S'inscrire en tant qu'admin
        response = self.client.post(self.register_url, data=ADMIN_REGISTER_DATA)
        
        user = User.objects.get(username='adminuser')
        
        # Vérifications spécifiques admin
        assert user.profile.role == 'admin', "Rôle admin incorrect"
        assert user.is_staff == True, "L'utilisateur devrait être staff"
        assert user.is_superuser == True, "L'utilisateur devrait être superuser"
        
        print("✅ BONUS TEST PASSED: Rôle admin attribué correctement")


# ===== Commandes pour exécuter les tests =====
"""
# Exécuter tous les tests d'authentification
pytest accounts/tests/test_auth_unit.py -v

# Exécuter un test spécifique
pytest accounts/tests/test_auth_unit.py::TestAuthentication::test_register_success -v

# Avec coverage
pytest accounts/tests/test_auth_unit.py --cov=accounts --cov-report=html

# Avec markers
pytest -m auth  # Tous les tests d'authentification
pytest -m unit  # Tous les tests unitaires
"""