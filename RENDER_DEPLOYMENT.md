# 🚀 Déploiement sur Render - Guide Complet

## ✅ Fichiers de Configuration Créés

- ✅ `requirements.txt` - Dépendances Python
- ✅ `build.sh` - Script de build pour Render
- ✅ `settings.py` - Modifié pour production
- ✅ `env.render.example` - Variables d'environnement

## 📋 Étapes de Déploiement

### 1️⃣ Créer une Base de Données PostgreSQL sur Render

1. Allez sur https://render.com/
2. Cliquez sur **"New +"** → **"PostgreSQL"**
3. Configuration :
   - **Name** : `artygen-db`
   - **Region** : Frankfurt (ou plus proche)
   - **Plan** : **Free**
4. Cliquez sur **"Create Database"**
5. ⚠️ **IMPORTANT** : Copiez l'**Internal Database URL**

### 2️⃣ Créer le Web Service

1. Cliquez sur **"New +"** → **"Web Service"**
2. Connectez votre repository GitHub
3. Configuration :
   - **Name** : `artygen`
   - **Region** : Même que votre DB
   - **Branch** : `main`
   - **Runtime** : **Python 3**
   - **Build Command** : `./build.sh`
   - **Start Command** : `gunicorn artify.wsgi:application`

### 3️⃣ Variables d'Environnement

Cliquez sur **"Advanced"** puis ajoutez :

```bash
SECRET_KEY = [générez une clé avec la commande ci-dessous]
DEBUG = False
DATABASE_URL = [collez l'Internal Database URL de l'étape 1]
PYTHON_VERSION = 3.11.0
ALLOWED_HOSTS = votre-app.onrender.com
GEMINI_API_KEY = votre-cle-gemini
OPENAI_API_KEY = votre-cle-openai
```

#### Générer une SECRET_KEY :
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4️⃣ Déployer

1. Cliquez sur **"Create Web Service"**
2. Attendez 5-10 minutes (suivez les logs)
3. Votre app sera accessible sur : `https://votre-app.onrender.com`

## 🔧 Commandes Utiles

### Créer un superuser (via Shell Render)
```bash
python manage.py createsuperuser
```

### Collecter les fichiers statiques localement
```bash
python manage.py collectstatic --no-input
```

### Tester le build localement
```bash
bash build.sh
```

## ⚠️ Limitations Plan Gratuit

- Service s'endort après 15 min d'inactivité
- Premier chargement lent (~30 sec après inactivité)
- 750 heures/mois
- Base de données expire après 90 jours

## 🔄 Mises à Jour

Render redéploie automatiquement à chaque push sur `main` :
```bash
git add .
git commit -m "Mise à jour"
git push origin main
```

## 📝 Notes Importantes

1. ✅ WhiteNoise gère les fichiers statiques automatiquement
2. ✅ PostgreSQL utilisé en production, SQLite en local
3. ✅ DEBUG=False en production
4. ✅ HTTPS automatique avec Render

## 🆘 Dépannage

### Erreur "collectstatic" :
```bash
python manage.py collectstatic --no-input --clear
```

### Voir les logs :
Dashboard Render → Votre Service → Onglet "Logs"

### Redéployer manuellement :
Dashboard Render → Votre Service → "Manual Deploy" → "Deploy latest commit"
