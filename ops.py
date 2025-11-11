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

    func_name_node = n.enfants[0]
    body_node = n.enfants[-1]
    nb_params = len(n.enfants) - 2  
    nb_vars = getattr(n, "nbvar", 0)

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

    target = n.enfants[0]  
    cond_node = n.enfants[1]  
    E1 = cond_node.enfants[0]  
    I1 = cond_node.enfants[1]  

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


OP = {
    # 6 
    TokenType.tok_etoile: { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_etoile },
    TokenType.tok_slash:  { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_slash },
    TokenType.tok_modulo: { "prio": 6, "parg": 7, "Ntype": NodeTypes.node_modulo },

    # 5 
    TokenType.tok_plus:   { "prio": 5, "parg": 6, "Ntype": NodeTypes.node_plus },
    TokenType.tok_moins:  { "prio": 5, "parg": 6, "Ntype": NodeTypes.node_moins },

    # 4 
    TokenType.tok_egal_egal:      { "prio": 4, "parg": 5, "Ntype": NodeTypes.node_egal_egal },
    TokenType.tok_différent:      { "prio": 4, "parg": 5, "Ntype": NodeTypes.node_différent },
    TokenType.tok_supérieur:      { "prio": 4, "parg": 5, "Ntype": NodeTypes.node_supérieur },
    TokenType.tok_inférieur:      { "prio": 4, "parg": 5, "Ntype": NodeTypes.node_inférieur },
    TokenType.tok_supérieur_egal: { "prio": 4, "parg": 5, "Ntype": NodeTypes.node_supérieur_egal },
    TokenType.tok_inférieur_egal: { "prio": 4, "parg": 5, "Ntype": NodeTypes.node_inférieur_egal },

    # 3    
    TokenType.tok_et: { "prio": 3, "parg": 4, "Ntype": NodeTypes.node_et },

    # 2 
    TokenType.tok_ou: { "prio": 2, "parg": 3, "Ntype": NodeTypes.node_ou },

    # 1 
    TokenType.tok_egal: { "prio": 1, "parg": 1, "Ntype": NodeTypes.node_affect },
}


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

    NodeTypes.node_supérieur:      lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["cmpgt"],
    NodeTypes.node_inférieur:      lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["cmplt"],
    NodeTypes.node_supérieur_egal: lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["cmpge"],
    NodeTypes.node_inférieur_egal: lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["cmple"],
    NodeTypes.node_egal_egal:      lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["cmpeq"],
    NodeTypes.node_différent:      lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["cmpne"],

    NodeTypes.node_et:             lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["and"],
    NodeTypes.node_ou:             lambda n: GenNode(n.enfants[0]) + GenNode(n.enfants[1]) + ["or"],
    NodeTypes.node_not:            lambda n: GenNode(n.enfants[0]) + ["not"],

    # Instructions
    NodeTypes.node_block:          lambda n: sum((GenNode(child) for child in n.enfants), []),  # PAS de start/halt ici
    NodeTypes.node_debug:          lambda n: GenNode(n.enfants[0]) + ["dbg"],
    NodeTypes.node_drop:           lambda n: GenNode(n.enfants[0]) + ["drop 1"],
    NodeTypes.node_declare:        lambda n: [],  # alloc gérée globalement (resn/drop)
    NodeTypes.node_return:        lambda n: GenNode(n.enfants[0]) + ["ret"],
    NodeTypes.node_affect: None, 
    
    # if(E) I(else I)? 
    NodeTypes.node_cond: NF_cond    ,
    NodeTypes.node_loop: NF_loop    ,
    NodeTypes.node_break: NF_break  ,
    NodeTypes.node_continue: lambda n: [f"jump LOOP_START_{NB_LOOP}"],
    NodeTypes.node_target:   lambda n: [], 

    #fonction et appel
    NodeTypes.node_fonction: NF_fonction,
    NodeTypes.node_call: NF_call,
    
    # pointeurs et tableaux
    NodeTypes.node_indirection: lambda n: GenNode(n.enfants[0]) + ["read"],
    NodeTypes.node_address: None, 
    NodeTypes.node_array_access: lambda n: (
        [f"push {n.enfants[0].valeur}"] +  
        GenNode(n.enfants[1]) +                     
        ["add", "read"]                     
    ),


}

def NF_affect(n):
    lhs, rhs = n.enfants[0], n.enfants[1]
    
    if lhs.type == NodeTypes.node_indirection:
        return GenNode(lhs.enfants[0]) + GenNode(rhs) + ["swap", "write", "push 0"]
    
    elif lhs.type == NodeTypes.node_array_access:
        return (
            [f"push {lhs.enfants[0].valeur}"] +  
            GenNode(lhs.enfants[1]) +            
            ["add"] +                            
            GenNode(rhs) +                       
            ["swap", "write", "push 0"]          
        )
    
    else:
        return GenNode(rhs) + ["dup", f"set {lhs.valeur}"]

NF[NodeTypes.node_affect] = NF_affect

def NF_address(n):
    child = n.enfants[0]
    
    if child.type == NodeTypes.node_array_access:
        return (
            [f"push {child.enfants[0].valeur}"] +  
            GenNode(child.enfants[1]) +            
            ["add"]                                
        )
    
    else:
        return [f"push {child.valeur}"]

NF[NodeTypes.node_address] = NF_address


def GenNode(n: Node):
    if n is None:
        return []
    fn = NF.get(n.type)
    if fn is not None:
        return fn(n)
    return _emit_children(n)
