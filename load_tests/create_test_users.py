# load_tests/create_test_users.py
import os
import sys
import django

# Ajoute le chemin du projet Django (répertoire racine)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artify.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_test_users():
    """Crée les utilisateurs de test pour Locust"""
    User = get_user_model()
    
    test_users = [
        {"username": "testuser", "password": "TestPass123!@#"},
        {"username": "artist1", "password": "ArtistPass123!@#"},
        {"username": "creator2", "password": "CreatePass123!@#"},
    ]
    
    for user_data in test_users:
        user, created = User.objects.get_or_create(
            username=user_data["username"],
            defaults={
                "email": f"{user_data['username']}@artygen.com",
                "is_active": True
            }
        )
        if created:
            user.set_password(user_data["password"])
            user.save()
            print(f"✅ Utilisateur {user_data['username']} créé")
        else:
            # Met à jour le mot de passe si l'utilisateur existe déjà
            user.set_password(user_data["password"])
            user.save()
            print(f"🔧 Utilisateur {user_data['username']} mis à jour")

if __name__ == "__main__":
    create_test_users()
    print("🎉 Tous les utilisateurs de test sont prêts!")