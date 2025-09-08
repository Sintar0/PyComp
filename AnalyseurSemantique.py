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
