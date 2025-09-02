from AnalyseurLexicale import TokenType, Token, T, next, init_from_file, erreur

class Node:
    def __init__(self, type, valeur, chaine, enfants=None):
        self.type = type 
        self.valeur = valeur
        self.chaine = chaine
        self.enfants = enfants if enfants else []

    def ajouter_enfant(self, enfant):
        self.enfants.append(enfant)

    def afficher(self, indent=0):
        print("  " * indent + f"({self.type.name}, valeur={self.valeur}, chaine='{self.chaine}')")
        for enfant in self.enfants:
            enfant.afficher(indent + 1)

class AnalyseurSyntaxique:
    def __init__(self, filepath):
        init_from_file(filepath)
        global T
        T = next()  # <<< On consomme le premier token ICI
        print(f"[DEBUG] Démarrage analyse syntaxique, premier token : {T.type.name}")
        self.arbre = self.E()
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

    def P(self):
        global T
        if T.type == TokenType.tok_moins:
            T = next()
            sous_arbre = self.P()
            return self.node_1_enfant(TokenType.tok_moins, "-", sous_arbre)
        elif T.type == TokenType.tok_plus:
            T = next()
            sous_arbre = self.P()
            return self.node_1_enfant(TokenType.tok_plus, "+", sous_arbre)
        else:
            return self.S()

    def E(self):
        return self.P()

    
    def S(self):
        return self.A()

    def A(self):
        global T
        if T.type == TokenType.tok_const:
            token = T
            T = next()
            return self.node_valeur(TokenType.tok_const, token.valeur, token.chaine)
        elif T.type == TokenType.tok_parenthese_ouvrante:
            T = next()
            sous_arbre = self.E()
            if T.type != TokenType.tok_parenthese_fermeante:
                erreur("Parenthèse fermante manquante")
                return None
            T = next()
            return sous_arbre
        elif T.type == TokenType.tok_eof:
            return None
        else:
            erreur(f"Expression atomique attendue, trouvé: {T.type.name}")
            return None
