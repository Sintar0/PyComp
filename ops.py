# -*- coding: utf-8 -*-
from AnalyseurLexicale import TokenType
from ast_nodes import NodeTypes, Node

NB_LABEL = 0
NB_LOOP = 0

def NF_call(n: Node):
    func_name_node = n.enfants[0]
    nb_args = len(n.enfants) - 1
    func_label = func_name_node.chaine
    code = [f"prep {func_label}"]
    for arg in n.enfants[1:]:
        code += GenNode(arg)
    code += [f"call {nb_args}"]
    return code



def NF_fonction(n: Node):
    '''
    fonction ; label idente + nbvars
    resn [nb vars]
    I
    push 0
    ret

    '''
    func_name_node = n.enfants[0]
    body_node = n.enfants[-1]
    nb_params = len(n.enfants) - 2  # exclut le nom et le corps
    nb_vars = getattr(n, "nbvar", 0)  # Récupère le nombre de variables locales annoté par l'analyseur sémantique

    func_label = func_name_node.chaine
    code = []
    code += [f".{func_label}"]
    code += [f"resn {nb_params + nb_vars}"]
    code += GenNode(body_node)
    return code




def NF_loop(n: Node):
    global NB_LOOP
    NB_LOOP += 1
    loop_id = NB_LOOP

    # enfants: [target, cond_node]
    target = n.enfants[0]  # node_target (vide)
    cond_node = n.enfants[1]  # node_cond
    E1 = cond_node.enfants[0]  # condition
    I1 = cond_node.enfants[1]  # corps

    start_lbl = f"LOOP_START_{loop_id}"
    end_lbl = f"LOOP_END_{loop_id}"

    code = []
    code += [f".{start_lbl}"]
    # E1 (condition)
    code += GenNode(E1)
    code += [f"jumpf {end_lbl}"]
    # I1 (corps de la boucle)
    code += GenNode(I1)
    code += [f"jump {start_lbl}"]
    code += [f".{end_lbl}"]
    return code

def NF_break(n: Node):
    return [f"jump LOOP_END_{NB_LOOP}"]

def NF_cond(n: Node):
    # enfants: [E, I1, (I2?)]
    cond = n.enfants[0]
    then_branch = n.enfants[1]
    has_else = len(n.enfants) >= 3

    else_lbl = next_label()
    end_lbl  = next_label() if has_else else else_lbl

    code = []
    # E
    code += GenNode(cond)
    code += [f"jumpf {else_lbl}"]
    # I1 (cas vrai)
    code += GenNode(then_branch)
    if has_else:
        code += [f"jump {end_lbl}"]
        code += [f".{else_lbl}"]
        # I2 (cas faux)
        code += GenNode(n.enfants[2])
        code += [f".{end_lbl}"]
    else:
        code += [f".{else_lbl}"]
    return code

def next_label():
    global NB_LABEL
    NB_LABEL += 1
    return f"L{NB_LABEL}"

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
    NodeTypes.node_return:        lambda n: GenNode(n.enfants[0]) + ["ret"],


    # affect: lhs=ref(name/index), rhs=expr
    NodeTypes.node_affect:         lambda n: (
        GenNode(n.enfants[1]) + ["dup", f"set {n.enfants[0].valeur}"]
    ),
    
    # if(E) I(else I)? 
    NodeTypes.node_cond: NF_cond    ,
    NodeTypes.node_loop: NF_loop    ,
    NodeTypes.node_break: NF_break  ,
    NodeTypes.node_continue: lambda n: [f"jump LOOP_START_{NB_LOOP}"],
    NodeTypes.node_target:   lambda n: [],  # <--- Corrigé : ne déclare plus le label ici

    #fonction et appel
    NodeTypes.node_fonction: NF_fonction,
    NodeTypes.node_call: NF_call,


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
