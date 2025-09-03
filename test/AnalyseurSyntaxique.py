# -*- coding: utf-8 -*-
import AnalyseurLexicale as LEX
from AnalyseurLexicale import TokenType
from ast_nodes import Node, NodeTypes
from ops import OP

class AnalyseurSyntaxique:
    def __init__(self, filepath):
        # init pédagogique: place déjà LEX.T sur le 1er token
        LEX.init_from_file(filepath)
        self.arbre = self.E(0)

    # helpers
    def node_valeur(self, type, valeur, chaine=""):
        return Node(type, valeur, chaine)

    def node_1_enfant(self, type, chaine, enfant):
        n = Node(type, 0, chaine)
        n.ajouter_enfant(enfant)
        return n

    def node_2_enfants(self, type, gauche, droite):
        n = Node(type)
        n.ajouter_enfant(gauche)
        n.ajouter_enfant(droite)
        return n

    # grammaire
    def E(self, prio):
        N = self.P()
        while LEX.T and (LEX.T.type in OP):
            entry = OP[LEX.T.type]
            if entry["prio"] < prio:
                break
            op_tok = LEX.T.type
            LEX.match(op_tok)                 # consomme l'opérateur courant
            M = self.E(entry["parg"])         # associativité gauche
            N = self.node_2_enfants(entry["Ntype"], N, M)
        return N

    def P(self):
        # +x -> x ; -x -> (0 - x)
        if LEX.T and LEX.T.type == TokenType.tok_moins:
            LEX.match(TokenType.tok_moins)
            sous = self.P()
            zero = self.node_valeur(NodeTypes.node_const, 0, "0")
            return self.node_2_enfants(NodeTypes.node_moins, zero, sous)
        elif LEX.T and LEX.T.type == TokenType.tok_plus:
            LEX.match(TokenType.tok_plus)
            return self.P()
        else:
            return self.S()

    def S(self):
        return self.A()

    def A(self):
        if LEX.check(TokenType.tok_const):
            tok = LEX.T
            LEX.match(TokenType.tok_const)
            return self.node_valeur(NodeTypes.node_const, tok.valeur, tok.chaine)

        elif LEX.check(TokenType.tok_parenthese_ouvrante):
            LEX.accept(TokenType.tok_parenthese_ouvrante)
            sous = self.E(0)
            if not LEX.match(TokenType.tok_parenthese_fermeante):
                LEX.erreur("')' attendu")
                return None
            return sous

        else:
            LEX.erreur(f"Expression atomique attendue, trouvé: {(LEX.T.type.name if LEX.T else 'None')}")
            return None
