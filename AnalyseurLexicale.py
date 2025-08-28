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
    tok_supérieur_egal = 19
    tok_inférieur_egal = 20
    tok_egal_egal = 21
    tok_différent = 22
    
    tok_et = 23
    tok_ou = 24
    tok_addr = 25
    
    tok_int = 26
    tok_void = 27
    tok_return = 28
    tok_do = 29
    tok_if = 30
    tok_else = 31
    tok_while = 32
    tok_for = 33
    tok_default = 34
    tok_break = 35
    tok_continue = 36
    
    tok_debug = 37
    tok_send = 38
    tok_recv = 39
    tok_error = 40

class Token:
    def __init__(self, type, valeur, chaine):
        self.type = type
        self.valeur = valeur
        self.chaine = chaine

def erreur(message):
    print(f"Erreur: {message}")

def accept(type: TokenType):
    if check(type):
        return True
    else:
        erreur("Unexpected token")
        return False

def check(type: TokenType):
    global T
    if T.type == type:
        T = next()
        return True
    else:
        return False

def init_from_file(filepath):
    global source_code, position, current_char, T
    with open(filepath, "r") as f:
        source_code = f.read()
    position = 0
    current_char = source_code[0] if source_code else None
    T = next() 

def advance():
    global position, current_char
    position += 1
    if position >= len(source_code):
        current_char = None
    else:
        current_char = source_code[position]

def next():
    global LAST, T, current_char
    
    LAST = T  
    while current_char and current_char.isspace():
        advance()
    
    if current_char is None:
        return Token(TokenType.tok_eof, None, "")
    
    # todo: gérer les commentaires plus tard
    
    
    if current_char.isnumeric():
        nombre_str = ""
        while current_char and current_char.isnumeric():
            nombre_str += current_char
            advance()
        return Token(TokenType.tok_const, int(nombre_str), nombre_str)
    
    elif current_char.isalpha() or current_char == '_':
        mot_str = ""
        while current_char and (current_char.isalnum() or current_char == '_'):
            mot_str += current_char
            advance()
        
        if mot_str == "int":
            return Token(TokenType.tok_int, 0, mot_str)
        elif mot_str == "void":
            return Token(TokenType.tok_void, 0, mot_str)
        elif mot_str == "return":
            return Token(TokenType.tok_return, 0, mot_str)
        elif mot_str == "do":
            return Token(TokenType.tok_do, 0, mot_str)
        elif mot_str == "if":
            return Token(TokenType.tok_if, 0, mot_str)
        elif mot_str == "else":
            return Token(TokenType.tok_else, 0, mot_str)
        elif mot_str == "while":
            return Token(TokenType.tok_while, 0, mot_str)
        elif mot_str == "for":
            return Token(TokenType.tok_for, 0, mot_str)
        elif mot_str == "default":
            return Token(TokenType.tok_default, 0, mot_str)
        elif mot_str == "break":
            return Token(TokenType.tok_break, 0, mot_str)
        elif mot_str == "continue":
            return Token(TokenType.tok_continue, 0, mot_str)
        elif mot_str == "debug":
            return Token(TokenType.tok_debug, 0, mot_str)
        elif mot_str == "send":
            return Token(TokenType.tok_send, 0, mot_str)
        elif mot_str == "recv":
            return Token(TokenType.tok_recv, 0, mot_str)
        else:
            # Si l'identifiant n'est pas autorisé, on le marque comme un identifiant non autorisé
            return Token(TokenType.tok_ident, 0, mot_str)
    
    elif current_char == '(':
        char = current_char
        advance()
        return Token(TokenType.tok_parenthese_ouvrante, 0, char)
    elif current_char == ')':
        char = current_char
        advance()
        return Token(TokenType.tok_parenthese_fermeante, 0, char)
    elif current_char == '{':
        char = current_char
        advance()
        return Token(TokenType.tok_accolade_ouvrante, 0, char)
    elif current_char == '}':
        char = current_char
        advance()
        return Token(TokenType.tok_accolade_fermeante, 0, char)
    elif current_char == '[':
        char = current_char
        advance()
        return Token(TokenType.tok_croche_ouvrante, 0, char)
    elif current_char == ']':
        char = current_char
        advance()
        return Token(TokenType.tok_croche_fermeante, 0, char)
    elif current_char == '=':
        char = current_char
        advance()
        return Token(TokenType.tok_egal, 0, char)
    elif current_char == '+':
        char = current_char
        advance()
        return Token(TokenType.tok_plus, 0, char)
    elif current_char == '-':
        char = current_char
        advance()
        return Token(TokenType.tok_moins, 0, char)
    elif current_char == '*':
        char = current_char
        advance()
        return Token(TokenType.tok_etoile, 0, char)
    elif current_char == '/':
        char = current_char
        advance()
        return Token(TokenType.tok_slash, 0, char)
    elif current_char == '%':
        char = current_char
        advance()
        return Token(TokenType.tok_modulo, 0, char)
    elif current_char == ',':
        char = current_char
        advance()
        return Token(TokenType.tok_virgule, 0, char)
    elif current_char == ';':
        char = current_char
        advance()
        return Token(TokenType.tok_point_virgule, 0, char)
    elif current_char == '>':
        char = current_char
        advance()
        return Token(TokenType.tok_supérieur, 0, char)
    elif current_char == '<':
        char = current_char
        advance()
        return Token(TokenType.tok_inférieur, 0, char)
    elif current_char == '&':
        char = current_char
        advance()
        return Token(TokenType.tok_addr, 0, char)
    else:
        erreur(f"Identifiant non autorisé: '{mot_str}'")
        return Token(TokenType.tok_error, 0, mot_str)

if __name__ == "__main__":
    
    init_from_file("test.c")
    
    print("=== Analyse lexicale ===")
    print(f"Premier token: {T.type.name}, Chaine: '{T.chaine}'")
    
    # Utilisation de check et accept
    if check(TokenType.tok_int):
        print("✓ Token 'int' accepté")
    
    # Continuer l'analyse
    while T.type != TokenType.tok_eof:
        print(f"Token courant: {T.type.name}, Chaine: '{T.chaine}'")
        T = next()  # Passer au token suivant
    
    print("Fin de l'analyse")
