# Batterie de Tests - Compilateur PyComp

Ce dossier contient une suite complète de tests pour valider toutes les fonctionnalités du compilateur PyComp.

## Liste des Tests

### Tests de Base (01-04)

#### **01_arithmetique_simple.c**
- **Objectif**: Valider les opérations arithmétiques de base
- **Fonctionnalités testées**: `+`, `-`, `*`, `/`
- **Résultats attendus**: 
  - Addition: 8
  - Soustraction: 2
  - Multiplication: 15
  - Division: 1

#### **02_comparaisons.c**
- **Fonctionnalités testées**: `>`, `<`, `==`, `!=`, `>=`, `<=`
- **Résultats attendus**: 1, 0, 0, 1, 1, 1

#### **03_operateurs_unaires.c**
- **Fonctionnalités testées**: `-x`, `+x`
- **Résultats attendus**: -5, 5, 10

#### **04_expressions_complexes.c**
- **Fonctionnalités testées**: Expressions avec parenthèses et priorités
- **Résultats attendus**: 
  - 2 + 3 * 4 = 14
  - (2 + 3) * 4 = 20
  - 2 * 3 + 4 * 2 = 14
  - (2 + 3) * (4 - 1) = 15

---

### Tests de Structures de Contrôle (05-08)

#### **05_if_simple.c**
- **Fonctionnalités testées**: `if` sans `else`
- **Résultats attendus**: 100, 100

#### **06_if_else.c**
- **Fonctionnalités testées**: `if-else`
- **Résultats attendus**: 200, 300

#### **07_while_simple.c**
- **Fonctionnalités testées**: `while`
- **Résultats attendus**: 
  - Somme 0+1+2+3+4 = 10
  - Compteur final = 5

#### **08_while_imbriques.c**
- **Fonctionnalités testées**: `while` dans `while`
- **Résultats attendus**: Compteur = 6 (3×2 itérations)

---

### Tests de Pointeurs et Tableaux (09-11)

#### **09_pointeurs_simple.c**
- **Fonctionnalités testées**: `&` (adresse), `*` (déréférencement)
- **Résultats attendus**: 
  - Lecture via pointeur: 42
  - Écriture via pointeur: 100

#### **10_tableaux_postfixe.c**
- **Fonctionnalités testées**: `arr[index]`
- **Résultats attendus**: 
  - arr[0] = 10
  - arr[1] = 20
  - arr[2] = 30

#### **11_tableaux_prefixe.c**
- **Fonctionnalités testées**: `[index]arr`
- **Résultats attendus**: 
  - [0]arr = 100
  - [1]arr = 200
  - [2]arr = 300

---

### Tests de Fonctions (12-13)

#### **12_fonctions_simple.c**
- **Fonctionnalités testées**: Définition et appel de fonction
- **Résultats attendus**: Fonction `add(5, 3)` = 8

#### **13_fonctions_recursives.c**
- **Fonctionnalités testées**: Fonction récursive (factorielle)
- **Résultats attendus**: 
  - factorial(5) = 120
  - factorial(3) = 6

---

### Tests Avancés (14-21)

#### **14_operateurs_logiques.c**
- **Fonctionnalités testées**: `&&`, `||`, `!`
- **Résultats attendus**: 0, 1, 0, 1

#### **15_variables_multiples.c**
- **Fonctionnalités testées**: Déclarations multiples, affectations
- **Résultats attendus**: 1, 2, 3, 4, 5, 10

#### **16_if_imbriques.c**
- **Fonctionnalités testées**: `if` dans `if` avec `else`
- **Résultats attendus**: 1

#### **17_if_while_imbriques.c**
- **Fonctionnalités testées**: `if` à l'intérieur d'une boucle `while`
- **Résultats attendus**: 6

#### **18_while_if_imbriques.c**
- **Objectif**: Tester while imbriqué dans if
- **Fonctionnalités testées**: `while` à l'intérieur d'un `if`
- **Résultats attendus**: 3

#### **19_complex_nesting.c**
- **Fonctionnalités testées**: `while` avec `if-else` contenant une autre boucle `while`
- **Résultats attendus**: 12

#### **20_mixed_nesting.c**
- **Fonctionnalités testées**: `while` avec `if-else`, contenant une autre boucle `while` dans une branche
- **Résultats attendus**: 16

#### **21_do_while_simple.c**
- **Fonctionnalités testées**: `do-while` (boucle exécutée au moins une fois)
- **Résultats attendus**: 10

#### **22_break_continue.c**
- **Fonctionnalités testées**: `break` et `continue` dans une boucle while
- **Résultats attendus**: 9

#### **23_pointeurs_tableaux.c**
- **Fonctionnalités testées**: Tester la combinaison pointeurs et tableaux
- **Résultats attendus**: 42, 100

#### **24_for_simple.c**
- **Fonctionnalités testées**: `for(init; cond; incr) body`
- **Résultats attendus**: 10

## Utilisation

### Lancer tous les tests
```bash
python run_tests.py
```

### Lancer un test spécifique
```bash
python run_tests.py tests/01_arithmetique_simple.c
```

### Lancer le compilateur sur un fichier
```bash
python main.py
# (modifiez la variable 'fichier' dans main.py)
```

---

### Format du rapport
- ✓ Tests réussis (en vert)
- ✗ Tests échoués (en rouge)
- Temps d'exécution par test
- Taux de réussite global

---

## Notes Importantes

### Fonctionnalités Testées
- Arithmétique de base
- Comparaisons
- Opérateurs unaires
- Structures conditionnelles (if/else)
- Boucles (while, do-while, for)
- Instructions de contrôle (break, continue)
- Imbrications de structures de contrôle
- Pointeurs simples et tableaux
- Fonctions
- Récursivité
- Opérateurs logiques
- Variables multiples

### Limitations Connues
- Les tableaux sont traités comme des pointeurs
- Pas de vérification de bornes pour les accès tableaux
- Les déclarations de tableaux avec taille (`int arr[10]`) nécessitent un parsing spécifique

