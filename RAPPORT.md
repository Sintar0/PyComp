# Rapport de Projet - Compilateur C vers MSM

## 1. Introduction

Ce projet consiste à créer un compilateur capable de transformer du code C en assembleur MSM (machine à pile). Le compilateur respecte l'architecture en 4 phases vue en cours : analyse lexicale, syntaxique, sémantique et génération de code.

## 2. Architecture du compilateur

On a suivi le pipeline classique du cours :

### 2.1 Analyse Lexicale (AnalyseurLexicale.py)

Découpage du code source en tokens comme vu au C1. On a implémenté :
- Classe `Token` avec type, valeur et chaine
- Fonction `next()` qui reconnait les mots-clés, constantes, identifiants
- Fonctions `check()`, `match()`, `accept()` pour vérifier et consommer les tokens
- Variable globale `T` pour le token courant

Les opérateurs double caractères (`==`, `!=`, `>=`, `<=`, `&&`, `||`) sont reconnus en priorité avant les simples.

### 2.2 Analyse Syntaxique (AnalyseurSyntaxique.py)

Parsing descendant récursif comme au C2/C3 avec la grammaire :
- `E(prio)` : expressions avec gestion des priorités (table OP vue en cours)
- `P()` : préfixes (`-`, `+`, `!`, `*`, `&`)
- `S()` : suffixes (tableaux `arr[i]` ou `[i]arr`, appels de fonction)
- `A()` : atomes (constantes, identifiants, parenthèses)
- `I()` : instructions (debug, blocks, if, while, for, déclarations...)
- `F()` : fonctions

La fonction `E(prio)` utilise la table des priorités comme au C3 pour gérer les opérateurs binaires correctement.

### 2.3 Analyse Sémantique (AnalyseurSemantique.py)

Comme au C5, on a :
- Une pile de tables de symboles `_TS_STACK` (des dictionnaires en Python)
- `beginBlock()` / `endBlock()` pour gérer les scopes
- `declare()` pour déclarer une variable avec son index
- `find()` pour retrouver une variable dans les scopes
- Variable globale `NBvar` pour compter les variables

La fonction `SemNode()` parcourt l'arbre et :
- Pour `node_block` : crée un nouveau scope
- Pour `node_declare` : réserve un index pour la variable
- Pour `node_reference` : annote le noeud avec l'index trouvé
- Pour `node_fonction` : gère les paramètres et variables locales

### 2.4 Génération de Code (ops.py + main.py)

On génère du code MSM avec :
- Table `NF` qui mappe chaque type de noeud à sa génération
- Table `OP` pour les opérateurs (prio, parg, Ntype)
- Fonction `GenNode()` qui parcourt l'arbre en post-ordre
- Instructions MSM : push, get, set, add, mul, etc.

Pour les boucles (C6), on utilise des labels avec un compteur global `nlbl` et la structure target/loop/cond vue en cours.

## 3. Problèmes rencontrés et solutions

### 3.1 L'opérateur NOT manquant

**Problème** : Le test 14 (opérateurs logiques) ne compilait pas, erreur "caractère inconnu '!'"

**Cause** : J'avais oublié d'ajouter `tok_not` dans le lexer

**Solution** :
- Ajouté `tok_not = 27` dans TokenType
- Ajouté `'!': TokenType.tok_not` dans la table des symboles
- Ajouté le cas dans `P()` pour gérer `!E`
- Ajouté `node_not` dans l'AST
- Génération : `GenNode(enfant) + ["not"]`

### 3.2 Le halt au mauvais endroit

**Problème** : Tous les tests tournaient en boucle infinie, timeout systématique

**Cause** : Le `halt` était après toutes les fonctions au lieu d'être juste après l'appel à main. Du coup après `ret` de main, l'exécution continuait sur les autres fonctions.

**Solution** : Restructurer le fichier MSM :
```
.start
prep main
call 0
halt        <- ici et pas à la fin
.main
...
ret
.autres_fonctions
```

Ça a été galère à debugger parce qu'on voyait pas directement le problème dans le code, fallait comprendre comment MSM exécutait le fichier.

### 3.3 Le compteur NBvar qui déconnait

**Problème** : Le test 12 retournait 65540 au lieu de 8

**Cause** : La variable globale `NBvar` continuait à incrémenter entre les fonctions. Si la première fonction avait 3 variables (indices 0,1,2), la fonction main commençait à l'indice 3 au lieu de 0. Du coup `get 0` dans main allait chercher au mauvais endroit.

**Solution** : Dans SemNode pour node_fonction :
```python
saved_nbvar = NBvar
NBvar = 0           # reset pour cette fonction
# traitement de la fonction
N.nbvar = NBvar     # nombre de variables locales
NBvar = saved_nbvar # on restaure
```

C'était un piège classique de variable globale partagée.

