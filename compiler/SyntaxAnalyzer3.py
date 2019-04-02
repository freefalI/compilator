from .LexicalAnalyzer import *
from .AscendingAnalysis import RelationTableMaker
from . import grammar_poliz as grammar
from itertools import chain 
from .classes import Lexeme


class SyntaxAnalyzer3:
    def __init__(self,t_lexemes,t_idns,t_constants,tableMaker):
        self.lexemes = t_lexemes[:]
        self.idns = t_idns
        self.constants = t_constants
        self.i = 0
        self.input_row = []
        self.stack = []
        self.TableMaker=tableMaker
        self.relation_table = tableMaker.getRelationTable()
        self.parse_results_table=[]
    # def nextLexeme(self):
    #     lexeme = self.lexemes[self.i]
        # self.i += 1
    #     return lexeme

    def line(self):
        print(self.i)
        return self.input_row[self.i].line

    def run(self):
        self.lexemes.append(None)
        self.stack.append(None)
        self.input_row=self.lexemes[:]
        it=0
        while True:
            print("NEW ITERATION",it,"\n   stack")
            self.parse_results_table.append({})
            print(*self.stack,sep="\n")
            it+=1
            current_lexeme = self.input_row[0]
            print("  cur lexeme\t",current_lexeme)
            relation = self.TableMaker.relationBetween(self.stack[-1],
                                                    self.input_row[0])
            print(relation)
            if relation==0:
                print(self.stack[-1], self.input_row[0])
                raise SyntaxException("Invalid syntax", self.line()-1)
            self.parse_results_table[-1].update({'relation':relation})
            self.parse_results_table[-1].update({'stack':self.stack[:]})
            self.parse_results_table[-1].update({'input_row':[i for i in self.input_row]})

            if relation in[1,2]:
                print("action1")
                self.stack.append(self.input_row.pop(0))
                self.i += 1
            else:
                print("action2")

                # print(self.stack)
                base=[]

                el2=self.stack[-1]
                for i in range(len(self.stack)-2,-1,-1):
                    el1=self.stack[i]
                    try:
                        if el1.name:
                            print(el1.name)
                    except AttributeError:
                        print( el1)
                    relation = self.TableMaker.relationBetween(el1,el2)
                    relation_map=['','=','<','>']
                    print("    ", relation_map[relation])
                    if relation!=2:
                        base.insert(0,el2)
                    else:
                        base.insert(0,el2)
                        break
                    el2=el1
                    # self.i -= 1
                print(self.stack[0])

                print("BASE=",base)
                base2=[]

                IDN_CODE = 100
                CON_CODE = 101
                LAB_CODE = 102
                for lexeme in base:
                    if isinstance(lexeme, Lexeme):
                        if lexeme.code==IDN_CODE:
                            i = base2.append("idn")
                        elif lexeme.code==CON_CODE:
                            i = base2.append("constant")
                        elif lexeme.code==LAB_CODE:
                            i = base2.append("lab")
                        elif lexeme.code==15:
                            i = base2.append("¶")
                        else:
                            i = base2.append(lexeme.name)

                    # except AttributeError:
                    else:
                        i = base2.append(lexeme)

                

                base2 = tuple(base2)
                print("BASE2=",base2)
                self.parse_results_table[-1].update({'base':base2})

                #find left part of rule in grammar
                answer=None
                find=False
                for nonterminal in self.TableMaker.grammar.keys():
                    right_part_of_rule = self.TableMaker.grammar[nonterminal]
                    if self.TableMaker.ruleHasAlternatives(right_part_of_rule):
                        for i in right_part_of_rule:
                            if i==base2:
                                answer = nonterminal
                                find=True
                                break
                    else:
                        if right_part_of_rule==base2:
                            answer = nonterminal
                            find=True
                    if find:
                        break
                print("ANSWER=",answer)
                if base2==('<expr1>',):
                    print("successful compilation")
                    return self.parse_results_table

                if answer==None:
                    raise SyntaxException("Invalid syntax", self.line()-1)
                count=len(base2)
                for i in range(count):
                    self.stack.pop()
                    self.i -= 1

                self.stack.append(answer)
                self.i += 1
            print("\n\n")
      


    def exit(self):
        print("EXIT")
        # self.i-=1
        # try:
        #     state = self.stack.pop()
        #     self.cur_state=state
        # except IndexError as ex:
        #     pass

if __name__ == "__main__":
    FILE_NAME  = 'source.txt'
    file = open(FILE_NAME,'r')
    input_text = file.read()
    file.close()
    lexer = LexicalAnalyzer(input_text)
    # (t_lexemes,t_idns,t_constants) = lexer.run()
    # text="".join(tablesToString(t_lexemes,t_idns,t_constants))
    # print(text)
    tableMaker = RelationTableMaker(grammar.grammar)
    # relation_table = tableMaker.getRelationTable()
    sAn = SyntaxAnalyzer3(*lexer.run(),tableMaker)
    # sAn.run()
    relation_map=['','=','<','>']
    parse_table = sAn.run()
    print(parse_table)
    for i in parse_table:
        print("\n",'='*30,end="")
        print("\nstack      ",end="")
        if not len(i['stack']):
            print("!!!empty!!!",end="")
        else:
            for st_el in i['stack']:
                if isinstance(st_el, Lexeme):
                    if st_el.code==15:
                        print("¶",end=", ")
                    else:
                        print(st_el.name,end=", ")
                else:
                    print(st_el,end=", ")
        
        print("\ninput_row      ",end="")
        if not len(i['input_row']):
            print("!!!empty!!!",end="")
        else:
            for row_el in i['input_row']:
                if isinstance(row_el, Lexeme):
                    if row_el.code==15:
                        print("¶",end=", ")
                    else:
                        print(row_el.name,end=", ")
                else:
                    print(row_el,end=", ")
        print("\nrelation      ",end="")
        
        print( relation_map[i['relation']],end="")
        try:
            if not len(i['base']):
                pass
                # print("!!!empty!!!",end="")
            else:
                print("\nBASE      ",end="")
                for base_el in i['base']:
                    if isinstance(base_el, Lexeme):
                        if base_el.code==15:
                            print("¶",end=", ")
                        else:
                            print(base_el.name,end=", ")
                    else:
                        print(base_el,end=", ")
        except KeyError:
            pass
