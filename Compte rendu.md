# Rapport compilation : MESSAL Ilyes - ACHNINE Ilyas 

## Architecture du compilateur

Notre compilateur suit une architecture classique en plusieurs passes où l'analyseur lexical produit un flux de tokens qui est ensuite consommé par l'analyseur syntaxique pour construire un arbre syntaxique abstrait, lequel est ensuite vérifié par l'analyseur sémantique avant que le générateur de code ne produise le fichier assembleur final. 

Le module `ast_nodes.py` reprend les structures définies dans les notes de cours avec l'énumération `NodeTypes` qui liste tous les types de nœuds du langage et la classe `Node` qui encapsule les attributs `type`, `valeur`, `chaine` et `enfants` pour construire l'arbre syntaxique. 

Le fichier `ops.py` rassemble la gestion des opérateurs via la table `OP`, la gestion des noeuds faciles via le dictionnaire `NF` mais aussi les noeuds complexes. Concrètement, notre fonction `GenNode()` parcourt l'AST en post-ordre et délègue la génération aux lambdas du dictionnaire `NF`, pour les cas complexes (boucle, fonction, appel, etc), des fonctions spécifiques sont utilisées.


Le module `main.py` orchestre le pipeline de compilation en suivant l'architecture et réalise les appelles en cascade. La fonction `pipeline()` enchaîne l'analyse syntaxique qui construit l'AST, puis l'analyse sémantique via `SemNode()` qui vérifie la cohérence et annote l'arbre avec les indices de variables, et termine par la génération de code via `GenNode()` suivie de l'écriture du fichier assembleur. La fonction `write_msm()` prend en charge cette dernière étape en aplatissant récursivement les listes d'instructions potentiellement imbriquées produites par `GenNode()`, puis en écrivant le fichier de sortie avec la directive `.start` en début de fichier suivie d'un appel à la fonction `main` et de l'instruction `halt` avant les définitions des fonctions. 

### Utilisation

Pour compiler un fichier source, il suffit de placer le code à compiler dans le fichier `test.c` à la racine du projet, puis d'exécuter la commande `python3 main.py` qui produira le fichier assembleur `out.msm`. L'exécution du programme compilé se fait ensuite en se déplaçant dans le répertoire `msm` avec `cd msm` et en lançant la machine virtuelle via `./msm ../PyComp/out.msm`, ce qui affichera les résultats des instructions `debug` présentes dans le code source. Il est également possible d'activer le mode debug du lexer en modifiant la variable `DEBUG_LEXER` à `True` dans `main.py`, ce qui permet d'afficher le flux de tokens produit par l'analyse lexicale sans effectuer la compilation complète.

## Tests et validation

Pour valider le compilateur, nous avons développé une batterie de 24 tests couvrant l'ensemble des fonctionnalités implémentées. Ces tests sont organisés dans le répertoire `tests/` et chacun teste une fonctionnalité spécifique du langage. Le script `run_tests.py` automatise l'exécution en copiant successivement chaque fichier `.c` dans `test.c`, en lançant la compilation avec `main.py`, puis en exécutant le fichier MSM généré et en comparant la sortie obtenue avec la sortie attendue définie dans le script.

### Tableau récapitulatif des tests

| # | Test | Fonctionnalité | Sortie attendue | Statut | Difficultés rencontrées |
|---|------|----------------|-----------------|--------|-------------------------|
| 01 | arithmetique_simple | +, -, *, / | 8, 2, 15, 1 | ✓ | Aucune |
| 02 | comparaisons | >, <, ==, !=, >=, <= | 1, 0, 0, 1, 1, 1 | ✓ | Aucune |
| 03 | operateurs_unaires | -x, +x | -5, 5, 10 | ✓ | Aucune |
| 04 | expressions_complexes | Priorités, parenthèses | 14, 20, 14, 15 | ✓ | Aucune |
| 05 | if_simple | if sans else | 100, 100 | ✓ | Aucune |
| 06 | if_else | if-else | 200, 300 | ✓ | Aucune |
| 07 | while_simple | while | 10, 5 | ✓ | Timeout dû au placement du halt |
| 08 | while_imbriques | Boucles imbriquées | 6 | ✓ | Timeout dû au placement du halt |
| 09 | pointeurs_simple | *, & | 42, 100 | ✓ | Pile vs mémoire MSM, calcul adresse, ordre write |
| 10 | tableaux_postfixe | arr[i] | 10, 20, 30 | ✓ | Aucune |
| 11 | tableaux_prefixe | [i]arr | 100, 200, 300 | ✓ | Aucune |
| 12 | fonctions_simple | Appel de fonction | 8 | ✓ | NBvar global non réinitialisé (sortie 65540) |
| 13 | fonctions_recursives | Récursion | 120, 6 | ✓ | NBvar global non réinitialisé |
| 14 | operateurs_logiques | &&, \|\|, ! | 0, 1, 0, 1 | ✓ | Opérateur ! absent du lexer |
| 15 | variables_multiples | Déclarations multiples | 1, 2, 3, 4, 5, 10 | ✓ | Aucune |
| 16 | if_imbriques | if dans if | 1 | ✓ | Aucune |
| 17 | if_while_imbriques | if dans while | 6 | ✓ | Aucune |
| 18 | while_if_imbriques | while dans if | 3 | ✓ | Aucune |
| 19 | complex_nesting | while+if-else+while | 12 | ✓ | Aucune |
| 20 | mixed_nesting | Imbrications mixtes | 16 | ✓ | Aucune |
| 21 | do_while_simple | do-while | 10 | ✓ | Aucune |
| 22 | break_continue | break, continue | 9 | ✓ | Aucune |
| 23 | pointeurs_tableaux | Combinaison *p et arr[i] | 42, 100 | ✓ | Mêmes problèmes que test 09 |
| 24 | for_simple | for(init;cond;incr) | 10 | ✓ | Aucune |

