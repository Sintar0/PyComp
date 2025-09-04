# -*- coding: utf-8 -*-
from AnalyseurSyntaxique import AnalyseurSyntaxique
import AnalyseurLexicale as LEX
from ops import GenNode

DEBUG_LEXER = False
#Mapping des instructions
MSM_MAP = {
    "gt": "cmpgt",
    "lt": "cmplt",
    "ge": "cmpge",
    "le": "cmple",
    "eq": "cmpeq",
    "ne": "cmpne",
    # les autres sont identiques: add, sub, mul, div, mod, and, or
}

def write_msm(program_instructions: list, out_path: str, show_result: bool = True):
    """
    program_instructions : sortie de GenNode (ex: ["push 1", "push 2", "mul", "push 3", "add"])
    Écrit un assembleur MSM exécutable avec .start, instructions mappées, dbg/halt.
    """
    def process_instruction(instr, file):
        if isinstance(instr, list):
            # Si c'est une liste imbriquée, traiter chaque élément récursivement
            for item in instr:
                process_instruction(item, file)
        else:
            # C'est une chaîne de caractères
            parts = instr.split()
            op = parts[0]
            arg = parts[1] if len(parts) > 1 else None
            op_msm = MSM_MAP.get(op, op)  # remap si nécessaire
            if arg is None:
                file.write(f"{op_msm}\n")
            else:
                file.write(f"{op_msm} {arg}\n")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(".start\n")
        for instr in program_instructions:
            process_instruction(instr, f)
        if show_result:
            f.write("dbg\n")   # affiche le top en décimal
        f.write("halt\n")


def analyse_semantique(arbre):
    print("=== Analyse sémantique (bidon) ===")
    return arbre

def optimisation(arbre):
    print("=== Optimisation (bidon) ===")
    return arbre

def gencode(arbre):
    print("=== Génération de code (postfixe) ===")
    instructions = GenNode(arbre)
    for instr in instructions:
        print(instr)
    write_msm(instructions, "out.msm", show_result=True)
    print("→ Programme MSM écrit dans out.msm")

def debug_lexer(filepath):
    print(f"--- Analyse lexicale de '{filepath}' ---")
    LEX.init_from_file(filepath)
    print(f"Premier token: {LEX.T.type.name}, Chaine: '{LEX.T.chaine}'")
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
