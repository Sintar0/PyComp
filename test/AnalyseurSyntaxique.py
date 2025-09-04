# -*- coding: utf-8 -*-
import AnalyseurLexicale as LEX
from AnalyseurLexicale import TokenType
from ast_nodes import Node, NodeTypes
from ops import OP

class AnalyseurSyntaxique:
    def __init__(self, filepath):
        # init pédagogique: place déjà LEX.T sur le 1er token
        LEX.init_from_file(filepath)
        self.arbre = self.I()

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

    def node_block_node(self, enfants):
        n = Node(NodeTypes.node_block)
        for enfant in enfants:
            n.ajouter_enfant(enfant)
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

    def I(self):
        if LEX.check(TokenType.tok_debug):
            N = self.E(0)
            LEX.accept(TokenType.tok_point_virgule)
            return self.node_1_enfant(NodeTypes.node_debug, "debug", N)
        elif LEX.check(TokenType.tok_accolade_ouvrante):
            LEX.accept(TokenType.tok_accolade_ouvrante)  # Consommer l'accolade ouvrante
            N = Node(NodeTypes.node_block, 0, "")
            enfants = []
            while not LEX.check(TokenType.tok_accolade_fermeante) and LEX.T and LEX.T.type != TokenType.tok_eof:
                child = self.I()
                if child is None:
                    break
                enfants.append(child)
            LEX.accept(TokenType.tok_accolade_fermeante)  # Consommer l'accolade fermante
            return self.node_block_node(enfants)
        else:
            N = self.E(0)
            LEX.accept(TokenType.tok_point_virgule)
            return self.node_1_enfant(NodeTypes.node_drop, "drop", N)

   
        
