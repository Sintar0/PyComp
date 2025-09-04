# TODO — C4 : Instructions, blocs, debug, (TS en place)
0) Pré-décisions (contrats)

 [] Convention “E;” : évaluer l’expression puis jeter le résultat → émettre drop 1 en MSM.

 [] Point d’entrée : le programme complet est une suite d’instructions ; le parseur construira une racine (block) contenant I*.

 [] MSM : on continue à générer un .msm avec .start, puis le code, puis halt.

1) AST (fichier ast_nodes.py)

 [] Ajouter NodeTypes.node_block (n-aire).

 [] Ajouter NodeTypes.node_debug (unaire, enfant = expression).

 [] (Option) NodeTypes.node_stmt_expr si tu veux un nœud explicite pour E; (sinon on gère en gencode “statements” directement).

 [] Vérifier que afficher() sait imprimer un block proprement (enfants séquentiels).

2) Parser — nouvelles règles “instructions” (fichier AnalyseurSyntaxique.py)
Nouvelles fonctions

 [x] def I(self): // parse une instruction

Cas 1 — debug E ;

[x] accept(tok_debug), parse E(0), accept(tok_point_virgule) → node_debug(E).

Cas 2 — Bloc { I* }

[x] accept(tok_accolade_ouvrante), puis boucle :
tant que pas tok_accolade_fermeante, appeler I() et empiler l’enfant ;
enfin accept(tok_accolade_fermeante) → node_block([...]).

Cas 3 — E ;

[] parse E(0), accept(tok_point_virgule) → soit node_stmt_expr(E) soit renvoyer un petit nœud « wrapper » (au choix).

 def Program(self): // point d’entrée parseur

Tant que T ≠ tok_eof, I() et accumuler les nœuds → retourner un node_block([...]) racine.

 Constructor

Remplacer self.arbre = self.E(0) par self.arbre = self.Program().

Garde-fous & cohérence

 Sur { I* }, bien gérer le cas bloc vide.

 Messages d’erreur clairs si ; manquant après debug E ou E.

3) Gencode — “statements” (fichier ops.py ou nouveau stmt_codegen.py)

On garde GenNode (expressions) tel quel, et on ajoute un émetteur pour les instructions.

 Créer def GenStmt(n): qui traite :

node_debug(expr) → GenNode(expr) puis dbg.

node_stmt_expr(expr) → GenNode(expr) puis drop 1.

node_block(children[]) → pour chaque enfant GenStmt(child).

 Créer def GenProgram(root):

Suppose root est un node_block.

Émet séquentiellement toutes les instructions via GenStmt.

 Adapter write_msm(...)

Mapping MSM déjà en place ; ajouter émission de :

dbg (identique MSM),

drop 1 (la MSM veut un argument → drop 1).

4) Intégration pipeline (fichier main.py)

 [] Remplacer l’appel à GenNode(arbre) par :

[] code = GenProgram(arbre) (récupère une liste d’instructions postfixe statements+expressions)

[] Afficher les instructions si tu veux (debug), puis write_msm(code, "out.msm"), puis halt.

 Cas tests :

Expression seule : 1+2*3; → doit afficher 7 via dbg seulement si tu ajoutes un debug explicite ; avec E; simple, le résultat est drop.

Debug : debug 1+2*3; → affiche 7.

Bloc : { debug 1; debug 2; } → affiche 1 puis 2.

5) Table des symboles (fichier ts.py, posée mais pas encore utilisée)

API minimaliste (stack de frames) :

 begin() : pousse un nouveau scope (nouvelle table).

 end() : pop le dernier scope.

 declare(name) -> addr : alloue une adresse (p.ex. incrément d’un compteur local) et l’enregistre dans le scope courant.

 find(name) -> addr|None : recherche de haut en bas (scopes imbriqués).

 (interne) gestion d’un compteur d’offset par bloc (utile plus tard pour get/set MSM).

Pour l’instant, on implémente l’API et les structures, sans l’utiliser dans le parser/gencode. L’usage viendra quand on ajoutera ident, affectations, resn/get/set, etc.

6) Tests unitaires / fichiers d’essai

 test1.c : 1 + 2 * 3;

attendu : aucune sortie (résultat droppé).

 test2.c : debug 1 + 2 * 3;

attendu : 7.

 test3.c : { debug 1; debug 2; }

attendu : 1\n2\n.

 test4.c : { debug (1+2); 3+4; debug 5; }

attendu : 3\n5\n (la ligne 3+4; ne produit rien).

 Générer out.msm, exécuter ./msm out.msm.

7) Backlog (prochaines itérations)

 if (E) I puis if (E) I else I → se mappe vers jumpt/jumpf + labels.

 Boucles while (E) I → labels + jump/jumpf.
(Décider si une boucle retourne quelque chose : en général non → statements purs.)

 return E; (si on introduit fonctions) → mapping MSM ret en s’appuyant sur prep/call/resn.

 Variables/affectations : ident = E;
- parser : reconnaître tok_ident tok_egal E ;
- TS : find(ident) pour l’adresse
- MSM : set <offset>/get <offset> + resn au début de bloc.

 Unary ! (logique) et & sémantique (adresse/bit-à-bit) : à spécifier.