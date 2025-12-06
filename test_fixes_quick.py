#!/usr/bin/env python3
"""
Test rapide pour valider les corrections SonarQube sans Django
"""

import ast
import os
from pathlib import Path


def test_constants_defined():
    """Test que les constantes de template sont définies"""
    print("🔍 Testing template constants...")
    
    category_result = _test_category_constants()
    generator_result = _test_generator_constants()
    
    return category_result and generator_result


def _test_category_constants():
    """Test constants in category/views.py"""
    category_file = Path("category/views.py")
    if not category_file.exists():
        print("  ❌ category/views.py not found")
        return False
    
    content = category_file.read_text(encoding='utf-8')
    
    if "SUBCATEGORY_FORM_TEMPLATE = 'subcategory_form.html'" not in content:
        print("  ❌ SUBCATEGORY_FORM_TEMPLATE constant not found")
        return False
    
    print("  ✅ SUBCATEGORY_FORM_TEMPLATE constant defined")
    
    if content.count("'subcategory_form.html'") <= 1:
        print("  ✅ No more duplicate 'subcategory_form.html' literals")
        return True
    else:
        print("  ❌ Still has duplicate 'subcategory_form.html' literals")
        return False


def _test_generator_constants():
    """Test constants in generator/views.py"""
    generator_file = Path("generator/views.py")
    if not generator_file.exists():
        print("  ❌ generator/views.py not found")
        return False
    
    content = generator_file.read_text(encoding='utf-8')
    
    if "GENERATE_IMAGE_TEMPLATE = 'generate_image.html'" not in content:
        print("  ❌ GENERATE_IMAGE_TEMPLATE constant not found")
        return False
    
    print("  ✅ GENERATE_IMAGE_TEMPLATE constant defined")
    
    if content.count("'generate_image.html'") <= 1:
        print("  ✅ No more duplicate 'generate_image.html' literals")
        return True
    else:
        print("  ❌ Still has duplicate 'generate_image.html' literals")
        return False


def test_cognitive_complexity():
    """Test approximatif de la complexité cognitive"""
    print("\n🧠 Testing cognitive complexity...")
    
    category_result = _test_category_complexity()
    return category_result


def _test_category_complexity():
    """Test complexity in category/views.py"""
    category_file = Path("category/views.py")
    if not category_file.exists():
        print("  ❌ category/views.py not found")
        return False
    
    content = category_file.read_text(encoding='utf-8')
    
    # Vérifier les fonctions helper
    helper_result = _test_helper_functions(content)
    if not helper_result:
        return False
    
    # Vérifier la complexité de get_art_subcategories
    complexity_result = _test_function_complexity(content)
    return complexity_result


def _test_helper_functions(content):
    """Test that helper functions exist"""
    helper_functions = [
        '_configure_gemini_api',
        '_create_subcategory_prompt', 
        '_parse_subcategory_response'
    ]
    
    for func in helper_functions:
        if f"def {func}(" in content:
            print(f"  ✅ Helper function {func} exists")
        else:
            print(f"  ❌ Helper function {func} missing")
            return False
    
    return True


def _test_function_complexity(content):
    """Test complexity of get_art_subcategories function"""
    if "def get_art_subcategories(" not in content:
        print("  ❌ get_art_subcategories function not found")
        return False
    
    func_start = content.find("def get_art_subcategories(")
    func_end = content.find("\ndef ", func_start + 1)
    if func_end == -1:
        func_end = len(content)
    
    func_content = content[func_start:func_end]
    
    # Compter les structures de contrôle complexes
    complexity_indicators = [
        "for line in lines:",
        "if not line:",
        "if line.startswith",
        "if ':' in line:",
        "if subcategory and"
    ]
    
    found_indicators = sum(1 for indicator in complexity_indicators if indicator in func_content)
    
    if found_indicators <= 3:
        print(f"  ✅ get_art_subcategories complexity reduced (indicators: {found_indicators})")
        return True
    else:
        print(f"  ❌ get_art_subcategories still complex (indicators: {found_indicators})")
        return False


def run_all_tests():
    """Execute all validation tests"""
    print("🎯 VALIDATION RAPIDE DES CORRECTIONS SONARQUBE")
    print("="*50)
    
    os.chdir("C:\\Users\\neebr\\OneDrive\\Bureau\\Artygen - Test\\Artygen")
    
    success = True
    success &= test_constants_defined()
    success &= test_cognitive_complexity()
    
    return success


def display_results(success):
    """Display test results"""
    print("\n" + "="*50)
    if success:
        print("🎉 TOUTES LES CORRECTIONS VALIDÉES AVEC SUCCÈS!")
        print("✅ Constantes de template créées")
        print("✅ Littéraux dupliqués éliminés") 
        print("✅ Complexité cognitive réduite")
        print("\n🚀 Le projet est prêt pour SonarQube!")
    else:
        print("❌ Certaines corrections nécessitent encore du travail")


def main():
    """Fonction principale de test"""
    success = run_all_tests()
    display_results(success)
    return success


if __name__ == "__main__":
    main()