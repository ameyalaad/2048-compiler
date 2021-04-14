from Storage import eprint
from sly import Parser
from Lexer import TZFELexer
import Game

class TZFEParser(Parser):   
    tokens = TZFELexer.tokens

    def __init__(self, storage) -> None:
        super().__init__()
        self.storage = storage

    @_('move', 'getval', 'assign', 'naming', 'noperiod', 'keyworderror') #, 'empty')
    def all(self, p):
        pass

    # @_('')
    # def empty(self, p):
    #     exit(0)

    @_('ADD UP PERIOD', 'ADD DOWN PERIOD', 'ADD LEFT PERIOD', 'ADD RIGHT PERIOD', 'SUBTRACT UP PERIOD', 'SUBTRACT DOWN PERIOD', 'SUBTRACT LEFT PERIOD', 'SUBTRACT RIGHT PERIOD', 'MULTIPLY UP PERIOD', 'MULTIPLY DOWN PERIOD', 'MULTIPLY LEFT PERIOD', 'MULTIPLY RIGHT PERIOD', 'DIVIDE UP PERIOD', 'DIVIDE DOWN PERIOD', 'DIVIDE LEFT PERIOD', 'DIVIDE RIGHT PERIOD')
    def move(self, p):
        self.storage.move(p[1], p[0])
        print(f"2048> Thanks, {p[1].lower()} move done, random tile added.")
        self.storage.generate_update()
        self.storage.show_current_state()
        self.storage.logstate()
        # print(self.storage._vars)

    @_('VALUE_IN location PERIOD')
    def getval(self, p):
        if p[1][1]>4 or p[1][3]>4 or p[1][1]==0 or p[1][3]==0:
            print("2048> There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")      
            eprint("-1")      
        else:
            print(f"2048> Thanks, value in ({p[1][1]}, {p[1][3]}) is {self.storage.get_value(p[1][1]-1, p[1][3]-1)}")
            eprint("-1")
            return self.storage.get_value(p[1][1]-1, p[1][3]-1)

    @_('ASSIGN value TO location PERIOD')
    def assign(self, p):
        if p[1]:
            if p[3][1]>4 or p[3][3]>4 or p[3][1]==0 or p[3][3]==0:
                print("2048> There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")    
                eprint("-1")        
            else:
                self.storage.set_value(p[3][1]-1, p[3][3]-1, p[1][1])
                print(f"2048> Thanks, assignment done.")
                self.storage.show_current_state()
                self.storage.logstate()

    @_('VAR VARNAME IS location PERIOD')
    def naming(self, p):
        if p[3][1]>4 or p[3][3]>4 or p[3][1]==0 or p[3][3]==0:
            print("2048> There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")
            eprint("-1")
        else:
            print("2048> Thanks, naming done.")
            self.storage.newvar(p[1], p[3][1]-1, p[3][3]-1)
            self.storage.logstate()

    @_('NUMBER COMMA NUMBER', 'VARNAME')
    def location(self, p):
        if len(p)==3:
            return p
        else:
            p=self.storage.lookup(p[0])
            if p:
                return p
            else:
                print("2048> There is no variable like that. ")

    @_('NUMBER', 'VALUE_IN location')
    def value(self, p):
        if len(p)==1:
            return p
        if p[1][1]>4 or p[1][3]>4 or p[1][1]==0 or p[1][3]==0:
            print("2048> There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4.")      
            eprint("-1")
            return None
        else:
            print(f"2048> Thanks, value in ({p[1][1]}, {p[1][3]}) is {self.storage.get_value(p[1][1]-1, p[1][3]-1)}")
            eprint("-1")
            return ('value', self.storage.get_value(p[1][1]-1, p[1][3]-1))

    @_('VAR keyword IS location', 'VAR VARNAME IS location', 'ASSIGN value TO location', 'VALUE_IN location', 'ADD UP', 'ADD DOWN', 'ADD LEFT', 'ADD RIGHT', 'SUBTRACT UP', 'SUBTRACT DOWN', 'SUBTRACT LEFT', 'SUBTRACT RIGHT', 'MULTIPLY UP', 'MULTIPLY DOWN', 'MULTIPLY LEFT', 'MULTIPLY RIGHT', 'DIVIDE UP', 'DIVIDE DOWN', 'DIVIDE LEFT', 'DIVIDE RIGHT')
    def noperiod(self, p):
        print("2048> You need to end a command with a full-stop.")
        eprint("-1")
        return

    @_('VAR keyword IS location PERIOD')
    def keyworderror(self, p):
        print("2048> No, a keyword cannot be a variable name.")
        eprint("-1")

    @_( 'NUMBER', 'ADD', 'SUBTRACT', 'MULTIPLY','DIVIDE', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'ASSIGN', 'TO', 'VAR', 'IS', 'VALUE_IN', 'COMMA', 'PERIOD')
    def keyword(self, p):
        pass
    
    def error(self, p):
        print("2048> Syntax Error")
        eprint("-1")