Le taux de réussite final est de 24/24 soit 100%. Cependant, arriver à ce résultat a nécessité de résoudre plusieurs problèmes majeurs qui nous ont pris du temps à identifier et corriger.

### Les difficultés rencontrées

La première difficulté importante concernait le placement de l'instruction `halt` dans le fichier MSM généré. Quand on a lancé les premiers tests, tous les programmes entraient dans des boucles infinies et provoquaient des timeouts. Au début, on pensait que c'était un problème dans la génération des boucles `while`, mais après avoir analysé le fichier `out.msm` généré, on s'est rendu compte que le `halt` était placé tout à la fin du fichier, après toutes les définitions de fonctions. Du coup, après que la fonction `main` faisait son `ret`, l'exécution continuait séquentiellement sur les instructions suivantes au lieu de s'arrêter. Pour corriger ça, on a restructuré la fonction `write_msm()` dans `main.py` pour placer le `halt` juste après l'appel à `main`. Maintenant le fichier MSM commence par `.start`, puis `prep main`, `call 0`, et immédiatement `halt`, et ensuite viennent toutes les définitions de fonctions.

Le deuxième problème était plus simple à identifier mais on l'avait complètement oublié. Le test 14 qui teste les opérateurs logiques échouait avec une erreur "caractère inconnu '!'" pendant la compilation. En fait, on avait implémenté les opérateurs `&&` et `||` en cours mais on avait oublié l'opérateur de négation `!`. Il fallait donc l'ajouter dans toute la chaîne de compilation. D'abord, on a ajouté `tok_not = 27` dans l'énumération `TokenType` de l'analyseur lexical, puis on a ajouté la reconnaissance du caractère dans la table des symboles de la fonction `next()`. Ensuite, dans l'analyseur syntaxique, on a modifié la fonction `P()` qui gère les préfixes pour traiter `!E` comme un opérateur unaire, exactement comme `-E`. On a aussi ajouté `node_not` dans l'énumération des types de nœuds de l'AST, et enfin dans `ops.py`, on a ajouté la génération de code qui consiste simplement à générer le code de l'enfant suivi de l'instruction `not`.

Le troisième bug était plus subtil et concernait la gestion des fonctions. Les tests 12 et 13 produisaient des résultats complètement faux, par exemple le test 12 retournait 65540 au lieu de 8. On a mis un moment à comprendre le problème. En fait, la variable globale `NBvar` qui sert à compter les indices des variables dans l'analyse sémantique continuait à s'incrémenter d'une fonction à l'autre. Concrètement, si on définit d'abord une fonction `add` avec 3 variables locales qui prennent les indices 0, 1 et 2, puis qu'on définit la fonction `main`, ses variables locales commençaient à l'indice 3 au lieu de repartir à 0. Du coup, quand la fonction `main` faisait `get 0` pour accéder à sa première variable, elle allait chercher au mauvais endroit sur la pile. La solution était de sauvegarder la valeur de `NBvar` avant de traiter une fonction, de la réinitialiser à 0 pour compter les variables locales de cette fonction, puis de la restaurer après. On a fait ça dans la fonction `SemNode()` du fichier `AnalyseurSemantique.py` pour le cas `node_fonction`. C'était un piège classique avec les variables globales partagées. 