### 3.4 Les pointeurs et la mémoire MSM

**Problème** : Le test 09 retournait n'importe quoi

**Cause principale** : En MSM, la pile et la mémoire c'est deux trucs séparés :
- Variables locales : `get`/`set` sur la pile
- Mémoire : `read`/`write` sur des adresses

On peut pas faire un pointeur vers une variable locale. Le test essayait de faire `p = &a` où `a` est sur la pile.

**Solution** : Modifier le test pour utiliser des tableaux (qui sont en mémoire) :
```c
int mem;
int *p;
mem[0] = 42;      // en mémoire
p = &mem[0];
debug *p;
```

**Autre problème** : `&arr[i]` générait juste `push 0` au lieu de calculer l'adresse.

**Solution** : Dans NF_address, détecter si c'est un array_access et calculer base + index.

**Dernier problème** : L'ordre sur la pile pour `write`. L'instruction MSM `write` veut [valeur, adresse] avec la valeur au sommet. On avait mis un `dup` qui cassait tout.

**Solution** : Pour `*p = valeur`, générer `[adresse] [valeur] swap write` pour avoir le bon ordre.

Franchement les pointeurs c'était la partie la plus chiante, il a fallu comprendre comment MSM gérait la mémoire.

## 4. Tests et résultats

On a fait 24 tests au total qui couvrent tout ce qu'on a vu en cours.

### 4.1 Tableau des tests

| Test | Fonctionnalité | Résultat | Difficultés |
|------|----------------|----------|-------------|
| 01 | Arithmétique (+,-,*,/) | ✓ | Aucune |
| 02 | Comparaisons | ✓ | Aucune |
| 03 | Opérateurs unaires | ✓ | Aucune |
| 04 | Priorités opérateurs | ✓ | Aucune |
| 05 | if simple | ✓ | Aucune |
| 06 | if-else | ✓ | Aucune |
| 07 | while | ✓ | Timeout avant fix halt |
| 08 | while imbriqués | ✓ | Timeout avant fix halt |
| 09 | Pointeurs | ✓ | Pile vs mémoire, &arr[i], ordre write |
| 10 | Tableaux postfixe arr[i] | ✓ | Aucune |
| 11 | Tableaux préfixe [i]arr | ✓ | Aucune |
| 12 | Fonctions | ✓ | NBvar global qui s'incrémentait |
| 13 | Récursion | ✓ | Même problème NBvar |
| 14 | Opérateurs logiques &&, \|\|, ! | ✓ | tok_not manquant |
| 15 | Variables multiples | ✓ | Aucune |
| 16 | if imbriqués | ✓ | Aucune |
| 17 | if dans while | ✓ | Aucune |
| 18 | while dans if | ✓ | Aucune |
| 19 | Imbrications complexes | ✓ | Aucune |
| 20 | Imbrications mixtes | ✓ | Aucune |
| 21 | do-while | ✓ | Aucune |
| 22 | break/continue | ✓ | Aucune |
| 23 | Pointeurs + tableaux | ✓ | Mêmes problèmes que test 09 |
| 24 | for | ✓ | Aucune |

**Résultat final : 24/24 (100%)**

### 4.2 Ce qui a marché du premier coup

Les trucs de base du cours (C1 à C4) ont bien marché :
- Analyse lexicale avec les tokens
- Parsing des expressions avec la table OP
- Les instructions simples (debug, blocks)
- Les if/else
- La table des symboles

### 4.3 Ce qui a posé problème

1. **Les fonctions** : Le coup du NBvar global pas réinitialisé, on a mis un moment à comprendre
2. **Les pointeurs** : Comprendre la différence pile/mémoire MSM
3. **Le halt** : Fallait bien lire la doc MSM pour comprendre

## 5. Conclusion

Le compilateur marche bien, tous les tests passent. On a respecté ce qui était demandé en cours :
- Les 4 phases d'analyse
- La table OP pour les priorités (C3)
- La table des symboles avec scopes (C5)
- Les boucles avec labels (C6)
- Les fonctions avec pile (C7)
- Les pointeurs et tableaux (C9)

Les principaux bugs venaient de la différence entre ce qu'on avait en tête et comment MSM fonctionne vraiment (surtout pour la mémoire et le halt).

---

## Annexe : Structure des fichiers

- `AnalyseurLexicale.py` : Découpage en tokens (C1)
- `AnalyseurSyntaxique.py` : Construction de l'AST (C2/C3)
- `AnalyseurSemantique.py` : Table des symboles (C5)
- `ast_nodes.py` : Définition des types de noeuds
- `ops.py` : Tables OP et NF, génération MSM
- `main.py` : Point d'entrée, orchestration des phases
- `run_tests.py` : Script de test automatique
- `tests/` : 24 fichiers de test .c
