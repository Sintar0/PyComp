# -*- coding: utf-8 -*-
from AnalyseurLexicale import TokenType
from ast_nodes import NodeTypes, Node

# Table des opérateurs (Pratt-like) :
# prio: plus grand => plus prioritaire ; parg = prio+1 => associativité gauche
OP = {
    # *, /, %
    TokenType.tok_etoile: {"prio": 60, "parg": 61, "Ntype": NodeTypes.node_etoile},
    TokenType.tok_slash:  {"prio": 60, "parg": 61, "Ntype": NodeTypes.node_slash},
    TokenType.tok_modulo: {"prio": 60, "parg": 61, "Ntype": NodeTypes.node_modulo},

    # +, -
    TokenType.tok_plus:   {"prio": 50, "parg": 51, "Ntype": NodeTypes.node_plus},
    TokenType.tok_moins:  {"prio": 50, "parg": 51, "Ntype": NodeTypes.node_moins},

    # comparaisons
    TokenType.tok_egal_egal:      {"prio": 40, "parg": 41, "Ntype": NodeTypes.node_egal_egal},
    TokenType.tok_différent:      {"prio": 40, "parg": 41, "Ntype": NodeTypes.node_différent},
    TokenType.tok_supérieur:      {"prio": 40, "parg": 41, "Ntype": NodeTypes.node_supérieur},
    TokenType.tok_inférieur:      {"prio": 40, "parg": 41, "Ntype": NodeTypes.node_inférieur},
    TokenType.tok_supérieur_egal: {"prio": 40, "parg": 41, "Ntype": NodeTypes.node_supérieur_egal},
    TokenType.tok_inférieur_egal: {"prio": 40, "parg": 41, "Ntype": NodeTypes.node_inférieur_egal},

    # logiques
    TokenType.tok_et: {"prio": 30, "parg": 31, "Ntype": NodeTypes.node_et},
    TokenType.tok_ou: {"prio": 20, "parg": 21, "Ntype": NodeTypes.node_ou},
}

# Table NF (noeuds faciles) pour génération postfixe sur VM à pile
NF = {
    NodeTypes.node_const: lambda n: [f"push {n.valeur}"],
    NodeTypes.node_plus:  lambda n: ["add"],
    NodeTypes.node_moins: lambda n: ["sub"],
    NodeTypes.node_etoile:lambda n: ["mul"],
    NodeTypes.node_slash: lambda n: ["div"],
    NodeTypes.node_modulo:lambda n: ["mod"],

    NodeTypes.node_supérieur:      lambda n: ["gt"],
    NodeTypes.node_inférieur:      lambda n: ["lt"],
    NodeTypes.node_supérieur_egal: lambda n: ["ge"],
    NodeTypes.node_inférieur_egal: lambda n: ["le"],
    NodeTypes.node_egal_egal:      lambda n: ["eq"],
    NodeTypes.node_différent:      lambda n: ["ne"],

    NodeTypes.node_et: lambda n: ["and"],
    NodeTypes.node_ou: lambda n: ["or"],

    NodeTypes.node_block: lambda n: ["start"] + sum([GenNode(child) for child in n.enfants], []) + ["halt"],
    NodeTypes.node_debug: lambda n: GenNode(n.enfants[0]) + ["dbg"],
    NodeTypes.node_drop: lambda n: GenNode(n.enfants[0]) + ["drop 1"],
}

def GenNode(n: Node):
    """Parcours post-ordre + émission via NF."""
    if n is None:
        return []
    # feuille
    if n.type == NodeTypes.node_const:
        return NF[n.type](n)
    # n-aire
    code = []
    for child in n.enfants:
        code.extend(GenNode(child))
    if n.type in NF:
        code.extend(NF[n.type](n))
    return code
