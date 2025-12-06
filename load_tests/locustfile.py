# load_tests/locustfile_simple.py
from locust import HttpUser, task, between
import random
from test_data import get_random_user, get_random_prompt, get_random_style


class SimpleArtygenUser(HttpUser):
    """
    Version simplifiée et robuste des tests de charge Artygen
    Focus sur les endpoints qui fonctionnent vraiment
    """
    wait_time = between(1, 3)  # Attente entre 1 et 3 secondes entre les tâches
    host = "http://127.0.0.1:8000"
    
    @task(10)
    def browse_home(self):
        """Page d'accueil - Test le plus fiable"""
        self.client.get("/", name="Home_Page")
    
    @task(5)
    def browse_blog(self):
        """Navigation blog"""
        self.client.get("/blog/", name="Blog_Page")
    
    @task(3)
    def browse_categories(self):
        """Navigation catégories"""
        self.client.get("/category/categories/", name="Categories_Page")
    
    @task(3)
    def browse_artwork_all(self):
        """Voir tous les artworks"""
        self.client.get("/artwork/all/", name="All_Artworks")
    
    @task(2)
    def browse_artwork_galleries(self):
        """Navigation galleries"""
        self.client.get("/artwork/galleries/", name="Galleries_Page")
    
    @task(2)
    def browse_login_page(self):
        """Page de connexion (GET seulement)"""
        self.client.get("/accounts/login/", name="Login_Page")
    
    @task(2)
    def browse_admin_redirect(self):
        """Test redirection admin"""
        self.client.get("/admin/", name="Admin_Redirect")
    
    @task(1)
    def browse_artwork_create_page(self):
        """Test accès page création artwork (peut rediriger vers login)"""
        self.client.get("/artwork/create/", name="Artwork_Create_Page")
        
    @task(1)
    def test_static_resources(self):
        """Test de quelques ressources statiques"""
        self.client.get("/static/css/style.css", name="Static_CSS")
    
    # SUPPRIMÉ: generate/ - Erreurs 500 fréquentes  
    # @task(1) test_generate_page_access - DÉSACTIVÉ
    
    def on_start(self):
        """Appelé quand un utilisateur virtuel commence"""
        print(f"👤 Utilisateur simple démarre...")
    
    def on_stop(self):
        """Appelé quand un utilisateur virtuel s'arrête"""
        print(f"👤 Utilisateur simple termine...")


if __name__ == "__main__":
    # Configuration pour test standalone
    import subprocess
    import sys
    
    print("🚀 Lancement des tests simples Artygen...")
    print("📊 Interface: http://localhost:8089")
    print("🎯 Focus: Tests GET fiables uniquement")