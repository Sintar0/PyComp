import sys
sys.stdout.reconfigure(encoding='utf-8') # on a souvent eu des soucis avec l'encodage du coup, on le force l'utf-8
from AnalyseurSyntaxique import AnalyseurSyntaxique 
import AnalyseurLexicale as LEX
from ops import GenNode
import AnalyseurSemantique as SEM 

DEBUG_LEXER = False

def write_msm(program_instructions: list, out_path: str):

    def process_instruction(instr, file):
        if isinstance(instr, list):
            # Si on lui donne une liste (potentiellement imbriquée),
            # elle appelle récursivement la fonction sur chaque élément.
            for item in instr:
                process_instruction(item, file)
        else:
            # Sinon, c'est une instruction sous forme de chaîne.
            # Elle l'écrit directement dans le fichier (ops.py génère déjà les instructions MSM)
            file.write(f"{instr}\n")


    with open(out_path, "w", encoding="utf-8") as f:
        f.write(".start\n")
        for instr in program_instructions:
            process_instruction(instr, f)

def analyse_semantique(arbre):
    print("=== Analyse sémantique ===")
    SEM.SemNode(arbre)           # annote les indices, remplit NBvar
    print(f"[INFO] NBvar={SEM.NBvar}")
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
    gencode(arbre)

if __name__ == "__main__":
    fichier = "test.c"
    if DEBUG_LEXER:
        debug_lexer(fichier)
    else:
        pipeline(fichier)