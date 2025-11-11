# Rapport compilation : MESSAL Ilyes - ACHNINE Ilyas 

## Architecture du compilateur

Notre compilateur suit une architecture classique en plusieurs passes où l'analyseur lexical produit un flux de tokens qui est ensuite consommé par l'analyseur syntaxique pour construire un arbre syntaxique abstrait, lequel est ensuite vérifié par l'analyseur sémantique avant que le générateur de code ne produise le fichier assembleur final. 

Le module `ast_nodes.py` reprend les structures définies dans les notes de cours avec l'énumération `NodeTypes` qui liste tous les types de nœuds du langage et la classe `Node` qui encapsule les attributs `type`, `valeur`, `chaine` et `enfants` pour construire l'arbre syntaxique. 

Le fichier `ops.py` rassemble la gestion des opérateurs via la table `OP`, la gestion des noeuds faciles via le dictionnaire `NF` mais aussi les noeuds complexes. Concrètement, notre fonction `GenNode()` parcourt l'AST en post-ordre et délègue la génération aux lambdas du dictionnaire `NF`, pour les cas complexes (boucle, fonction, appel, etc), des fonctions spécifiques sont utilisées.


Le module `main.py` orchestre le pipeline de compilation en suivant l'architecture et réalise les appelles en cascade. La fonction `pipeline()` enchaîne l'analyse syntaxique qui construit l'AST, puis l'analyse sémantique via `SemNode()` qui vérifie la cohérence et annote l'arbre avec les indices de variables, et termine par la génération de code via `GenNode()` suivie de l'écriture du fichier assembleur. La fonction `write_msm()` prend en charge cette dernière étape en aplatissant récursivement les listes d'instructions potentiellement imbriquées produites par `GenNode()`, puis en écrivant le fichier de sortie avec la directive `.start` en début de fichier suivie d'un appel à la fonction `main` et de l'instruction `halt` avant les définitions des fonctions. 

### Utilisation

Pour compiler un fichier source, il suffit de placer le code à compiler dans le fichier `test.c` à la racine du projet, puis d'exécuter la commande `python3 main.py` qui produira le fichier assembleur `out.msm`. L'exécution du programme compilé se fait ensuite en se déplaçant dans le répertoire `msm` avec `cd msm` et en lançant la machine virtuelle via `./msm ../PyComp/out.msm`, ce qui affichera les résultats des instructions `debug` présentes dans le code source. Il est également possible d'activer le mode debug du lexer en modifiant la variable `DEBUG_LEXER` à `True` dans `main.py`, ce qui permet d'afficher le flux de tokens produit par l'analyse lexicale sans effectuer la compilation complète.
