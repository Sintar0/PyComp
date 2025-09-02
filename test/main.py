from AnalyseurSyntaxique import AnalyseurSyntaxique, Node
from AnalyseurLexicale import init_from_file, next, T

DEBUG_LEXER = True  # ← Active/désactive le mode debug de l’analyse lexicale

def analyse_semantique(arbre_syntaxique):
    print("=== Analyse sémantique (bidon) ===")
    return arbre_syntaxique

def optimisation(arbre_decore):
    print("=== Optimisation (bidon) ===")
    return arbre_decore

def gencode(arbre_optimise):
    print("=== Génération de code (bidon) ===")
    arbre_optimise.afficher()

def debug_lexer(filepath):
    print(f"--- Analyse lexicale de '{filepath}' ---")
    init_from_file(filepath)
    token = next()
    while token is not None and token.type.name != "tok_eof":
        print(f"{token.type.name}, valeur={token.valeur}, chaine='{token.chaine}'")
        token = next()
    print("tok_eof")

def pipeline(filepath):
    print(f"--- Compilation de '{filepath}' ---")
    analyseur = AnalyseurSyntaxique(filepath)
    arbre_syntaxique = analyseur.arbre

    if arbre_syntaxique is None:
        print("Erreur : aucun arbre syntaxique généré")
        return

    arbre_decore = analyse_semantique(arbre_syntaxique)
    arbre_optimise = optimisation(arbre_decore)
    gencode(arbre_optimise)

if __name__ == "__main__":
    fichier = "test.c"
    if DEBUG_LEXER:
        debug_lexer(fichier)
    else:
        pipeline(fichier)
