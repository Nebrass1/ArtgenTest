import sys
import os
import django

# Configuration du chemin
project_path = r"C:\Users\neebr\OneDrive\Bureau\Artygen - Test\artygen"
sys.path.insert(0, project_path)

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artify.settings')

# Initialiser Django
try:
    django.setup()
    print("✅ Django configuré avec succès!")
    
    # Test d'import
    try:
        from generator import views
        print("✅ Generator views importé!")
        print(f"Fonctions disponibles: {[f for f in dir(views) if not f.startswith('_')]}")
    except Exception as e:
        print(f"❌ Erreur import: {e}")
    
    # Lancer pydoc
    import pydoc
    print("🚀 Lancement de pydoc sur le port 8080...")
    pydoc.cli()
    
except Exception as e:
    print(f"❌ Erreur configuration: {e}")
    import traceback
    traceback.print_exc()
    input("Appuyez sur Entrée pour quitter...")