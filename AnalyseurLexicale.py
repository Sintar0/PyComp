from enum import Enum

current_char = None
T = None
LAST = None
source_code = ""
position = 0

class TokenType(Enum):
    tok_eof = 1
    tok_const = 2
    tok_ident = 3
    tok_parenthese_ouvrante = 4
    tok_parenthese_fermeante = 5
    tok_accolade_ouvrante = 6
    tok_accolade_fermeante = 7
    tok_croche_ouvrante = 8
    tok_croche_fermeante = 9

    tok_egal = 10
    tok_plus = 11
    tok_moins = 12
    tok_etoile = 13
    tok_slash = 14
    tok_modulo = 15

    tok_virgule = 16
    tok_point_virgule = 17
    tok_supérieur = 18
    tok_inférieur = 19
    tok_supérieur_egal = 20
    tok_inférieur_egal = 21
    tok_egal_egal = 22
    tok_différent = 23

    tok_et = 24         # '&&'
    tok_ou = 25         # '||'
    tok_addr = 26       # '&' seul
    tok_not = 27        # '!' seul

    tok_int = 28
    tok_void = 29
    tok_return = 30
    tok_do = 31
    tok_if = 32
    tok_else = 33
    tok_while = 34
    tok_for = 35
    tok_default = 36
    tok_break = 37
    tok_continue = 38

    tok_debug = 39
    tok_send = 40
    tok_recv = 41
    tok_error = 42

class Token:
    def __init__(self, type, valeur, chaine):
        self.type = type
        self.valeur = valeur
        self.chaine = chaine

def erreur(message: str):
    print(f"Erreur: {message}")


def check(type: TokenType):
    """Vérifie le type du token courant sans le consommer."""
    return T is not None and T.type == type

def match(type: TokenType):
    """Consomme le token courant s'il correspond au type attendu."""
    global T
    if check(type):
        T = next()
        return True
    return False

def accept(type: TokenType):
    """Vérifie puis consomme; lève une erreur claire en cas d'inadéquation."""
    if not check(type):
        found = T.type.name if T else 'None'
        raise Exception(f"Syntax Error: Expected {type.name} but got {found}")
    return match(type)


def init_from_file(filepath: str):
    """Charge la source et initialise T en appelant immédiatement next()."""
    global source_code, position, current_char, T, LAST
    with open(filepath, "r") as f:
        source_code = f.read()
    position = 0
    current_char = source_code[0] if source_code else None
    LAST = None
    T = next()  # NOTE: on consomme le PREMIER token 


def advance():
    global position, current_char
    position += 1
    current_char = source_code[position] if position < len(source_code) else None


def next():
    """Retourne le prochain token à partir de la position courante.
    N'ASSIGNE PAS T; c'est le rôle de match/accept/init."""
    global LAST, T, current_char
    LAST = T

    # Sauter les espaces
    while current_char and current_char.isspace():
        advance()

    if current_char is None:
        return Token(TokenType.tok_eof, None, "")

    # TODO commentaires (// ... ou /* ... */) à traiter plus tard

    # Constantes entières
    if current_char.isnumeric():
        s = ""
        while current_char and current_char.isnumeric():
            s += current_char
            advance()
        return Token(TokenType.tok_const, int(s), s)

    # Identifiants / mots-clés
    if current_char.isalpha() or current_char == '_':
        s = ""
        while current_char and (current_char.isalnum() or current_char == '_'):
            s += current_char
            advance()
        mots_cles = {
            "int": TokenType.tok_int,
            "void": TokenType.tok_void,
            "return": TokenType.tok_return,
            "do": TokenType.tok_do,
            "if": TokenType.tok_if,
            "else": TokenType.tok_else,
            "while": TokenType.tok_while,
            "for": TokenType.tok_for,
            "default": TokenType.tok_default,
            "break": TokenType.tok_break,
            "continue": TokenType.tok_continue,
            "debug": TokenType.tok_debug,
            "send": TokenType.tok_send,
            "recv": TokenType.tok_recv,
        }
        return Token(mots_cles.get(s, TokenType.tok_ident), 0, s)

    # Opérateurs 2 caractères
    two = (current_char or '') + (source_code[position+1] if position+1 < len(source_code) else '')
    if two == '==':
        advance(); advance(); return Token(TokenType.tok_egal_egal, 0, '==')
    if two == '!=':
        advance(); advance(); return Token(TokenType.tok_différent, 0, '!=')
    if two == '>=':
        advance(); advance(); return Token(TokenType.tok_supérieur_egal, 0, '>=')
    if two == '<=':
        advance(); advance(); return Token(TokenType.tok_inférieur_egal, 0, '<=')
    if two == '&&':
        advance(); advance(); return Token(TokenType.tok_et, 0, '&&')
    if two == '||':
        advance(); advance(); return Token(TokenType.tok_ou, 0, '||')

    # Symboles simples
    table = {
        '(': TokenType.tok_parenthese_ouvrante,
        ')': TokenType.tok_parenthese_fermeante,
        '{': TokenType.tok_accolade_ouvrante,
        '}': TokenType.tok_accolade_fermeante,
        '[': TokenType.tok_croche_ouvrante,
        ']': TokenType.tok_croche_fermeante,
        '=': TokenType.tok_egal,
        '+': TokenType.tok_plus,
        '-': TokenType.tok_moins,
        '*': TokenType.tok_etoile,
        '/': TokenType.tok_slash,
        '%': TokenType.tok_modulo,
        ',': TokenType.tok_virgule,
        ';': TokenType.tok_point_virgule,
        '>': TokenType.tok_supérieur,
        '<': TokenType.tok_inférieur,
        '&': TokenType.tok_addr,
        '!': TokenType.tok_not,
    }
    if current_char in table:
        ch = current_char
        tt = table[ch]
        advance()
        return Token(tt, 0, ch)

    # Caractère inconnu
    ch = current_char
    advance()
    erreur(f"Caractère inconnu: '{ch}'")
    return Token(TokenType.tok_error, 0, ch)