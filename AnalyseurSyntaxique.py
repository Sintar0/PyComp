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
        # *P -> indirection (déréférencement)
        if LEX.T and LEX.T.type == TokenType.tok_etoile:
            LEX.match(TokenType.tok_etoile)
            sous = self.P()
            return self.node_1_enfant(NodeTypes.node_indirection, sous)
        # &P -> adresse de
        elif LEX.T and LEX.T.type == TokenType.tok_addr:
            LEX.match(TokenType.tok_addr)
            sous = self.P()
            return self.node_1_enfant(NodeTypes.node_address, sous)
        # !P -> négation logique
        elif LEX.T and LEX.T.type == TokenType.tok_not:
            LEX.match(TokenType.tok_not)
            sous = self.P()
            return self.node_1_enfant(NodeTypes.node_not, sous)
        # -x -> (0 - x)
        elif LEX.T and LEX.T.type == TokenType.tok_moins:
            LEX.match(TokenType.tok_moins)
            sous = self.P()
            zero = self.node_valeur(NodeTypes.node_const, 0, "0")
            return self.node_2_enfants(NodeTypes.node_moins, zero, sous)
        # +x -> x
        elif LEX.T and LEX.T.type == TokenType.tok_plus:
            LEX.match(TokenType.tok_plus)
            return self.P()
        else:
            return self.S()

    def S(self):
        # Gérer [E]A (notation préfixe pour tableaux)
        if LEX.T and LEX.T.type == TokenType.tok_croche_ouvrante:
            LEX.match(TokenType.tok_croche_ouvrante)
            index = self.E(0)
            if not LEX.match(TokenType.tok_croche_fermeante):
                LEX.erreur("']' attendu")
                return None
            base = self.A()
            return self.node_2_enfants(NodeTypes.node_array_access, base, index)
        
        N = self.A()
        
        # Gérer A[E] (notation postfixe pour tableaux)
        if LEX.T and LEX.T.type == TokenType.tok_croche_ouvrante:
            LEX.match(TokenType.tok_croche_ouvrante)
            index = self.E(0)
            if not LEX.match(TokenType.tok_croche_fermeante):
                LEX.erreur("']' attendu")
                return None
            return self.node_2_enfants(NodeTypes.node_array_access, N, index)
        
        # Gérer A(...) (appels de fonction)
        if LEX.T and LEX.T.type == TokenType.tok_parenthese_ouvrante:
            LEX.match(TokenType.tok_parenthese_ouvrante)
            args = []
            if LEX.T and LEX.T.type != TokenType.tok_parenthese_fermeante:
                while True:
                    arg = self.E(0)
                    args.append(arg)
                    if LEX.T and LEX.T.type == TokenType.tok_virgule:
                        LEX.match(TokenType.tok_virgule)
                    else:
                        break
            if not LEX.match(TokenType.tok_parenthese_fermeante):
                LEX.erreur("')' attendu")
                return None
            # nd_call (fonction, args...)
            call_node = Node(NodeTypes.node_call)
            call_node.ajouter_enfant(N)  # fonction
            for a in args:
                call_node.ajouter_enfant(a)  # arguments
            return call_node
        return N

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
        
    # F → int ident ( (int ident (, int ident)*)? ) I
    def F(self):
        
        '''
        accept(tok_int);
        accept(tok_ident);
        LAST = tok_ident
        accept(tok_parenthese_ouvrant);
        if(!check(tok_parenthese_ouvrant)){
        do{accept(tok_int);
        accept(tok_ident);
        }
        while(check(tok_virgule))
        accept(tok_parentèse_fermante)
        }
        I();
        '''
        LEX.accept(TokenType.tok_int)
        if not LEX.check(TokenType.tok_ident):
            LEX.erreur("identifiant attendu après 'int'")
            return None
        LAST = LEX.T
        LEX.accept(TokenType.tok_ident)
        LEX.accept(TokenType.tok_parenthese_ouvrante)
        params = []
        if not LEX.check(TokenType.tok_parenthese_fermeante):
            while True:
                LEX.accept(TokenType.tok_int)
                if not LEX.check(TokenType.tok_ident):
                    LEX.erreur("identifiant attendu après 'int'")
                    return None
                param_tok = LEX.T
                params.append(param_tok.chaine)
                LEX.accept(TokenType.tok_ident)
                if LEX.check(TokenType.tok_virgule):
                    LEX.accept(TokenType.tok_virgule)
                else:
                    break
        LEX.accept(TokenType.tok_parenthese_fermeante)
        body = self.I()
        func_node = Node(NodeTypes.node_fonction)
        func_node.ajouter_enfant(self.node_valeur(NodeTypes.node_reference, 0, LAST.chaine))  # nom de la fonction
        for p in params:
            func_node.ajouter_enfant(self.node_valeur(NodeTypes.node_reference, 0, p))  # paramètres
        func_node.ajouter_enfant(body)  # corps de la fonction
        return func_node
    

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

        # int *p ; ou int **p ; (déclarations de pointeurs)
        if LEX.check(TokenType.tok_int):
            LEX.accept(TokenType.tok_int)
            # Compter les étoiles pour les pointeurs
            nb_stars = 0
            while LEX.check(TokenType.tok_etoile):
                LEX.accept(TokenType.tok_etoile)
                nb_stars += 1
            if not LEX.check(TokenType.tok_ident):
                LEX.erreur("identifiant attendu après 'int'")
                return None
            name_tok = LEX.T
            LEX.accept(TokenType.tok_ident)
            LEX.accept(TokenType.tok_point_virgule)
            # nd_decl(name) avec nb_stars dans valeur
            return self.node_valeur(NodeTypes.node_declare, nb_stars, name_tok.chaine)
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

            n = Node(NodeTypes.node_cond)            # = "condi" dans tes notes
            n.ajouter_enfant(cond)                 # enfants[0] = E (test)
            n.ajouter_enfant(then_branch)          # enfants[1] = I1 (cas vrai)
            if else_branch is not None:
                n.ajouter_enfant(else_branch)      # enfants[2] = I2 (cas faux, optionnel)
            return n
       # while(E) I 
        if LEX.check(TokenType.tok_while):
            LEX.accept(TokenType.tok_while)
            LEX.accept(TokenType.tok_parenthese_ouvrante)
            E1 = self.E(0)  # condition
            LEX.accept(TokenType.tok_parenthese_fermeante)
            I1 = self.I()   # corps de la boucle
            break_node = Node(NodeTypes.node_break)
            cond_node = Node(NodeTypes.node_cond)
            cond_node.ajouter_enfant(E1)
            cond_node.ajouter_enfant(I1)
            cond_node.ajouter_enfant(break_node)
            target_node = Node(NodeTypes.node_target)
            loop_node = Node(NodeTypes.node_loop)
            loop_node.ajouter_enfant(target_node)
            loop_node.ajouter_enfant(cond_node)
            return loop_node

            # do I while (E) ;
        if LEX.check(TokenType.tok_do):
            LEX.accept(TokenType.tok_do)
            I1 = self.I()   # corps de la boucle
            LEX.accept(TokenType.tok_while)
            LEX.accept(TokenType.tok_parenthese_ouvrante)
            E1 = self.E(0)  # condition
            LEX.accept(TokenType.tok_parenthese_fermeante)
            LEX.accept(TokenType.tok_point_virgule)

            node_target = Node(NodeTypes.node_target)

            seq_in_loop = Node(NodeTypes.node_sequence)
            seq_in_loop.ajouter_enfant(I1)
            seq_in_loop.ajouter_enfant(node_target)

            node_break = Node(NodeTypes.node_break)

            node_cond = Node(NodeTypes.node_cond)
            node_cond.ajouter_enfant(E1)
            node_cond.ajouter_enfant(seq_in_loop)
            node_cond.ajouter_enfant(node_break)

            node_loop = Node(NodeTypes.node_loop)
            node_loop.ajouter_enfant(node_target)  # ou None si pas utilisé
            node_loop.ajouter_enfant(node_cond)

            return node_loop
        
        
   
        
        # for (E1; E2; E3) I
        if LEX.check(TokenType.tok_for):
            LEX.accept(TokenType.tok_for)
            LEX.accept(TokenType.tok_parenthese_ouvrante)
            E1 = self.E(0)
            LEX.accept(TokenType.tok_point_virgule)
            E2 = self.E(0)
            LEX.accept(TokenType.tok_point_virgule)
            E3 = self.E(0)
            LEX.accept(TokenType.tok_parenthese_fermeante)
            I1 = self.I()

            # Construction de l'arbre
            node_drop_E1 = Node(NodeTypes.node_drop)
            node_drop_E1.ajouter_enfant(E1)

            node_drop_E3 = Node(NodeTypes.node_drop)
            node_drop_E3.ajouter_enfant(E3)

            node_target = Node(NodeTypes.node_target)

            seq_in_loop = Node(NodeTypes.node_sequence)
            seq_in_loop.ajouter_enfant(I1)
            seq_in_loop.ajouter_enfant(node_target)
            seq_in_loop.ajouter_enfant(node_drop_E3)

            node_break = Node(NodeTypes.node_break)

            node_cond = Node(NodeTypes.node_cond)
            node_cond.ajouter_enfant(E2)
            node_cond.ajouter_enfant(seq_in_loop)
            node_cond.ajouter_enfant(node_break)

            node_loop = Node(NodeTypes.node_loop)
            node_loop.ajouter_enfant(node_target)  # ou None si pas utilisé
            node_loop.ajouter_enfant(node_cond)

            node_seq = Node(NodeTypes.node_sequence)
            node_seq.ajouter_enfant(node_drop_E1)
            node_seq.ajouter_enfant(node_loop)

            return node_seq

        # continue ;
        if LEX.check(TokenType.tok_continue):
            LEX.accept(TokenType.tok_continue)
            LEX.accept(TokenType.tok_point_virgule)
            return Node(NodeTypes.node_continue)

        # break ;
        if LEX.check(TokenType.tok_break):
            LEX.accept(TokenType.tok_break)
            LEX.accept(TokenType.tok_point_virgule)
            return Node(NodeTypes.node_break)
        # I <- ... |return E ;
        if LEX.check(TokenType.tok_return):
            LEX.accept(TokenType.tok_return)
            N = self.E(0)
            LEX.accept(TokenType.tok_point_virgule)
            return self.node_1_enfant(NodeTypes.node_return, N)
        
        # par défaut : E ; (instruction expression → drop)
        N = self.E(0)
        LEX.accept(TokenType.tok_point_virgule)
        return self.node_1_enfant(NodeTypes.node_drop, N)

    


    # Programme : séquence d’instructions jusqu’à EOF, empaquetée dans un block racine
    # #je dois rajouter ça je sais pas comment faire
    #    debut Block
    #   tant qu'on est différent de EOF niveau token
    #   genCode()
    #   fin Block
    #   print("ident")
    def Programme(self):
        enfants = []
        while LEX.T and LEX.T.type != TokenType.tok_eof:
            if LEX.check(TokenType.tok_int):
                # Déclaration de fonction
                func_node = self.F()
                if func_node is not None:
                    enfants.append(func_node)
            else:
                instr = self.I()
                if instr is not None:
                    enfants.append(instr)
        return self.node_block(enfants)
    
    
       
        



        
