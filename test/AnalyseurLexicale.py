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
    tok_et = 24
    tok_ou = 25
    tok_addr = 26
    tok_int = 27
    tok_void = 28
    tok_return = 29
    tok_do = 30
    tok_if = 31
    tok_else = 32
    tok_while = 33
    tok_for = 34
    tok_default = 35
    tok_break = 36
    tok_continue = 37
    tok_debug = 38
    tok_send = 39
    tok_recv = 40
    tok_error = 41

class Token:
    def __init__(self, type, valeur, chaine):
        self.type = type
        self.valeur = valeur
        self.chaine = chaine

def erreur(message):
    print(f"[LEXER ERREUR] {message}")

def advance():
    global position, current_char
    position += 1
    if position >= len(source_code):
        current_char = None
    else:
        current_char = source_code[position]

def init_from_file(filepath):
    global source_code, position, current_char, T, LAST
    with open(filepath, "r") as f:
        source_code = f.read()
    print(f"[DEBUG] Contenu de {filepath} : {repr(source_code)}")
    position = 0
    current_char = source_code[0] if source_code else None
    LAST = None
    T = None  # <<< On NE CONSOMME PAS encore le premier token ici !

def next():
    global LAST, T, current_char
    LAST = T

    while current_char and current_char.isspace():
        advance()

    if current_char is None:
        return Token(TokenType.tok_eof, None, "")

    # Nombres
    if current_char.isnumeric():
        nombre_str = ""
        while current_char and current_char.isnumeric():
            nombre_str += current_char
            advance()
        return Token(TokenType.tok_const, int(nombre_str), nombre_str)

    # Identifiants / mots-clés
    if current_char.isalpha() or current_char == '_':
        mot_str = ""
        while current_char and (current_char.isalnum() or current_char == '_'):
            mot_str += current_char
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
            "recv": TokenType.tok_recv
        }
        return Token(mots_cles.get(mot_str, TokenType.tok_ident), 0, mot_str)

    # Symboles simples
    single_tokens = {
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
        '&': TokenType.tok_addr
    }

    if current_char in single_tokens:
        token = Token(single_tokens[current_char], 0, current_char)
        advance()
        return token

    # Caractère inconnu
    char = current_char
    advance()
    erreur(f"Caractère inconnu: '{char}'")
    return Token(TokenType.tok_error, 0, char)
