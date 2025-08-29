from AnalyseurSyntaxique import AnalyseurSyntaxique, Node

def analyse_semantique(arbre_syntaxique):
    print("=== Analyse sémantique (bidon) ===")
    return arbre_syntaxique

def optimisation(arbre_decore):
    print("=== Optimisation (bidon) ===")
    return arbre_decore

def gencode(arbre_optimise):
    print("=== Génération de code (bidon) ===")
    arbre_optimise.afficher()

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
    pipeline("test.c")
