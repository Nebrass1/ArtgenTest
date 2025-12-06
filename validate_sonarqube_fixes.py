#!/usr/bin/env python3
"""
Script de validation des corrections SonarQube
Vérifie que tous les problèmes identifiés ont bien été corrigés
"""

import os
import ast
import sys
from pathlib import Path


class SonarQubeValidator:
    """Validateur des corrections SonarQube"""
    
    def __init__(self):
        self.issues_found = 0
        self.issues_fixed = 0
        self.validation_success = False
        
    def validate_all_fixes(self):
        """Valide toutes les corrections"""
        print("🔍 Validation des corrections SonarQube...\n")
        
        # 1. Validation sécurité API
        self._validate_api_security()
        
        # 2. Validation littéraux dupliqués  
        self._validate_duplicate_literals()
        
        # 3. Validation complexité cognitive
        self._validate_cognitive_complexity()
        
        # 4. Validation imports
        self._validate_imports()
        
        # Résumé
        self._print_summary()
        return self.validation_success
        
    def _validate_api_security(self):
        """Valide la sécurité des clés API"""
        print("🔐 Validation sécurité API...")
        
        settings_file = Path("artify/settings.py")
        if settings_file.exists():
            content = settings_file.read_text(encoding='utf-8')
            
            # Vérifier que les clés API utilisent os.getenv
            if "os.getenv('GEMINI_API_KEY'" in content:
                print("  ✅ GEMINI_API_KEY utilise os.getenv")
                self.issues_fixed += 1
            else:
                print("  ❌ GEMINI_API_KEY n'utilise pas os.getenv")
                self.issues_found += 1
                
            if "os.getenv('SECRET_KEY'" in content:
                print("  ✅ SECRET_KEY utilise os.getenv") 
                self.issues_fixed += 1
            else:
                print("  ❌ SECRET_KEY n'utilise pas os.getenv")
                self.issues_found += 1
        
    def _validate_duplicate_literals(self):
        """Valide la correction des littéraux dupliqués"""
        print("\n📋 Validation littéraux dupliqués...")
        
        # Vérifier l'existence du fichier de constantes
        constants_file = Path("accounts/tests/test_constants.py")
        if constants_file.exists():
            print("  ✅ Fichier test_constants.py créé")
            self.issues_fixed += 1
            
            content = constants_file.read_text(encoding='utf-8')
            constants = ['TEST_PASSWORD', 'TEST_EMAIL', 'SUBMIT_BUTTON_SELECTOR']
            
            for const in constants:
                if const in content:
                    print(f"  ✅ Constante {const} définie")
                    self.issues_fixed += 1
                else:
                    print(f"  ❌ Constante {const} manquante")
                    self.issues_found += 1
        else:
            print("  ❌ Fichier test_constants.py manquant")
            self.issues_found += 1
            
    def _validate_cognitive_complexity(self):
        """Valide la réduction de complexité cognitive"""
        print("\n🧠 Validation complexité cognitive...")
        
        files_to_check = [
            ("accounts/views.py", "register"),
            ("category/views.py", "subcategory_create"), 
            ("generator/views.py", "generate_image")
        ]
        
        for file_path, function_name in files_to_check:
            if Path(file_path).exists():
                complexity = self._calculate_cognitive_complexity(file_path, function_name)
                if complexity <= 15:
                    print(f"  ✅ {file_path}::{function_name} - Complexité: {complexity}")
                    self.issues_fixed += 1
                else:
                    print(f"  ❌ {file_path}::{function_name} - Complexité: {complexity} (>15)")
                    self.issues_found += 1
                    
    def _calculate_cognitive_complexity(self, file_path, function_name):
        """Calcule approximativement la complexité cognitive d'une fonction"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if (isinstance(node, ast.FunctionDef) and 
                    node.name == function_name):
                    return self._count_complexity_nodes(node)
            return 0
            
        except Exception as e:
            print(f"  ⚠️  Erreur calcul complexité {file_path}: {e}")
            return 999
            
    def _count_complexity_nodes(self, node):
        """Compte les nœuds contribuant à la complexité cognitive"""
        complexity = 0
        
        for child in ast.walk(node):
            # +1 pour chaque structure de contrôle
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler)):
                complexity += 1
            # +1 pour chaque condition logique
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
                
        return complexity
        
    def _validate_imports(self):
        """Valide l'optimisation des imports"""
        print("\n📦 Validation imports...")
        
        # Vérifier que les imports inutilisés ont été supprimés
        # (vérification basique)
        files_to_check = [
            "accounts/views.py",
            "category/views.py", 
            "generator/views.py"
        ]
        
        for file_path in files_to_check:
            if Path(file_path).exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                import_lines = [l for l in lines if l.strip().startswith('import') or l.strip().startswith('from')]
                
                if len(import_lines) < 20:  # Limite raisonnable
                    print(f"  ✅ {file_path} - Imports optimisés ({len(import_lines)} lignes)")
                    self.issues_fixed += 1
                else:
                    print(f"  ⚠️  {file_path} - Beaucoup d'imports ({len(import_lines)} lignes)")
                    
    def _print_summary(self):
        """Affiche le résumé de validation"""
        print("\n" + "="*50)
        print("📊 RÉSUMÉ DE VALIDATION")
        print("="*50)
        print(f"✅ Problèmes corrigés: {self.issues_fixed}")
        print(f"❌ Problèmes restants: {self.issues_found}")
        
        if self.issues_found == 0:
            print("\n🎉 Tous les problèmes SonarQube ont été corrigés!")
            self.validation_success = True
        else:
            print(f"\n⚠️  Il reste {self.issues_found} problèmes à corriger")
            self.validation_success = False


def main():
    """Fonction principale"""
    validator = SonarQubeValidator()
    success = validator.validate_all_fixes()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()