# -*- coding: utf-8 -*-
from ast_nodes import NodeTypes

# Pile de tables (un dict par bloc)
_TS_STACK = []
NBvar = 0  # compteur global de variables (indexation)

class SemError(Exception):
    pass

def beginBlock():
    _TS_STACK.append({})

def endBlock():
    if not _TS_STACK:
        raise SemError("endBlock() sans beginBlock()")
    _TS_STACK.pop()

def declare(name: str):
    if not _TS_STACK:
        beginBlock()
    cur = _TS_STACK[-1]
    if name in cur:
        raise SemError(f"Double déclaration dans le même bloc: '{name}'")
    sym = {"name": name, "index": None}
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

    # nd_block : ouvre/ferme un scope et descend
    if t == NodeTypes.node_block:
        beginBlock()
        for c in N.enfants:
            SemNode(c)
        endBlock()
        return

    # nd_decl(name) : réserve un index
    if t == NodeTypes.node_declare:
        sym = declare(N.chaine)
        sym["index"] = NBvar
        NBvar += 1
        # on garde le nom dans N.chaine, pas besoin d'enfants
        return

    # nd_ref(name) : annote la valeur = index trouvé
    if t == NodeTypes.node_reference:
        sym = find(N.chaine)
        N.valeur = sym["index"]
        return

    # nd_call (fonction)
    if t == NodeTypes.node_call:
        # vérifier que le nom de la fonction est bien déclaré
        if len(N.enfants) < 1:
            raise SemError("Appel de fonction mal formé")
        func_name_node = N.enfants[0]
        if func_name_node.type != NodeTypes.node_reference:
            raise SemError("Le nom de la fonction doit être une référence")
        find(func_name_node.chaine)  # Vérifie que la fonction est déclarée
        # Traiter les arguments
        for arg in N.enfants[1:]:
            SemNode(arg)
        return
    if t == NodeTypes.node_function:
        if len(N.enfants) < 2:
            raise SemError("Définition de fonction mal formée")
        func_name_node = N.enfants[0]
        if func_name_node.type != NodeTypes.node_reference:
            raise SemError("Le nom de la fonction doit être une référence")
        declare(func_name_node.chaine)  # Déclare la fonction
        beginBlock()  # Nouveau scope pour les paramètres et le corps
        # Traiter les paramètres
        for param in N.enfants[1:-1]:
            if param.type != NodeTypes.node_declare:
                raise SemError("Les paramètres doivent être des déclarations")
            SemNode(param)
        # Traiter le corps de la fonction
        SemNode(N.enfants[-1])
        endBlock()
        return

    # autres : descente simple
    for c in N.enfants:
        SemNode(c)


    # nd_affect(ref, expr) : check que gauche=ref, sémantique des enfants
    if t == NodeTypes.node_affect:
        if len(N.enfants) < 2:
            raise SemError("Affectation mal formée")
        lhs, rhs = N.enfants[0], N.enfants[1]
        SemNode(lhs)
        SemNode(rhs)
        if lhs.type != NodeTypes.node_reference:
            raise SemError("LHS d'une affectation doit être une référence")
        return

    # autres : descente simple
    for c in N.enfants:
        SemNode(c)
