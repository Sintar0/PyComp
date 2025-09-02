from AnalyseurLexicale import TokenType, Token, T, next, init_from_file, erreur
from enum import Enum

class Node:
    def __init__(self, type, valeur, chaine, enfants=None):
        self.type = type 
        self.valeur = valeur
        self.chaine = chaine
        self.enfants = enfants if enfants else []

    def ajouter_enfant(self, enfant):
        self.enfants.append(enfant)
    
    def afficher(self, indent=0):
        # Si le nœud est une feuille (constante ou identifiant), on affiche valeur
        if not self.enfants:
            print(f"{self.type.name}:{self.chaine}", end="")
        else:
            print(f"({self.type.name}, (", end="")
            for i, enfant in enumerate(self.enfants):
                enfant.afficher()
                if i < len(self.enfants) - 1:
                    print(", ", end="")
            print("))", end="")

        # Seulement pour l'appel initial, faire un retour à la ligne
        if indent == 0:
            print()


class NodeTypes(Enum):
    node_eof = 1
    node_const = 2
    node_ident = 3
    node_parenthese_ouvrante = 4
    node_parenthese_fermeante = 5
    node_accolade_ouvrante = 6
    node_accolade_fermeante = 7
    node_croche_ouvrante = 8
    node_croche_fermeante = 9
    node_egal = 10
    node_plus = 11
    node_moins = 12
    node_etoile = 13
    node_slash = 14
    node_modulo = 15
    node_virgule = 16
    node_point_virgule = 17
    node_supérieur = 18
    node_inférieur = 19
    node_supérieur_egal = 19
    node_inférieur_egal = 20
    node_egal_egal = 21
    node_différent = 22
    node_et = 23
    node_ou = 24
    node_addr = 25
    node_int = 26
    node_void = 27
    node_return = 28
    node_do = 29
    node_if = 30
    node_else = 31
    node_while = 32
    node_for = 33
    node_default = 34
    node_break = 35
    node_continue = 36
    node_debug = 37
    node_send = 38
    node_recv = 39


OP = {
    TokenType.tok_plus:     { "prio": 5, "parg": 6, "Ntype": NodeTypes.node_plus },
    TokenType.tok_moins:    { "prio": 5, "parg": 6, "Ntype": NodeTypes.node_moins },
    TokenType.tok_etoile:   { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_etoile },
    TokenType.tok_slash:    { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_slash },
    TokenType.tok_modulo:   { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_modulo },
    TokenType.tok_supérieur: { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_supérieur },
    TokenType.tok_inférieur: { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_inférieur },
    TokenType.tok_supérieur_egal: { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_supérieur_egal },
    TokenType.tok_inférieur_egal: { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_inférieur_egal },
    TokenType.tok_egal_egal: { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_egal_egal },
    TokenType.tok_différent: { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_différent },
    TokenType.tok_et: { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_et },
    TokenType.tok_ou: { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_ou }
}

#GenNode 
def GenNode(Node):
    if Node.type == NodeTypes.node_eof:
        return ""



class AnalyseurSyntaxique:
    def __init__(self, filepath):
        init_from_file(filepath)
        global T
        T = next()  # <<< On consomme le premier token ICI
        print(f"[DEBUG] Démarrage analyse syntaxique, premier token : {T.type.name}")
        self.arbre = self.E(0)
        print("=== Arbre Syntaxique ===")
        if self.arbre:
            self.arbre.afficher()
        else:
            print("Erreur : aucun arbre généré")

    def node_valeur(self, type, valeur, chaine):
        return Node(type, valeur, chaine)

    def node_1_enfant(self, type, chaine, enfant):
        node = Node(type, 0, chaine)
        node.ajouter_enfant(enfant)
        return node
    
    def node_2_enfants(self, type, gauche, droite):
        node = Node(type, 0, "")
        node.ajouter_enfant(gauche)
        node.ajouter_enfant(droite)
        return node

    def P(self):
        global T
        if T.type == TokenType.tok_moins:
            T = next()
            sous_arbre = self.P()
            return self.node_1_enfant(NodeTypes.node_moins, "-", sous_arbre)
        elif T.type == NodeTypes.node_plus:
            T = next()
            sous_arbre = self.P()
            return self.node_1_enfant(NodeTypes.node_plus, "+", sous_arbre)
        else:
            return self.S()

    def E(self, prio):
        global T
        N = self.P()
        while T.type in OP:
            entry = OP[T.type]
            if entry["prio"] < prio:
                break
            op_token = T.type
            T = next()
            M = self.E(entry["parg"])
            N = self.node_2_enfants(entry["Ntype"], N, M)
        return N  # ✅ return N après la boucle (pas à l'intérieur)

    def S(self):
        return self.A()

    def A(self):
        global T
        if T.type == TokenType.tok_const:
            token = T
            T = next()
            return self.node_valeur(NodeTypes.node_const, token.valeur, token.chaine)
        elif T.type == TokenType.tok_parenthese_ouvrante:
            T = next()
            sous_arbre = self.E(0)
            if T.type != TokenType.tok_parenthese_fermeante:
                erreur("Parenthèse fermante manquante")
                return None
            T = next()
            return sous_arbre
        else:
            erreur(f"Expression atomique attendue, trouvé: {T.type.name}")
            return None

