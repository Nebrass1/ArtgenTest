#!/bin/bash

# Script pour exécuter les tests d'authentification
echo "🚀 Démarrage des tests d'authentification..."

# Activer l'environnement virtuel si nécessaire
if [ -f "../.venv/bin/activate" ]; then
    source ../.venv/bin/activate
    echo "✅ Environnement virtuel activé"
fi

# Aller dans le répertoire du projet Django
cd "$(dirname "$0")"

echo "📁 Répertoire actuel: $(pwd)"

# Exécuter les tests spécifiques
echo "🔧 Exécution des tests d'authentification..."

echo "1️⃣ Test des données (test_data.py)"
python manage.py test accounts.tests.test_data --verbosity=2

echo "2️⃣ Test unitaires d'authentification (test_auth_unit.py)"
python manage.py test accounts.tests.test_auth_unit --verbosity=2

echo "3️⃣ Test d'interface utilisateur (test_auth_ui.py)"
python manage.py test accounts.tests.test_auth_ui --verbosity=2

echo "✅ Tests d'authentification terminés!"