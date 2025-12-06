# load_tests/test_data.py
import random

# Données pour les tests de charge
USERS = [
    {"username": "testuser", "password": "TestPass123!@#"},
    {"username": "artist1", "password": "ArtistPass123!@#"},
    {"username": "creator2", "password": "CreatePass123!@#"},
]

PROMPTS = [
    "A mystical forest with glowing mushrooms and fairies",
    "Cyberpunk cityscape at night with neon lights",
    "Abstract geometric patterns in vibrant colors",
    "Portrait of a robot with human emotions",
    "Surreal landscape with floating islands and waterfalls",
    "Fantasy castle in the clouds during sunset",
    "Steampunk machinery with intricate details",
    "Ocean depths with bioluminescent creatures",
    "Digital art of a cosmic nebula explosion",
    "Minimalist landscape with mountains and lakes"
]

STYLES = [
    "Digital Art", "Cyberpunk", "Abstract", "Realistic", 
    "Anime", "Fantasy", "Steampunk", "Minimalist",
    "Impressionist", "Surreal"
]

def get_random_user():
    """Retourne un utilisateur aléatoire pour les tests"""
    return random.choice(USERS)

def get_random_prompt():
    """Retourne un prompt aléatoire"""
    return random.choice(PROMPTS)

def get_random_style():
    """Retourne un style aléatoire"""
    return random.choice(STYLES)