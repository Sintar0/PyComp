import sys
sys.stdout.reconfigure(encoding='utf-8')# -*- coding: utf-8 -*-
from AnalyseurSyntaxique import AnalyseurSyntaxique
import AnalyseurLexicale as LEX
from ops import GenNode           # GenNode doit gérer block/debug/drop/decl/ref/affect + expr
import AnalyseurSemantique as SEM  # ← passe sémantique réelle (C5)

DEBUG_LEXER = False

# Remap des comparaisons vers MSM (le reste passe tel quel)
MSM_MAP = {
    "gt": "cmpgt",
    "lt": "cmplt",
    "ge": "cmpge",
    "le": "cmple",
    "eq": "cmpeq",
    "ne": "cmpne",
}

def write_msm(program_instructions: list, out_path: str):
    """
    Écrit un assembleur MSM exécutable avec .start ... halt
    program_instructions : liste plate (ou imbriquée) de str comme 'push 3', 'add', 'set 0', etc.
    """
    def process_instruction(instr, file):
        if isinstance(instr, list):
            # 1) Si on lui donne une liste (potentiellement imbriquée),
            #    elle APPELLERA RECURSIVEMENT la fonction sur chaque élément.
            for item in instr:
                process_instruction(item, file)
        else:
            # 2) Sinon, elle suppose que c’est UNE INSTRUCTION sous forme de chaîne.
            parts = instr.split()
            op = parts[0]                           # le mnémonique (ex: "push", "add", "gt")
            arg = parts[1] if len(parts) > 1 else None  # l’argument optionnel (ex: "3", "0", …)

            # 3) Elle fait le REMAP vers la MSM pour les opé qui changent de nom.
            op_msm = MSM_MAP.get(op, op)            # ex: "gt" devient "cmpgt"; "add" reste "add"

            # 4) Elle EMET (écrit) la ligne dans le fichier .msm
            if arg is None:
                file.write(f"{op_msm}\n")           # ex: "add\n" ou "dbg\n"
            else:
                file.write(f"{op_msm} {arg}\n")     # ex: "push 3\n" ou "set 0\n"


    with open(out_path, "w", encoding="utf-8") as f:
        f.write(".start\n")
        for instr in program_instructions:
            process_instruction(instr, f)

def analyse_semantique(arbre):
    print("=== Analyse sémantique ===")
    SEM.SemNode(arbre)           # annote les indices, remplit NBvar
    print(f"[INFO] NBvar={SEM.NBvar}")
    return arbre
def optimisation(arbre):
    print("=== Optimisation (bidon) ===")
    return arbre

def gencode(arbre):
    print("=== Génération de code (postfixe) ===")
    instructions = []
    # Générer le code de toutes les fonctions
    for child in arbre.enfants:
        instructions += GenNode(child)
    # Ajouter l'appel à main au début, puis halt, puis les définitions fonctions
    main_call = ["prep main", "call 0", "halt"]
    # Réorganiser : appel main + halt, puis définitions fonctions
    final_instructions = main_call + instructions
    for instr in final_instructions:
        print(instr)
    write_msm(final_instructions, "out.msm")
    print("→ Programme MSM écrit dans out.msm")

def debug_lexer(filepath):
    print(f"--- Analyse lexicale de '{filepath}' ---")
    LEX.init_from_file(filepath)
    while LEX.T and LEX.T.type.name != "tok_eof":
        print(f"{LEX.T.type.name} -> '{LEX.T.chaine}'")
        LEX.T = LEX.next()
    print("tok_eof")

def pipeline(filepath):
    print(f"--- Compilation de '{filepath}' ---")
    analyseur = AnalyseurSyntaxique(filepath)
    arbre = analyseur.arbre
    if arbre is None:
        print("Erreur : aucun arbre syntaxique généré")
        return
    print("=== Arbre Syntaxique ===")
    arbre.afficher()
    arbre = analyse_semantique(arbre)
    arbre = optimisation(arbre)
    gencode(arbre)

if __name__ == "__main__":
    fichier = "test.c"
    if DEBUG_LEXER:
        debug_lexer(fichier)
    else:
        pipeline(fichier)