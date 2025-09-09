# -*- coding: utf-8 -*-
import AnalyseurLexicale as LEX
from AnalyseurLexicale import TokenType
from ast_nodes import Node, NodeTypes
from ops import OP   # table opérateurs: prio/parg/Ntype (inclure '=' prio 1 → nd_affect)

class AnalyseurSyntaxique:
    def __init__(self, filepath):
        # init pédagogique : LEX.T positionné sur le 1er token
        LEX.init_from_file(filepath)
        # Programme = séquence d'instructions jusqu'à EOF
        self.arbre = self.Programme()

    # --- helpers pour fabriquer les nœuds ---
    def node_valeur(self, type, valeur, chaine=""):
        return Node(type, valeur, chaine)

    def node_1_enfant(self, type, enfant):
        n = Node(type)
        n.ajouter_enfant(enfant)
        return n

    def node_2_enfants(self, type, gauche, droite):
        n = Node(type)
        n.ajouter_enfant(gauche)
        n.ajouter_enfant(droite)
        return n

    def node_block(self, enfants):
        n = Node(NodeTypes.node_block)
        for e in enfants:
            n.ajouter_enfant(e)
        return n

    # --- grammaire des expressions (cours 3) ---
    def E(self, prio):
        N = self.P()
        while LEX.T and (LEX.T.type in OP):
            entry = OP[LEX.T.type]
            if entry["prio"] < prio:
                break
            op_tok = LEX.T.type
            LEX.match(op_tok)                 # consomme l’opérateur courant
            M = self.E(entry["parg"])         # assoc/priority par table
            N = self.node_2_enfants(entry["Ntype"], N, M)
        return N

    def P(self):
        # +x -> x ; -x -> (0 - x)
        if LEX.T and LEX.T.type == TokenType.tok_moins:
            LEX.match(TokenType.tok_moins)
            sous = self.P()
            zero = self.node_valeur(NodeTypes.nd_const, 0, "0")
            return self.node_2_enfants(NodeTypes.nd_sub, zero, sous)
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

        elif LEX.check(TokenType.tok_ident):
            tok = LEX.T
            LEX.match(TokenType.tok_ident)
            # ident → nd_ref(name) (cours 5)
            return self.node_valeur(NodeTypes.node_reference, 0, tok.chaine)

        else:
            LEX.erreur(f"Atome attendu, trouvé: {(LEX.T.type.name if LEX.T else 'None')}")
            return None

    # --- grammaire des instructions (cours 4/5) ---
    # I → debug E ; | { I* } | int ident ; | E ;
    def I(self):
        # debug E ;
        if LEX.check(TokenType.tok_debug):
            LEX.accept(TokenType.tok_debug)
            N = self.E(0)
            LEX.accept(TokenType.tok_point_virgule)
            return self.node_1_enfant(NodeTypes.node_debug, N)

        # { I* }
        if LEX.check(TokenType.tok_accolade_ouvrante):
            LEX.accept(TokenType.tok_accolade_ouvrante)
            enfants = []
            while not LEX.check(TokenType.tok_accolade_fermeante):
                enfants.append(self.I())
            LEX.accept(TokenType.tok_accolade_fermeante)
            return self.node_block(enfants)

        # int ident ;
        if LEX.check(TokenType.tok_int):
            LEX.accept(TokenType.tok_int)
            if not LEX.check(TokenType.tok_ident):
                LEX.erreur("identifiant attendu après 'int'")
                return None
            name_tok = LEX.T
            LEX.accept(TokenType.tok_ident)
            LEX.accept(TokenType.tok_point_virgule)
            # nd_decl(name)
            return self.node_valeur(NodeTypes.node_declare, 0, name_tok.chaine)
        # I <- ... | if(E) I(else I)?
        if LEX.check(TokenType.tok_if):
            LEX.accept(TokenType.tok_if)
            LEX.accept(TokenType.tok_parenthese_ouvrante)
            cond = self.E(0)
            LEX.accept(TokenType.tok_parenthese_fermeante)

            then_branch = self.I()

            else_branch = None
            if LEX.check(TokenType.tok_else):
                LEX.accept(TokenType.tok_else)
                else_branch = self.I()

            n = Node(NodeTypes.node_if)            # = "condi" dans tes notes
            n.ajouter_enfant(cond)                 # enfants[0] = E (test)
            n.ajouter_enfant(then_branch)          # enfants[1] = I1 (cas vrai)
            if else_branch is not None:
                n.ajouter_enfant(else_branch)      # enfants[2] = I2 (cas faux, optionnel)
            return n
        # par défaut : E ; (instruction expression → drop)
        N = self.E(0)
        LEX.accept(TokenType.tok_point_virgule)
        return self.node_1_enfant(NodeTypes.node_drop, N)

    # Programme : séquence d’instructions jusqu’à EOF, empaquetée dans un block racine
    def Programme(self):
        instrs = []
        while LEX.T and LEX.T.type != TokenType.tok_eof:
            instrs.append(self.I())
        return self.node_block(instrs)
