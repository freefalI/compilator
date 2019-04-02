import re
from .exceptions import *
from .classes import *
#TODO  чи може бути ідн і мітка з одним іменем

class LexicalAnalyzer:
    IDN_CODE = 100
    CON_CODE = 101
    LAB_CODE = 102
    def __init__(self,program):
        self.program = program
        self.lexemes_table = {
            'int': 1,
            'float': 2,
            'for': 3,
            'by':4,
            'do': 5,
            'if': 6,
            'cin': 7,
            'cout': 8,
            'while': 9,
            'then': 10,
            'goto': 11,
            'label': 12,
            '{': 13,
            '}': 14,
            '\n': 15,
            ',': 16,
            '=': 17,
            '<<': 18,
            '>>': 19,
            '<': 20,
            '>': 21,
            '<=': 22,
            '>=': 23,
            '==': 24,
            '!=': 25,
            '+': 26,
            "-":27,
            '*': 28,
            '/': 29,
            '(': 30,
            ')': 31,
            ":": 32,
            '?': 33
        }
        self.single_separators = {'{','}','\n',' ',',','=','>','<','+','-','*','/','(',')',':','?','!'}
        self.lexemes = []
        self.idns = []
        self.constants = []

        self.current_position = 0
        self.white_separators={' ','\t'}
        self.line_count = 1
        self.variable_type = None 
        self.wait_for_kft = True # 

        self.END_OF_PROGRAM_SYMBOL = '}'
        self.TYPE_INT = 'int'
        self.TYPE_FLOAT = 'float'
        self.TYPE_LABEL = 'label'
        self.IDN_CODE = 100
        self.CON_CODE = 101
        self.LAB_CODE = 102

    def removeComments(self):
        self.program = re.sub(r'//[^\n]*','',self.program)

    def run(self):
        # print(self.program)
        self.removeComments()
        # print(self.program)
        self.parse()
        # print("---Lexems",*self.lexemes,sep='\n')
        # print("---Idns",*self.idns,sep='\n')
        # print("---Cons",*self.constants,sep='\n')
        return (self.lexemes,self.idns,self.constants)

    def nextChar(self):
        char=None
        try:
            char = self.program[self.current_position]
        except IndexError as ex:
            pass
            #raise NoEndOfProgramSymbolException("Need {} in the end of program".format(
            #    self.END_OF_PROGRAM_SYMBOL), self.line_count)
        self.current_position += 1
        if char:
            print("nextchar return ",char)
            return char
            #new_lexeme_id = len(self.lexemes)+1
            #return  "\n"#Lexeme(new_lexeme_id,self.line_count,"¶",15)
        print("nextchar return None")
        return None
    
    def isTerminal(self,char):
        return char in self.lexemes_table
    def isWhiteSeparator(self,char):
        return char in self.white_separators
    def isSingleSeparator(self,char):
        return  char  in self.single_separators
    
    def addLexeme(self,lexeme,code=None,fid=None):
        new_lexeme_id = len(self.lexemes)+1
        if not code:
            code = self.getLexemCode(lexeme)
        self.lexemes.append(Lexeme(new_lexeme_id,self.line_count,lexeme,code,fid))
    
    def getLexemCode(self,lexeme):
        try:
            return self.lexemes_table[lexeme]
        except KeyError as ex:
            raise  NotFoundLexemException("Не знайдена лексема " +lexeme,self.line_count)

    def idnExists(self,lexeme):
        return lexeme in [idn.name for idn in self.idns]
    def addIdn(self,idn_name):
        self.idns.append(Idn(len(self.idns)+1,idn_name,self.TYPE_INT,self.line_count))
        # if self.variable_type == self.TYPE_LABEL:
        #     self.idns.append(Idn(len(self.idns)+1,idn_name,self.variable_type,self.line_count))
        # else:
        #     self.idns.append(Idn(len(self.idns)+1,idn_name,self.variable_type))
        return self.idns[-1]
    def getIdnByName(self,idn_name):
        for idn in self.idns:
            if idn.name==idn_name:
                return idn
        raise NotFoundIdnException("Не знайдений ідентифікатор "+idn_name,self.line_count)

    def constantExists(self,lexeme):
       return lexeme in [constant.name for constant in self.constants]
    def addConstant(self,constant,constant_type):
        self.constants.append(Constant(len(self.constants)+1,constant ,constant_type))
        return self.constants[-1]
    def getConstantByName(self,constant):
        for con in self.constants:
            if con.name==constant:
                return con
        raise NotFoundConException("Не знайдена константа "+constant,self.line_count)

    def parse(self):
        char  = self.nextChar() 
        while (char != self.END_OF_PROGRAM_SYMBOL):
            while self.isWhiteSeparator(char):# пропускаєм білі роздільники
                char = self.nextChar()
            lexeme = ''
            if char =='\n':
                self.line_count +=1
            #if char==None:
            #    self.char=''
            print("lexeme=",lexeme,'|')
            while not self.isSingleSeparator(char):
                # накопичуэмо лексему поки  наст символ не роздільник
                lexeme += char
                char = self.nextChar()
                #if char==None:
                #    char=''
            print("lexeme=",lexeme,'|')
            if lexeme=='':
                lexeme = char
                char =  self.nextChar()
                if char==None:
                    char=''
                    return
            print("lexeme=",lexeme,'|')
            if char==None:
                 char=''
                 break
            print("lexeme=",lexeme,'|')    
            if  self.wait_for_kft and lexeme == '-'  : # мінус бінарний чи кфт
                while not self.isSingleSeparator(char):
                    lexeme += char
                    char = self.nextChar()
                self.wait_for_kft = True
            else:
                self.wait_for_kft = True
            if char==None:
                 char=''
                 break
            print("0000lexeme=",lexeme,'|')    
            char = self.processLexeme(lexeme,char)
            

        self.addLexeme(char,self.getLexemCode(char))        

    def processLexeme(self,lexeme,char):
        if lexeme == '!':
            if char == '=':
                lexeme += char
                self.addLexeme(lexeme,self.getLexemCode(lexeme))        
            else:
                raise LexicException(
                    "Недопустимое выражение " + lexeme, self.line_count)
            char = self.nextChar()
        elif lexeme in ('<','>','='):
            if self.isTerminal(lexeme + char):
                lexeme += char
                char = self.nextChar()
            self.addLexeme(lexeme,self.getLexemCode(lexeme))   
        elif self.isTerminal(lexeme):
            if lexeme==')':
                self.wait_for_kft = False
            self.processTerminal(lexeme)  
        elif re.match(r'^[a-zA-Z][a-zA-Z\d]*$',lexeme) :
            self.processIdn(lexeme)
            self.wait_for_kft = False
        elif re.match(r'^[+-]?(\d+\.\d*|\.?\d+)$',lexeme):
            self.processConstant(lexeme)
            self.wait_for_kft = False
        else:
            raise LexicException("Недопустимое выражение " + lexeme,self.line_count)
        return char     
        
    def processIdn(self, lexeme):
        idn_code = self.IDN_CODE
        if self.idnExists(lexeme):
            if self.variable_type:
                raise VariableRedeclarationException("Перевизначення змінної " + lexeme,self.line_count)
            idn = self.getIdnByName(lexeme)
        else:
            if not self.variable_type:
               pass
               # raise UndefinedVariableException("Використання необ'явленої змінної "+ lexeme,self.line_count)
            idn = self.addIdn(lexeme)
        if idn.type=="label":
            idn_code = self.LAB_CODE
        self.addLexeme(idn.name,idn_code, str(idn.id))
    def processConstant(self, lexeme):
        lexeme  = lexeme.lstrip('+')
        constant_type = self.TYPE_FLOAT if ('.' in lexeme) else self.TYPE_INT
        if constant_type==self.TYPE_FLOAT:
            lexeme= lexeme.rstrip('0')
        if self.constantExists(lexeme):
            con = self.getConstantByName(lexeme)
        else:
            con = self.addConstant(lexeme,constant_type)

        self.addLexeme(con.name,self.CON_CODE, str(con.id))        
    def processTerminal(self, lexeme):
        if lexeme =='\n':
            self.variable_type=None
        elif lexeme in {self.TYPE_INT,self.TYPE_FLOAT,self.TYPE_LABEL}:
            self.variable_type=lexeme
        self.addLexeme(lexeme,self.getLexemCode(lexeme))        

if __name__ == "__main__":
    FILE_NAME  = 'source.txt'
    file = open(FILE_NAME,'r')
    input_text = file.read()
    file.close()
    # print(input_text)
    lexer = LexicalAnalyzer(input_text)
    (t_lexemes,t_idns,t_constants) = lexer.run()
    # text="".join(tablesToString(t_lexemes,t_idns,t_constants))
    print(*t_lexemes,*t_idns,*t_constants,sep="\n")