Le dernier problème était le plus complexe et concernait les pointeurs dans le test 09. Ce test retournait des valeurs complètement fausses. Le problème principal venait de la différence entre notre compréhension intuitive des pointeurs et la façon dont MSM gère réellement la mémoire. En MSM, il y a deux espaces mémoire complètement séparés. D'un côté, il y a la pile qui stocke les variables locales des fonctions et qu'on manipule avec les instructions `get` et `set` en utilisant des indices. De l'autre côté, il y a la mémoire qui stocke les données persistantes et qu'on manipule avec les instructions `read` et `write` en utilisant des adresses. Le test initial essayait de créer un pointeur vers une variable locale avec `p = &a` où `a` était une variable sur la pile, mais ça ne correspond pas au modèle de MSM. On ne peut pas obtenir l'adresse mémoire d'une variable locale parce qu'elle n'existe que sur la pile. On a donc dû modifier le test pour utiliser des tableaux à la place, car les tableaux en MSM résident en mémoire. Le test modifié déclare un tableau `mem` et fait `mem[0] = 42`, puis `p = &mem[0]`, et ensuite `debug *p`. 

Mais ça n'a pas suffi, il restait deux sous-problèmes. Le premier était que l'expression `&mem[0]` ne générait que `push 0` au lieu de calculer l'adresse effective. On a corrigé la fonction `NF_address` dans `ops.py` pour détecter quand on prend l'adresse d'un accès tableau et dans ce cas, générer le calcul complet `base + index`. Le deuxième sous-problème concernait l'ordre des éléments sur la pile pour l'instruction `write`. En MSM, l'instruction `write` s'attend à trouver la valeur au sommet de la pile et l'adresse juste en dessous, mais notre génération produisait l'ordre inverse. On a ajouté une instruction `swap` dans la génération de code pour les affectations via indirection pour inverser l'ordre et obtenir `[valeur, adresse]` comme attendu par `write`. 

### Comment on a utilisé le cours

Pour l'analyse lexicale, on a directement appliqué ce qu'on avait vu au cours 1 avec la classe `Token` qui contient les attributs `type`, `valeur` et `chaine`, et les fonctions `check()`, `match()` et `accept()` pour consommer les tokens. La fonction `next()` qui découpe le code source en tokens utilise exactement la même logique qu'en cours avec les tests sur le caractère courant pour reconnaître les constantes, les identifiants et les mots-clés.

Pour l'analyse syntaxique, on a suivi l'approche des cours 2 et 3 avec le parsing descendant récursif et la grammaire `E(prio)` → `P()` → `S()` → `A()`. La fonction `E(prio)` utilise la table `OP` vue en cours qui associe à chaque opérateur sa priorité et la priorité de ses arguments. C'est cette table qui permet de gérer correctement les priorités des opérateurs comme le fait que `*` est prioritaire sur `+`. La boucle dans `E(prio)` qui teste si la priorité de l'opérateur courant est inférieure à `prio` et qui appelle récursivement `E()` avec `parg` est exactement celle du cours.

Pour l'analyse sémantique qu'on a vue au cours 5, on a implémenté la pile de tables des symboles avec les fonctions `beginBlock()` et `endBlock()` qui ajoutent et retirent des dictionnaires de la pile. La fonction `declare()` vérifie qu'on ne déclare pas deux fois la même variable dans le même bloc, et la fonction `find()` remonte la pile de scopes pour trouver une variable. Le compteur global `NBvar` qui attribue un indice unique à chaque variable est aussi directement tiré du cours. La fonction `SemNode()` qui parcourt l'arbre suit la structure donnée en cours avec le switch sur le type de nœud et les cas particuliers pour `node_block`, `node_declare` et `node_reference`.

Pour la génération de code, on a utilisé les tables `OP` et `NF` présentées au cours 3. La table `NF` mappe chaque type de nœud simple à sa génération en listant le code à générer après avoir traité les enfants. La fonction `GenNode()` fait le parcours post-ordre de l'arbre comme expliqué en cours. Pour les boucles qu'on a vues au cours 6, on a utilisé la structure avec les nœuds `target`, `loop` et `cond` et la génération de labels avec le compteur global `nlbl`. C'est cette structure qui permet de gérer les `break` et `continue` correctement en sautant vers les bons labels.

## Conclusion

Le développement de ce compilateur nous a permis de mettre en pratique tous les concepts vus en cours, de l'analyse lexicale jusqu'à la génération de code. Les principales difficultés rencontrées ne venaient pas tant de l'implémentation des algorithmes du cours que de la compréhension du modèle d'exécution de la machine cible MSM, notamment la distinction entre pile et mémoire pour les pointeurs. Le passage de 0% à 100% de tests réussis s'est fait progressivement en corrigeant quatre bugs majeurs qui nécessitaient chacun de bien comprendre comment fonctionne MSM et comment les différentes phases du compilateur interagissent via les variables globales partagées.

