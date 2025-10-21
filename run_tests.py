#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test automatisé pour le compilateur PyComp
"""

import os
import subprocess
import shutil
from pathlib import Path

# Chemins
TESTS_DIR = Path("tests")
TEST_FILE = Path("test.c")
OUT_MSM = Path("out.msm")
MSM_EXECUTABLE = Path("../msm/msm")

# Couleurs pour le terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def run_test(test_file):
    """Execute un test : copie le fichier, compile et exécute"""
    test_name = test_file.stem
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Test: {test_name}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    try:
        # 1. Copier le fichier de test dans test.c
        shutil.copy(test_file, TEST_FILE)
        print(f"✓ Fichier copié: {test_file.name}")
        
        # 2. Compiler avec Python
        print(f"\n{YELLOW}Compilation...{RESET}")
        result = subprocess.run(
            ["python3", "main.py"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            print(f"{RED}✗ Erreur de compilation:{RESET}")
            print(result.stderr)
            return False
        
        print(result.stdout)
        
        # 3. Vérifier que out.msm existe
        if not OUT_MSM.exists():
            print(f"{RED}✗ Fichier out.msm non généré{RESET}")
            return False
        
        print(f"{GREEN}✓ Compilation réussie{RESET}")
        
        # 4. Exécuter avec MSM
        if MSM_EXECUTABLE.exists():
            print(f"\n{YELLOW}Exécution MSM...{RESET}")
            result = subprocess.run(
                [str(MSM_EXECUTABLE), str(OUT_MSM)],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            print(f"{GREEN}Sortie MSM:{RESET}")
            print(result.stdout)
            if result.stderr:
                print(f"{YELLOW}Erreurs:{RESET}")
                print(result.stderr)
        else:
            print(f"{YELLOW}! MSM non trouvé, skip exécution{RESET}")
        
        return True
        
    except subprocess.TimeoutExpired:
        print(f"{RED}✗ Timeout dépassé{RESET}")
        return False
    except Exception as e:
        print(f"{RED}✗ Erreur: {e}{RESET}")
        return False

def main():
    """Lance tous les tests"""
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}BATTERIE DE TESTS - COMPILATEUR PyComp{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    # Récupérer tous les fichiers .c dans tests/
    test_files = sorted(TESTS_DIR.glob("*.c"))
    
    if not test_files:
        print(f"{RED}Aucun fichier de test trouvé dans {TESTS_DIR}{RESET}")
        return
    
    results = {}
    
    for test_file in test_files:
        success = run_test(test_file)
        results[test_file.name] = success
    
    # Résumé final
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}RÉSUMÉ DES TESTS{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for test_name, success in results.items():
        status = f"{GREEN}✓ PASS{RESET}" if success else f"{RED}✗ FAIL{RESET}"
        print(f"{status} - {test_name}")
    
    print(f"\n{BLUE}Total: {total} | {GREEN}Réussis: {passed}{RESET} | {RED}Échoués: {failed}{RESET}")
    
    if failed == 0:
        print(f"\n{GREEN}🎉 Tous les tests sont passés !{RESET}")
    else:
        print(f"\n{YELLOW}⚠️  {failed} test(s) ont échoué{RESET}")

if __name__ == "__main__":
    main()
