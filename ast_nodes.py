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
    node_not = 26  # opérateur unaire !

    # instructions / variables
    node_block = 27
    node_debug = 28
    node_stmt_expr = 29   # (conservé si utile)
    node_drop = 30
    node_var = 31         # (réservé)
    node_declare = 32     # decl name;
    node_reference = 33   # ref name
    node_affect = 34      # ref = expr
    # structures de contrôle
    node_cond = 35         # if(E) I(else I)?
    node_loop = 36        # while(E)I|break|continue
    node_target = 37    
    node_break = 38
    node_continue = 39
    node_sequence = 40   
    node_fonction = 41   # function ref(params) block
    node_call = 42       # ref(args)
    node_return = 43     # return expr
    # pointeurs et tableaux
    node_indirection = 44  # *P (déréférencement)
    node_address = 45      # &P (adresse de)
    node_array_access = 46 # A[E] ou [E]A
    



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
