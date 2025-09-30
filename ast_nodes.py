from enum import Enum

class NodeTypes(Enum):
    node_eof = 1
    node_const = 2
    node_ident = 3
    # binaires arith.
    node_plus = 11
    node_moins = 12
    node_etoile = 13
    node_slash = 14
    node_modulo = 15
    # comparaisons
    node_supérieur = 18
    node_inférieur = 19
    node_supérieur_egal = 20
    node_inférieur_egal = 21
    node_egal_egal = 22
    node_différent = 23
    # logiques
    node_et = 24
    node_ou = 25

    # instructions / variables
    node_block = 26
    node_debug = 27
    node_stmt_expr = 28   # (conservé si utile)
    node_drop = 29
    node_var = 30         # (réservé)
    node_declare = 31     # decl name;
    node_reference = 32   # ref name
    node_affect = 33      # ref = expr
    # structures de contrôle
    node_cond = 34         # if(E) I(else I)?
    node_loop = 35        # while(E)I|break|continue
    node_target = 36    
    node_break = 37
    node_continue = 38
    node_sequence = 39   
    node_fonction = 40   # function ref(params) block
    node_call = 41       # ref(args)
    node_return = 42     # return expr
    



class Node:
    def __init__(self, type, valeur=0, chaine="", enfants=None):
        self.type = type
        self.valeur = valeur
        self.chaine = chaine
        self.enfants = list(enfants) if enfants else []

    def ajouter_enfant(self, enfant):
        self.enfants.append(enfant)

    def afficher(self):
        def _rec(n):
            if not n.enfants:
                payload = n.chaine if n.chaine != "" else n.valeur
                return f"{n.type.name}:{payload}"
            return f"({n.type.name} " + " ".join(_rec(c) for c in n.enfants) + ")"
        print(_rec(self))
    
    def node_1_enfant(self, type, enfant):
        n = Node(type)
        n.ajouter_enfant(enfant)
        return n

    def node_2_enfants(self, type, gauche, droite):
        n = Node(type)
        n.ajouter_enfant(gauche)
        n.ajouter_enfant(droite)
        return n

    def node_simple(self, type, valeur):
        return Node(type, valeur, "")
