# 🔧 FIX: Conflits de Dépendances Render

## ❌ Erreur Identifiée

```
ERROR: Cannot install requirements because these package versions have conflicting dependencies.
The conflict is caused by:
    requests==2.32.5
    locust 2.42.3 depends on requests<2.32.5 and >=2.32.2
```

### Cause
- `locust==2.42.3` demande `requests<2.32.5`
- Nous avions spécifié `requests==2.32.5`
- **Conflit d'incompatibilité**

---

## ✅ Solutions

### Option 1: Utiliser requests==2.32.2 (RECOMMANDÉ)
```bash
# Dans requirements.txt, remplacez:
requests==2.32.5
# Par:
requests==2.32.2
```

**Avantages:**
- Compatible avec Locust
- Compatible avec toutes les autres dépendances
- Version stable et sécurisée

### Option 2: Utiliser requirements-production.txt
```bash
# Utilisez la version allégée sans Jupyter/Testing:
cp requirements-production.txt requirements.txt
```

**Avantages:**
- Réduit de 254 à 50 dépendances
- Plus rapide à installer
- Aucune dépendance de développement
- Conforme à la production

---

## 🚀 Actions à Prendre

### 1. **Sur votre machine locale:**

**Option A - Correction minimale:**
```bash
cd Artygen
# Modifier requirements.txt: requests==2.32.2
git add requirements.txt
git commit -m "Fix: Change requests from 2.32.5 to 2.32.2 for Locust compatibility"
git push origin main
```

**Option B - Version production complète:**
```bash
cd Artygen
# Utiliser la version production optimisée
cp requirements-production.txt requirements.txt
git add requirements.txt requirements-production.txt
git commit -m "Use optimized production requirements for Render"
git push origin main
```

### 2. **Sur Render:**
- Attendez que le push soit visible
- Cliquez **"Manual Deploy"**
- Sélectionnez branche **"main"**
- Le build devrait réussir ✅

---

## 📋 Dépendances par Catégorie

### Essentielles (Production)
```
Django==5.2.7
gunicorn==23.0.0
whitenoise==6.11.0
dj-database-url==3.0.1
psycopg2-binary==2.9.11
requests==2.32.2  ← VERSION CORRIGÉE
```

### API & Framework
```
djangorestframework==3.16.1
django-cors-headers==4.9.0
djangorestframework_simplejwt==5.5.1
```

### AI/ML
```
google-generativeai==0.8.5
openai==2.8.1
```

### Data Science
```
pandas==2.2.3
numpy==2.2.6
scikit-learn==1.6.1
```

---

## ⚠️ Dépendances Supprimées dans requirements-production.txt

- ❌ Jupyter (jupyterlab, notebook, ipython)
- ❌ Testing (pytest, coverage, locust)
- ❌ Dev tools (ipdb, debugpy, Cython)
- ❌ Build tools (setuptools, wheel)
- ❌ Linters (flake8, pylint, black)

Ces outils sont pour le développement, **pas pour la production**.

---

## ✅ Vérification

Après le déploiement, vérifiez:

```bash
# Voir les dépendances installées:
pip list

# Vérifier que l'app démarre:
gunicorn artify.wsgi:application --bind 0.0.0.0:8000

# Tester les imports:
python -c "import django; import requests; print('OK')"
```

---

## 💡 Astuce pour Futurs Déploiements

Toujours spécifier les versions de manière flexible en production:

```
# Bon:
requests>=2.32.2,<3.0

# À éviter:
requests==2.32.5
```

Cela laisse de la latitude pour les corrections de bugs/sécurité.
