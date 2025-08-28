from enum import Enum
from AnalyseurLexicale import *

class Node:
    def __init__(self, type,nombre_enfants, valeur, chaine, enfants):
        self.type = type 
        self.valeur = valeur
        self.chaine = chaine
        self.enfants = enfants
        self.nombre_enfants = nombre_enfants
    
    def create_node_id(self, type, valeur, chaine, enfants):
        return Node(type, valeur, chaine, enfants)

    def ajouter_enfant(self, enfant):
        self.enfants.append(enfant) 
        self.nombre_enfants += 1

    def afficher(self):
        print("(",self.type,)
        for enfant in self.enfants:
            print(" ",end="") 
            enfant.afficher()
        print(")")

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

class AnalyseurSyntaxique:
    def __init__(self, filepath):
        self.filepath = filepath
        # On appel le init_from_file de l'analyseur lexicale
        init_from_file(filepath)
        # tant que j'ai des token dans T, on les traite en créant des arbres
        while T.type != TokenType.tok_eof:
            self.arbre.afficher()
            T = next()

    def node_valeur(self,type : str, valeur : int, chaine : str):
        return Node(type, valeur, chaine, [])

    def node_1_enfant(self,type : str, valeur : int, chaine : str):
        node = Node(type, valeur, chaine, [])
        node.ajouter_enfant(self.node_2(NodeTypes.node_2, 0, ""))
        return node

    def node_2_enfants(self,type : str, valeur : int, chaine : str):
        node = Node(type, valeur, chaine, [])
        node.ajouter_enfant(self.node_2(NodeTypes.node_2, 0, ""))
        node.ajouter_enfant(self.node_2(NodeTypes.node_2, 0, ""))
        return node

    def P(self):
        # pour l'instant je n'ais pas d'opérateur binaire
        if(check(TokenType.tok_ident)):
            # On regarde si le tocken est un prefixe
            if(check(TokenType.tok_addr)):
                return self.node_1_enfant(NodeTypes.node_addr, T.valeur, T.chaine)
            elif(check(TokenType.tok_etoile)):
                return self.node_1_enfant(NodeTypes.node_etoile, T.valeur, T.chaine)
            else:
                return self.node_1_enfant(NodeTypes.node_ident, T.valeur, T.chaine)
        return  # je délègue à E qui gère les expressions sur qui je peux mettre un prefixe
    
    def E(self):
        # pour l'instant je n'ais pas d'opérateur binaire
        return P() # je délègue à P qui gère les expressions sur qui je peux mettre un prefixe
    
    def S(self):
        return A()

    def A(self):
        if(check(TokenType.tok_const)):
            return self.node_valeur(NodeTypes.node_const, T.valeur, T.chaine)
