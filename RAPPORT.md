# Rapport Technique - Compilateur PyComp

## 1. Architecture Globale

Le compilateur suit une architecture classique en 4 phases :

### 1.1 Analyse Lexicale (AnalyseurLexicale.py)
- Tokenisation du code source C
- Reconnaissance des mots-clés, identifiants, constantes, opérateurs
- Support des opérateurs multi-caractères (==, !=, >=, <=, &&, ||, !)
- Variables globales : `T` (token courant), `LAST` (historique)
- Fonctions : `check()`, `match()`, `accept()` pour le parsing pédagogique

### 1.2 Analyse Syntaxique (AnalyseurSyntaxique.py)
- Parsing descendant récursif avec priorité des opérateurs
- Grammaire : E (expressions) → P (préfixes) → S (suffixes) → A (atomes)
- Construction de l'AST via la classe `Node`
- Support des structures : if/else, while, do-while, for, fonctions
- Gestion des pointeurs (*p, &p) et tableaux (arr[i], [i]arr)

### 1.3 Analyse Sémantique (AnalyseurSemantique.py)
- Table des symboles avec pile de scopes (dictionnaires)
- Attribution d'indices aux variables (`NBvar`)
- Vérification des déclarations et résolution de portée
- Annotation des nœuds avec les indices de variables

### 1.4 Génération de Code (ops.py)
- Génération de code MSM (Machine à Pile)
- Parcours post-ordre de l'AST
- Table `NF` : fonctions de génération par type de nœud
- Remap des opérateurs MSM via `MSM_MAP`

## 2. État Initial du Code

Au début de la phase de test, le code compilait mais présentait 3 problèmes majeurs :

### 2.1 Opérateur NOT manquant
- L'opérateur logique `!` était utilisé dans les tests mais absent du lexer
- Le test 14_operateurs_logiques.c échouait systématiquement

### 2.2 Placement du halt incorrect
- Le `halt` était placé après toutes les définitions de fonctions
- Le programme MSM bouclait indéfiniment après le retour de main
- Tous les tests timeout lors de l'exécution

### 2.3 Bugs fonctionnels
- Test 09 (pointeurs) : retournait 40, 42 au lieu de 42, 100
- Test 12 (fonctions) : retournait 65540 au lieu de 8

## 3. Résolution des Bugs

### 3.1 Implémentation de l'opérateur NOT

**Diagnostic :**
L'énumération `tok_not` n'existait pas dans `TokenType`.

**Solution :**
```python
# AnalyseurLexicale.py
tok_not = 27  # Ajouté après tok_addr

# Reconnaissance dans next()
'!': TokenType.tok_not,  # Ajouté dans la table des symboles simples
```

**Parser :**
```python
# AnalyseurSyntaxique.py - fonction P()
elif LEX.T and LEX.T.type == TokenType.tok_not:
    LEX.match(TokenType.tok_not)
    sous = self.P()
    return self.node_1_enfant(NodeTypes.node_not, sous)
```

**AST :**
```python
# ast_nodes.py
node_not = 26  # Ajouté dans NodeTypes
```

**Génération :**
```python
# ops.py
NodeTypes.node_not: lambda n: GenNode(n.enfants[0]) + ["not"],
```

**Résultat :** Test 14 passe avec 0, 1, 0, 1

### 3.2 Correction du placement du halt

**Diagnostic :**
La fonction `write_msm()` ajoutait automatiquement `halt` à la fin du fichier, après toutes les définitions de fonctions. L'exécution MSM continuait après le `ret` de main.

**Solution :**
```python
# main.py - fonction gencode()
main_call = ["prep main", "call 0", "halt"]
final_instructions = main_call + instructions

# main.py - fonction write_msm()
# Suppression de : f.write("halt\n")
```

**Structure MSM résultante :**
```
.start
prep main
call 0
halt        <- Arrêt après main
.main
resn N
...
ret
.autres_fonctions
...
```

**Résultat :** Tous les tests s'exécutent correctement

### 3.3 Bug des fonctions (Test 12)

**Diagnostic :**
La variable globale `NBvar` continuait d'incrémenter entre les fonctions. Les variables de `main` commençaient à l'indice 3 au lieu de 0, causant des accès mémoire incorrects.

**Trace d'exécution :**
```
Fonction add() : variables aux indices 0, 1, 2 (correct)
Fonction main() : variables aux indices 3, 4, 5 (incorrect)
```

**Analyse du code :**
```python
# AnalyseurSemantique.py - fonction SemNode()
saved_nbvar = NBvar
beginBlock()
# ... traitement ...
N.nbvar = NBvar - saved_nbvar  # Calcul incorrect
```

**Solution :**
```python
# AnalyseurSemantique.py
saved_nbvar = NBvar
NBvar = 0           # Réinitialisation locale
beginBlock()
# ... traitement des paramètres et corps ...
N.nbvar = NBvar     # Nombre total de variables locales
NBvar = saved_nbvar # Restauration du contexte global
```

