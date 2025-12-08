#!/usr/bin/env python3
"""
Audit du code MathCopain
Vérifie les imports, fonctions manquantes et erreurs potentielles
"""

import ast
import os
from collections import defaultdict

def analyze_file(filepath):
    """Analyse un fichier Python"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        tree = ast.parse(content, filepath)
    except SyntaxError as e:
        return {'error': f'Syntax error at line {e.lineno}: {e.msg}'}

    imports = []
    functions_defined = []
    functions_called = []

    for node in ast.walk(tree):
        # Imports
        if isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imports.append(f"{module}.{alias.name}")

        # Function definitions
        elif isinstance(node, ast.FunctionDef):
            functions_defined.append(node.name)

        # Function calls
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                functions_called.append(node.func.id)

    return {
        'imports': imports,
        'functions_defined': functions_defined,
        'functions_called': set(functions_called),
        'error': None
    }

def main():
    files_to_check = [
        'ui/math_sections.py',
        'ui/exercise_sections.py',
        'app.py',
        'utilisateur.py'
    ]

    results = {}
    for filepath in files_to_check:
        if os.path.exists(filepath):
            results[filepath] = analyze_file(filepath)
        else:
            print(f"⚠️  File not found: {filepath}")

    print("\n" + "="*60)
    print("📋 AUDIT DU CODE MATHCOPAIN")
    print("="*60 + "\n")

    for filepath, data in results.items():
        if data.get('error'):
            print(f"❌ {filepath}")
            print(f"   Error: {data['error']}\n")
        else:
            print(f"✅ {filepath}")
            print(f"   Functions defined: {len(data['functions_defined'])}")
            print(f"   Unique functions called: {len(data['functions_called'])}")
            print(f"   Imports: {len(data['imports'])}\n")

    # Check for auto_save_profil
    print("\n" + "-"*60)
    print("🔍 Vérification de auto_save_profil:")
    print("-"*60)

    for filepath, data in results.items():
        if 'auto_save_profil' in data.get('functions_defined', []):
            print(f"✅ Défini dans: {filepath}")
        if 'auto_save_profil' in data.get('functions_called', set()):
            print(f"📞 Appelé dans: {filepath}")
            # Check if imported
            has_import = any('auto_save_profil' in imp for imp in data.get('imports', []))
            if has_import:
                print(f"   ✅ Importé correctement")
            else:
                print(f"   ⚠️  NON IMPORTÉ - Erreur potentielle!")

    print("\n" + "="*60)
    print("Audit terminé")
    print("="*60)

if __name__ == '__main__':
    main()
