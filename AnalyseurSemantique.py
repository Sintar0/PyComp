from ast_nodes import NodeTypes

_TS_STACK = []
NBvar = 0  

class SemError(Exception):
    pass

def beginBlock():
    _TS_STACK.append({})

def endBlock():
    if not _TS_STACK:
        raise SemError("endBlock() sans beginBlock()")
    _TS_STACK.pop()

def declare(name: str, type="var"):
    if not _TS_STACK:
        beginBlock()
    cur = _TS_STACK[-1]
    if name in cur:
        raise SemError(f"Double déclaration dans le même bloc: '{name}'")
    sym = {"name": name, "index": None, "type": type}
    cur[name] = sym
    return sym

def find(name: str):
    for scope in reversed(_TS_STACK):
        if name in scope:
            return scope[name]
    raise SemError(f"Identifiant non déclaré: '{name}'")

def SemNode(N):
    global NBvar
    if N is None:
        return

    t = N.type

    if t == NodeTypes.node_block:
        beginBlock()
        for c in N.enfants:
            SemNode(c)
        endBlock()
        return

    if t == NodeTypes.node_declare:
        sym = declare(N.chaine)
        sym["index"] = NBvar
        NBvar += 1
        return

    if t == NodeTypes.node_reference:
        sym = find(N.chaine)
        N.valeur = sym["index"]
        return
    if t == NodeTypes.node_call:
        if len(N.enfants) < 1:
            raise SemError("Appel de fonction mal formé")
        func_name_node = N.enfants[0]
        if func_name_node.type != NodeTypes.node_reference:
            raise SemError("Le nom de la fonction doit être une référence")
        sym = find(func_name_node.chaine)
        if sym["type"] != "fonction":
            raise SemError(f"'{func_name_node.chaine}' n'est pas une fonction")
        for arg in N.enfants[1:]:
            SemNode(arg)
        return
    if t == NodeTypes.node_fonction:
        if len(N.enfants) < 2:
            raise SemError("Déclaration de fonction mal formée")
        func_name_node = N.enfants[0]
        if func_name_node.type != NodeTypes.node_reference:
            raise SemError("Le nom de la fonction doit être une référence")
        declare(func_name_node.chaine, "fonction")
        saved_nbvar = NBvar
        NBvar = 0
        beginBlock()
        for param in N.enfants[1:-1]: 
            if param.type != NodeTypes.node_reference:
                raise SemError("Les paramètres de la fonction doivent être des références")
            sym = declare(param.chaine, "var")
            sym["index"] = NBvar
            NBvar += 1
        body = N.enfants[-1]
        SemNode(body)
        endBlock()
        N.nbvar = NBvar 
        NBvar = saved_nbvar 
        return
    
    if t == NodeTypes.node_indirection:
        SemNode(N.enfants[0])
        return
    
    if t == NodeTypes.node_address:
        SemNode(N.enfants[0])
        return
    
    if t == NodeTypes.node_array_access:
        SemNode(N.enfants[0])  
        SemNode(N.enfants[1])  
        return
    
    for c in N.enfants:
        SemNode(c)

    if t == NodeTypes.node_affect:
        if len(N.enfants) < 2:
            raise SemError("Affectation mal formée")
        lvalue, rvalue = N.enfants[0], N.enfants[1]
        SemNode(lvalue)
        SemNode(rvalue)
        if lvalue.type not in [NodeTypes.node_reference, NodeTypes.node_indirection, NodeTypes.node_array_access]:
            raise SemError("La lvalue d'une affectation doit être une référence, *p ou arr[i]")
        return

    for c in N.enfants:
        SemNode(c)
