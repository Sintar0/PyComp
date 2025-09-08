# -*- coding: utf-8 -*-
from AnalyseurLexicale import TokenType
from ast_nodes import NodeTypes, Node

# ---------------------------
# Priorités (cours) 6..1
# ---------------------------
OP = {
    # 6 : *, /, %
    TokenType.tok_etoile: { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_etoile },
    TokenType.tok_slash:  { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_slash },
    TokenType.tok_modulo: { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_modulo },

    # 5 : +, -
    TokenType.tok_plus:   { "prio": 5, "parg": 6, "Ntype": NodeTypes.node_plus },
    TokenType.tok_moins:  { "prio": 5, "parg": 6, "Ntype": NodeTypes.node_moins },

    # 4 : comparaisons
    TokenType.tok_egal_egal:      { "prio": 4, "parg": 5, "Ntype": NodeTypes.node_egal_egal },
    TokenType.tok_différent:      { "prio": 4, "parg": 5, "Ntype": NodeTypes.node_différent },
    TokenType.tok_supérieur:      { "prio": 4, "parg": 5, "Ntype": NodeTypes.node_supérieur },
    TokenType.tok_inférieur:      { "prio": 4, "parg": 5, "Ntype": NodeTypes.node_inférieur },
    TokenType.tok_supérieur_egal: { "prio": 4, "parg": 5, "Ntype": NodeTypes.node_supérieur_egal },
    TokenType.tok_inférieur_egal: { "prio": 4, "parg": 5, "Ntype": NodeTypes.node_inférieur_egal },

    # 3 : &&
    TokenType.tok_et: { "prio": 3, "parg": 4, "Ntype": NodeTypes.node_et },

    # 2 : ||
    TokenType.tok_ou: { "prio": 2, "parg": 3, "Ntype": NodeTypes.node_ou },

    # 1 : =  (assoc. droite → parg = prio)
    TokenType.tok_egal: { "prio": 1, "parg": 1, "Ntype": NodeTypes.node_affect },
}

# ---------------------------
# NF : “nœuds faciles”
# ---------------------------
def _emit_children(n):
    code = []
    for c in n.enfants:
        code += GenNode(c)
    return code

NF = {
    # Expressions
    NodeTypes.node_const:          lambda n: [f"push {n.valeur}"],
    NodeTypes.node_reference:      lambda n: [f"get {n.valeur}"],

    NodeTypes.node_plus:           lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["add"],
    NodeTypes.node_moins:          lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["sub"],
    NodeTypes.node_etoile:         lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["mul"],
    NodeTypes.node_slash:          lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["div"],
    NodeTypes.node_modulo:         lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["mod"],

    NodeTypes.node_supérieur:      lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["gt"],
    NodeTypes.node_inférieur:      lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["lt"],
    NodeTypes.node_supérieur_egal: lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["ge"],
    NodeTypes.node_inférieur_egal: lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["le"],
    NodeTypes.node_egal_egal:      lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["eq"],
    NodeTypes.node_différent:      lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["ne"],

    NodeTypes.node_et:             lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["and"],
    NodeTypes.node_ou:             lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["or"],

    # Instructions
    NodeTypes.node_block:          lambda n: sum((GenNode(child) for child in n.enfants), []),  # PAS de start/halt ici
    NodeTypes.node_debug:          lambda n: GenNode(n.enfants[0]) + ["dbg"],
    NodeTypes.node_drop:           lambda n: GenNode(n.enfants[0]) + ["drop 1"],
    NodeTypes.node_declare:        lambda n: [],  # alloc gérée globalement (resn/drop)

    # affect: lhs=ref(name/index), rhs=expr
    NodeTypes.node_affect:         lambda n: (
        GenNode(n.enfants[1]) + ["dup", f"set {n.enfants[0].valeur}"]
    ),
}

# ---------------------------
# Générateur unique
# ---------------------------
def GenNode(n: Node):
    """Parcours post-ordre + émission via NF (liste plate d'instructions)."""
    if n is None:
        return []
    # si le type est directement dans NF, déléguer (les lambdas appellent GenNode pour les enfants)
    fn = NF.get(n.type)
    if fn is not None:
        return fn(n)
    # fallback générique (au cas où un type ne serait pas dans NF)
    return _emit_children(n)