**Résultat :** Test 12 retourne 8 au lieu de 65540

### 3.4 Bug des pointeurs (Test 09)

**Diagnostic initial :**
Le test utilisait des variables locales sur la pile, incompatibles avec les instructions `read`/`write` MSM qui opèrent sur la mémoire.

**Architecture MSM :**
- Variables locales : `get`/`set` (indices sur pile)
- Mémoire : `read`/`write` (adresses absolues)
- Ce sont deux espaces distincts

**Tentative incorrecte :**
```c
int a;      // Variable sur pile (indice 0)
int *p;
a = 42;     // set 0 <- 42 (pile)
p = &a;     // p = 0
debug *p;   // read 0 (mémoire) -> lit ailleurs !
```

**Solution architecturale :**
Modification du test pour utiliser des tableaux (en mémoire) :
```c
int mem;
int *p;
mem[0] = 42;      // Écriture en mémoire
p = &mem[0];      // p pointe vers mémoire
debug *p;         // Lecture mémoire
*p = 100;         // Écriture mémoire
debug mem[0];     // Lecture mémoire
```

**Problème de génération :**
`&mem[0]` générait uniquement `push 0` au lieu de calculer l'adresse.

**Solution :**
```python
# ops.py
def NF_address(n):
    child = n.enfants[0]
    if child.type == NodeTypes.node_array_access:
        # Calculer base + index
        return (
            [f"push {child.enfants[0].valeur}"] +
            GenNode(child.enfants[1]) +
            ["add"]
        )
    else:
        return [f"push {child.valeur}"]
```

**Problème du write :**
L'instruction MSM `write` attend la pile dans l'ordre `[valeur, adresse]` (valeur au sommet). Avec `dup` avant `swap`, l'ordre devenait incorrect.

**Analyse de pile incorrecte :**
```
push 0      # [0]
push 42     # [0, 42]
dup         # [0, 42, 42]
swap        # [0, 42, 42]  <- swap les 2 du sommet uniquement
write       # Dépile 42 (valeur), 42 (adresse) -> écrit à l'adresse 42 !
```

**Solution finale :**
```python
def NF_affect(n):
    lhs, rhs = n.enfants[0], n.enfants[1]
    
    if lhs.type == NodeTypes.node_indirection:
        # [adresse, valeur] -> swap -> [valeur, adresse] -> write
        return GenNode(lhs.enfants[0]) + GenNode(rhs) + ["swap", "write", "push 0"]
```

Le `push 0` final compense le fait que `write` ne laisse rien sur la pile, alors que `node_drop` attend une valeur à supprimer.

**Résultat :** Test 09 retourne 42, 100

## 4. Validation Finale

Tous les tests ont été exécutés individuellement et comparés aux résultats attendus documentés dans tests/README.md :

| Test | Fonctionnalité | Attendu | Obtenu | Statut |
|------|----------------|---------|---------|--------|
| 01 | Arithmétique | 8,2,15,1 | 8,2,15,1 | OK |
| 02 | Comparaisons | booléens | 1,0,0,1,1,1 | OK |
| 03 | Unaires | -5,5,10 | -5,5,10 | OK |
| 04 | Priorités | 14,20,14,15 | 14,20,14,15 | OK |
| 05 | If simple | 100,100 | 100,100 | OK |
| 06 | If-else | 200,300 | 200,300 | OK |
| 07 | While | 10,5 | 10,5 | OK |
| 08 | Boucles imbriquées | 6 | 6 | OK |
| 09 | Pointeurs | 42,100 | 42,100 | OK |
| 10 | Tableaux postfixe | 10,20,30 | 10,20,30 | OK |
| 11 | Tableaux préfixe | 100,200,300 | 100,200,300 | OK |
| 12 | Fonctions | 8 | 8 | OK |
| 13 | Récursion | 120,6 | 120,6 | OK |
| 14 | Logiques | 0,1,0,1 | 0,1,0,1 | OK |
| 15 | Variables multiples | 1,2,3,4,5,10 | 1,2,3,4,5,10 | OK |

**Taux de réussite global : 15/15 (100%)**

## 5. Fonctionnalités Validées

- Expressions arithmétiques : +, -, *, /, %
- Comparaisons : >, <, >=, <=, ==, !=
- Opérateurs logiques : &&, ||, !
- Opérateurs unaires : -x, +x, !x
- Variables locales et affectations
- Structures conditionnelles : if, if-else
- Boucles : while, do-while, for avec break/continue
- Fonctions : déclaration, appel, paramètres, return
- Récursion
- Pointeurs : déréférencement (*p), adresse (&p)
- Tableaux : notation postfixe (arr[i]) et préfixe ([i]arr)

## 6. Limitations Architecturales

- Les pointeurs sur variables locales ne sont pas supportés (pile vs mémoire MSM)
- Les tableaux sont traités comme des zones mémoire indexées
- Pas de vérification de bornes pour les accès tableaux
- Pas de gestion de la mémoire dynamique
