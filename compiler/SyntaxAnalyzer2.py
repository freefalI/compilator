
from .LexicalAnalyzerOld import *
#from .AscendingAnalysis import RelationTableMaker
#from . import grammar_poliz as grammar
#from itertools import chain 
#from .classes import Lexeme
from  .transition_table import transition_table

class SyntaxAnalyzer2:
    def __init__(self,t_lexemes,t_idns,t_constants,transition_table):
        self.lexemes = t_lexemes
        self.idns = t_idns
        self.constants = t_constants
        self.i = 0
        self.stack = []
        self.cur_state = 1
        self.analysis_table=[]
        self.ERROR = 'error'
        self.EXIT = 'exit'
        self.transition_table=transition_table

    def nextLexeme(self):
        lexeme = self.lexemes[self.i]
        self.i += 1
        return lexeme

    def line(self):
        return self.lexemes[self.i].line

    def run(self):
        while self.i < len(self.lexemes):
            lexeme = self.nextLexeme()
            # print(" state = {}, lexeme_code = {}, lexeme = {}, stack = {}".format(
            #             self.cur_state,lexeme.code,lexeme.name,self.stack[:]))
            
            self.analysis_table.append([self.cur_state,self.stack[:]])
            self.processState(self.cur_state, lexeme.code)
        return self.analysis_table

    def processState(self, state, lexeme_code):
        transitions = self.transition_table[state]
        if not isinstance(transitions, tuple):
            transitions = (transitions,)
        for transition in transitions:
            if transition.get("label") == None:
                self.exit()
                return
            labels = transition['label']
            if labels == "any":
                self.i -= 1
                self.stack.append(transition['stack'])
                self.cur_state = transition['state']
                return
            if not isinstance(labels, tuple):
                labels = (labels,)
            for label in labels:
                if label == lexeme_code:
                    if transition.get("zr") != None:
                        if transition['zr'] == self.EXIT:
                            self.i += 1
                            self.exit()
                            return
                    if transition.get("stack") != None:
                        self.stack.append(transition['stack'])
                        self.cur_state = transition['state']
                        return
                    self.cur_state = transition['state']
                    return
            if transition.get("nezr") != None:
                if transition['nezr'] == self.EXIT:
                    self.exit()
                elif transition['nezr'] == self.ERROR:
                    # raise SyntaxException("{} \n state = {}, lexeme_code = {}, lexeme = {}, stack = {}".format(
                    #    transition['error_msg'], self.cur_state, lexeme_code, self.lexemes[self.i].name, self.stack,))
                    raise SyntaxException(
                        transition['error_msg'], self.line()-1)



    def exit(self):
        # print("EXIT")
        self.i-=1
        try:
            state = self.stack.pop()
            self.cur_state=state
        except IndexError as ex:
            pass

if __name__ == "__main__":
    FILE_NAME  = 'source.txt'
    file = open(FILE_NAME,'r')
    input_text = file.read()
    file.close()
    lexer = LexicalAnalyzer(input_text)
    # (t_lexemes,t_idns,t_constants) = lexer.run()
    # text="".join(tablesToString(t_lexemes,t_idns,t_constants))
    # print(text)

    sAn = SyntaxAnalyzer2(*lexer.run(),transition_table.transition_table)
    # sAn.run()
    print(*sAn.run(),sep="\n")
