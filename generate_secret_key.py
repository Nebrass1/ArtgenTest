#!/usr/bin/env python
"""
Generate a new SECRET_KEY for Django production deployment
"""
from django.core.management.utils import get_random_secret_key

if __name__ == "__main__":
    secret_key = get_random_secret_key()
    print("\n" + "="*60)
    print("🔐 NOUVELLE SECRET_KEY GÉNÉRÉE")
    print("="*60)
    print(f"\n{secret_key}\n")
    print("="*60)
    print("⚠️  Copiez cette clé dans vos variables d'environnement Render")
    print("="*60 + "\n")
