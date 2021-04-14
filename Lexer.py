from sly import Lexer

class TZFELexer(Lexer):

    #1 Set of token names.   This is always required
    tokens = { VARNAME, NUMBER, ADD, SUBTRACT, MULTIPLY,
               DIVIDE, UP, DOWN, LEFT, RIGHT, ASSIGN, 
               TO, VAR, IS, VALUE_IN, COMMA, PERIOD }

    # String containing ignored characters between tokens
    ignore = ' \t'
    ignore_comment_py = r'\#.*'
    ignore_comment_c = r'//.*'

    # Regular expression rules for tokens
    ADD     = r'ADD'
    SUBTRACT   = r'SUBTRACT'
    MULTIPLY   = r'MULTIPLY'
    DIVIDE  = r'DIVIDE'
    UP  = r'UP'
    DOWN  = r'DOWN'
    LEFT  = r'LEFT'
    RIGHT = r'RIGHT'
    ASSIGN = r'ASSIGN'
    TO = r'TO'
    VAR=r'VAR'
    IS=r'IS'
    VALUE_IN = r'VALUE IN'
    COMMA = r','
    PERIOD = r'\.'
    VARNAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER  = r'\d+'

    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print(f"2048> Sorry, I don't understand that.")
        self.index+=1
        # return t # optional, only if error token required while parsing

if __name__ == '__main__':
    lexer = TZFELexer()
    line = input()
    while(line!=""):
        print(list(lexer.tokenize(line)))
        line=input()
