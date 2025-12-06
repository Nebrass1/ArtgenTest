"""
Données de test pour l'authentification
"""

from .test_constants import TEST_PASSWORD, TEST_EMAIL, TEST_USERNAME

# Données valides pour l'inscription
VALID_REGISTER_DATA = {
    'username': TEST_USERNAME,
    'email': TEST_EMAIL,
    'first_name': 'Test',
    'last_name': 'User',
    'password1': TEST_PASSWORD,
    'password2': TEST_PASSWORD,
    'cin': '12345678',
    'birthdate': '1995-01-15',
    'role': 'user',
    'art_style': 'Abstract Digital Art',
    'art_interests': 'nature, colors, emotions',
    'generate_bio': True
}

# Données invalides (email existant)
INVALID_DUPLICATE_EMAIL = {
    'username': 'testuser2',
    'email': TEST_EMAIL,  # Déjà utilisé
    'first_name': 'Test2',
    'last_name': 'User2',
    'password1': 'TestPass123!@#',
    'password2': 'TestPass123!@#',
    'cin': '87654321',
    'birthdate': '1996-05-20',
    'role': 'user'
}

# Données invalides (mots de passe différents)
INVALID_PASSWORD_MISMATCH = {
    'username': 'testuser3',
    'email': 'testuser3@artygen.com',
    'first_name': 'Test3',
    'last_name': 'User3',
    'password1': TEST_PASSWORD,
    'password2': 'DifferentPass456!@#',  # Différent
    'cin': '11223344',
    'birthdate': '1997-03-10',
    'role': 'user'
}

# Données de connexion valides
VALID_LOGIN_DATA = {
    'username': TEST_USERNAME,
    'password': TEST_PASSWORD
}

# Données de connexion invalides
INVALID_LOGIN_DATA = {
    'username': TEST_USERNAME,
    'password': 'WrongPassword123'
}

# Données pour un admin
ADMIN_REGISTER_DATA = {
    'username': 'adminuser',
    'email': 'admin@artygen.com',
    'first_name': 'Admin',
    'last_name': 'User',
    'password1': TEST_PASSWORD,
    'password2': TEST_PASSWORD,
    'cin': '99887766',
    'birthdate': '1990-08-25',
    'role': 'admin'
}

# Données pour edit profile
EDIT_PROFILE_DATA = {
    'bio': 'Je suis un artiste passionné par l\'art numérique',
    'art_style': 'Digital Abstract',
    'art_interests': 'technology, futurism, colors'
}