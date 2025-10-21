# 🧪 Batterie de Tests - Compilateur PyComp

Ce dossier contient une suite complète de tests pour valider toutes les fonctionnalités du compilateur PyComp.

## 📋 Liste des Tests

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
- **Objectif**: Tester les opérateurs de comparaison
- **Fonctionnalités testées**: `>`, `<`, `==`, `!=`, `>=`, `<=`
- **Résultats attendus**: Valeurs booléennes (0 ou 1)

#### **03_operateurs_unaires.c**
- **Objectif**: Valider les opérateurs unaires
- **Fonctionnalités testées**: `-x`, `+x`
- **Résultats attendus**: Négation et identité correctes

#### **04_expressions_complexes.c**
- **Objectif**: Vérifier la priorité des opérateurs
- **Fonctionnalités testées**: Expressions avec parenthèses et priorités
- **Résultats attendus**: 
  - `2 + 3 * 4` = 14 (pas 20)
  - `(2 + 3) * 4` = 20

---

### Tests de Structures de Contrôle (05-08)

#### **05_if_simple.c**
- **Objectif**: Tester les structures conditionnelles simples
- **Fonctionnalités testées**: `if` sans `else`
- **Résultats attendus**: Exécution conditionnelle correcte

#### **06_if_else.c**
- **Objectif**: Tester les structures if-else
- **Fonctionnalités testées**: `if-else`
- **Résultats attendus**: Branchements corrects selon les conditions

#### **07_while_simple.c**
- **Objectif**: Valider les boucles while simples
- **Fonctionnalités testées**: `while`
- **Résultats attendus**: 
  - Somme 0+1+2+3+4 = 10
  - Compteur final = 5

#### **08_while_imbriques.c**
- **Objectif**: Tester les boucles imbriquées
- **Fonctionnalités testées**: `while` dans `while`
- **Résultats attendus**: Compteur = 6 (3×2 itérations)

---

### Tests de Pointeurs et Tableaux (09-11)

#### **09_pointeurs_simple.c**
- **Objectif**: Valider les opérations sur pointeurs
- **Fonctionnalités testées**: `&` (adresse), `*` (déréférencement)
- **Résultats attendus**: 
  - Lecture via pointeur: 42
  - Écriture via pointeur: 100

#### **10_tableaux_postfixe.c**
- **Objectif**: Tester la notation postfixe des tableaux
- **Fonctionnalités testées**: `arr[index]`
- **Résultats attendus**: 
  - arr[0] = 10
  - arr[1] = 20
  - arr[2] = 30

#### **11_tableaux_prefixe.c**
- **Objectif**: Tester la notation préfixe des tableaux
- **Fonctionnalités testées**: `[index]arr`
- **Résultats attendus**: 
  - [0]arr = 100
  - [1]arr = 200
  - [2]arr = 300

---

### Tests de Fonctions (12-13)

#### **12_fonctions_simple.c**
- **Objectif**: Valider les appels de fonctions
- **Fonctionnalités testées**: Définition et appel de fonction
- **Résultats attendus**: Fonction `add(5, 3)` = 8

#### **13_fonctions_recursives.c**
- **Objectif**: Tester la récursivité
- **Fonctionnalités testées**: Fonction récursive (factorielle)
- **Résultats attendus**: 
  - factorial(5) = 120
  - factorial(3) = 6

---

### Tests Avancés (14-15)

#### **14_operateurs_logiques.c**
- **Objectif**: Valider les opérateurs logiques
- **Fonctionnalités testées**: `&&`, `||`, `!`
- **Résultats attendus**: Opérations booléennes correctes

#### **15_variables_multiples.c**
- **Objectif**: Tester la gestion de plusieurs variables
- **Fonctionnalités testées**: Déclarations multiples, affectations
- **Résultats attendus**: Somme 1+2+3+4 = 10

---

## 🚀 Utilisation

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

## 📊 Rapport de Tests

Le script `run_tests.py` génère automatiquement :
- Un affichage coloré dans le terminal
- Un fichier `test_report.txt` avec les résultats détaillés

### Format du rapport
- ✓ Tests réussis (en vert)
- ✗ Tests échoués (en rouge)
- Temps d'exécution par test
- Taux de réussite global

---

## 🔧 Structure des Fichiers de Test

Chaque fichier de test suit cette structure :
```c
// Commentaire descriptif du test
int main() {
    // Déclarations
    int var;
    
    // Code de test
    var = 42;
    
    // Vérification avec debug
    debug var;  // Attendu: 42
    
    return 0;
}
```

---

## 📝 Notes Importantes

### Fonctionnalités Testées
- ✅ Arithmétique de base
- ✅ Comparaisons
- ✅ Opérateurs unaires
- ✅ Structures conditionnelles (if/else)
- ✅ Boucles (while)
- ✅ Pointeurs simples
- ✅ Tableaux (notation préfixe et postfixe)
- ✅ Fonctions
- ✅ Récursivité
- ✅ Opérateurs logiques
- ✅ Variables multiples

### Limitations Connues
- Les tableaux sont traités comme des pointeurs
- Pas de vérification de bornes pour les accès tableaux
- Les déclarations de tableaux avec taille (`int arr[10]`) nécessitent un parsing spécifique

### Instructions MSM Générées
Les tests génèrent des fichiers `.msm` qui peuvent être exécutés avec la machine virtuelle MSM :
- `push <val>` : Empile une valeur
- `pop` : Dépile
- `add`, `sub`, `mul`, `div` : Opérations arithmétiques
- `cmpgt`, `cmplt`, etc. : Comparaisons
- `read`, `write` : Accès mémoire (pointeurs/tableaux)
- `dbg` : Affichage debug
- `halt` : Arrêt du programme

---

## 🎯 Objectifs de la Batterie de Tests

1. **Validation fonctionnelle** : Vérifier que chaque fonctionnalité du compilateur fonctionne correctement
2. **Non-régression** : S'assurer que les modifications n'introduisent pas de bugs
3. **Documentation** : Servir d'exemples d'utilisation du langage
4. **Performance** : Mesurer les temps de compilation

---

## 🐛 Debugging

Si un test échoue :
1. Vérifier le message d'erreur dans le terminal
2. Consulter le fichier `test_report.txt`
3. Lancer le test individuellement pour plus de détails
4. Activer `DEBUG_LEXER = True` dans `main.py` pour voir les tokens
5. Examiner l'arbre syntaxique généré

---

## 📈 Évolution Future

Tests à ajouter :
- [ ] Tests de gestion d'erreurs
- [ ] Tests de cas limites (overflow, division par zéro)
- [ ] Tests de portée des variables
- [ ] Tests de tableaux multidimensionnels
- [ ] Tests de pointeurs de pointeurs
- [ ] Tests de structures de données complexes
- [ ] Tests de performance (grands programmes)

---

## 👥 Contribution

Pour ajouter un nouveau test :
1. Créer un fichier `XX_nom_du_test.c` dans le dossier `tests/`
2. Suivre la structure standard avec commentaires
3. Documenter les résultats attendus
4. Lancer `run_tests.py` pour valider

---

**Dernière mise à jour** : Octobre 2025
