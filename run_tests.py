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

# Résultats attendus pour chaque test
EXPECTED_OUTPUTS = {
    "01_arithmetique_simple.c": "8\n2\n15\n1\n",
    "02_comparaisons.c": "1\n0\n0\n1\n1\n1\n",
    "03_operateurs_unaires.c": "-5\n5\n10\n",
    "04_expressions_complexes.c": "14\n20\n14\n15\n",
    "05_if_simple.c": "100\n100\n",
    "06_if_else.c": "200\n300\n",
    "07_while_simple.c": "10\n5\n",
    "08_while_imbriques.c": "6\n",
    "09_pointeurs_simple.c": "42\n100\n",
    "10_tableaux_postfixe.c": "10\n20\n30\n",
    "11_tableaux_prefixe.c": "100\n200\n300\n",
    "12_fonctions_simple.c": "8\n",
    "13_fonctions_recursives.c": "120\n6\n",
    "14_operateurs_logiques.c": "0\n1\n0\n1\n",
    "15_variables_multiples.c": "1\n2\n3\n4\n5\n10\n",
    "16_if_imbriques.c": "1\n",
    "17_if_while_imbriques.c": "6\n",
    "18_while_if_imbriques.c": "3\n",
    "19_complex_nesting.c": "12\n",
    "20_mixed_nesting.c": "16\n",
    "21_do_while_simple.c": "10\n",
    "22_break_continue.c": "9\n",
    "23_pointeurs_tableaux.c": "42\n100\n",
    "24_for_simple.c": "10\n",
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
            
            actual_output = result.stdout
            expected_output = EXPECTED_OUTPUTS.get(test_file.name, "")
            
            print(f"{GREEN}Sortie MSM:{RESET}")
            print(actual_output)
            if result.stderr:
                print(f"{YELLOW}Erreurs:{RESET}")
                print(result.stderr)
            
            # Vérifier la sortie
            if expected_output and actual_output == expected_output:
                print(f"{GREEN}✓ Sortie correcte{RESET}")
                return True
            elif expected_output:
                print(f"{RED}✗ Sortie incorrecte - Attendu:{RESET}")
                print(repr(expected_output))
                print(f"{RED}Obtenu:{RESET}")
                print(repr(actual_output))
                return False
            else:
                print(f"{YELLOW}! Pas de résultat attendu défini{RESET}")
                return True  # Ne pas échouer si pas défini
        else:
            print(f"{YELLOW}! MSM non trouvé, skip exécution{RESET}")
            return False
        
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
        print(f"\n{GREEN} Tous les tests sont passés !{RESET}")
    else:
        print(f"\n{YELLOW}  {failed} test(s) ont échoué{RESET}")

if __name__ == "__main__":
    main()
