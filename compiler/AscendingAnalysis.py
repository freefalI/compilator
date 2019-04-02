import numpy as np
np.set_printoptions(threshold=np.inf)
from itertools import chain 
from .classes import Lexeme
# chain.from_iterable(list_of_lists)
#  [[1,2,3],[5,6,7]] => [1,2,3,5,6,7]


from tkinter import *
from . import grammar_poliz as grammar
class RelationTableMaker:
    def __init__(self,grammar): 
        self.grammar = grammar
        self.terminals = []
        self.nonterminals=[]
        self.relationMatrix = None
        self.all_elements_dict={}
        self.equals_elements=[] # elements that have equals relation, [i,j,el1,el2]
        # self.number_of_nonterminals=None
        self.conflicts={}
        self.all_elements_dict=None

        self.process()
    def ruleHasAlternatives(self,rule):
        for i in rule:
            if isinstance(i,tuple):
                return True
        return False

    def addElement(self,element):
        if  self.isTerminal(element):
            if element not in self.terminals:
                self.terminals.append(element)
        else:
            if element not in self.nonterminals:
                self.nonterminals.append(element)

    def fillElements(self):
        #fill sel.terminals and self.nonterminals with grammar elements
        for nonterminal in self.grammar.keys():
            self.nonterminals.append(nonterminal)

        for nonterminal in self.grammar.keys():
            right_part_of_rule = self.grammar[nonterminal]
            if self.ruleHasAlternatives(right_part_of_rule):
                right_part_of_rule = list(chain.from_iterable(right_part_of_rule))
            for element in right_part_of_rule:
                self.addElement(element)
            
    def buildRelationEquals(self):
        def _buildRelaionEqualsForRule(rule):
            for index,element in enumerate(rule[:-1]):
                i = self.all_elements_dict[element]
                j = self.all_elements_dict[rule[index+1]]
                self.relationMatrix[i][j] = 1
                self.equals_elements.append((i,j,element,rule[index+1]))

        for nonterminal in self.grammar.keys():
            right_part_of_rule = self.grammar[nonterminal]

            if self.ruleHasAlternatives(right_part_of_rule):
                for variant in right_part_of_rule:
                    _buildRelaionEqualsForRule(variant)
            else:
                _buildRelaionEqualsForRule(right_part_of_rule)


    def isTerminal(self,element):
        return not  (element[0]=='<' and element[-1]=='>')
    def isNonTerminal(self,element):
        return not  self.isTerminal(element)
    
    def _first_plus_recursion(self,element,first_plus):
        def inner(rule):
            if  self.isNonTerminal(rule[0]):
                if rule[0] not in first_plus:
                    first_plus.append(rule[0])
                    self._first_plus_recursion(rule[0],first_plus)
            else:
                if rule[0] not in first_plus:
                    first_plus.append(rule[0])

        rule = self.grammar[element]
        if self.ruleHasAlternatives(rule):
            for variant in rule:
                inner(variant)
        else:
            inner(rule)

    def firstPlus(self,element):
        first_plus = []
        self._first_plus_recursion(element,first_plus)
        return first_plus

    def _last_plus_recursion(self,element,last_plus):
        rule = self.grammar[element]
        if self.ruleHasAlternatives(rule):
            for variant in rule:
                if  self.isNonTerminal(variant[-1]):
                    if variant[-1] not in last_plus:
                        last_plus.append(variant[-1])
                        self._last_plus_recursion(variant[-1],last_plus)
                else:
                    if variant[-1] not in last_plus:
                        last_plus.append(variant[-1])
        else:
            if  self.isNonTerminal(rule[-1]):
                if rule[-1] not in last_plus:
                    last_plus.append(rule[-1])
                    self._last_plus_recursion(rule[-1],last_plus)
            else:
                if rule[-1] not in last_plus:
                    last_plus.append(rule[-1])

    def lastPlus(self,element):
        last_plus = []
        self._last_plus_recursion(element,last_plus)
        return last_plus

    def buildRelationLess(self):
        left_half_of_table = [i for i in self.equals_elements if i[1]<=len(self.nonterminals)-1]
        for (i,j,el1,el2) in left_half_of_table:
            first_plus = self.firstPlus(el2)
            for element in first_plus:
                j = self.all_elements_dict[element]
                if self.relationMatrix[i][j]==0 or self.relationMatrix[i][j]==2:#no conflict
                    self.relationMatrix[i][j] = 2
                else:# conflict
                    self.conflicts.update({(i,j):['=','<']})


    def buildRelationGreater(self):
        top_half_of_table = [i for i in self.equals_elements if i[0]<=len(self.nonterminals)-1]
        for (i,j,el1,el2) in top_half_of_table:
            last_plus = self.lastPlus(el1)
            for element in last_plus:
                i = self.all_elements_dict[element]
                if self.relationMatrix[i][j]==0 or self.relationMatrix[i][j]==3:#no conflict
                    self.relationMatrix[i][j] = 3
                else:#conflict
                    if self.conflicts.get((i,j)):#triple conflict
                        if '>' not in self.conflicts[(i,j)]:
                            self.conflicts[(i,j)].append('>')
                    else:
                        self.conflicts.update({(i,j):['=','>']})
            #3.2            
            if self.isNonTerminal(el2):     
                first_plus = self.firstPlus(el2)
                for a in last_plus:
                    for b in first_plus:
                        i = self.all_elements_dict[a]
                        j = self.all_elements_dict[b]
                        if self.relationMatrix[i][j]==0 or self.relationMatrix[i][j]==3:#no conflict
                                self.relationMatrix[i][j] = 3
                        else:# conflict
                            if self.conflicts.get((i,j)):#triple conflict
                                if '>' not in self.conflicts[(i,j)]:
                                    self.conflicts[(i,j)].append('>')
                            else:
                                self.conflicts.update({(i,j):['=','>']})
    
    def process(self):    
        self.fillElements()
        list_ = self.nonterminals + self.terminals
        self.all_elements_dict = {value:index for index,value in enumerate(list_)}
        matrix_size = len(list_)
        self.relationMatrix = np.zeros((matrix_size,matrix_size),np.int8) 
        self.buildRelationEquals()
        # print(self.equals_elements)
        self.buildRelationLess()
        self.buildRelationGreater()

        print(self.all_elements_dict)
        print("matrix size = ",matrix_size)
        # print (self.nonterminals)
        # print (self.terminals)
        # print(list_)
        # print(self.relationMatrix)
        np.savetxt("relationTable",self.relationMatrix,fmt='%.d')
        print('Conflicts:')
        print("number of conflicts = ",len(self.conflicts))
        for key in self.conflicts.keys():
            print(key,self.conflicts[key])
        # print(,*self.conflicts.keys(),*self.conflicts.values(),sep='\n')
        
    def getRelationTable(self):
        return self.relationMatrix
    def getElements(self):
        return self.nonterminals + self.terminals
    def relationBetween(self,lexeme1,lexeme2):
        if lexeme1==None:
            return 2
        if lexeme2==None:
            return 3
        else:
            IDN_CODE = 100
            CON_CODE = 101
            LAB_CODE = 102
            # try:
            if isinstance(lexeme1, Lexeme):
                if lexeme1.code==IDN_CODE:
                    i = self.all_elements_dict["idn"]
                elif lexeme1.code==CON_CODE:
                    i = self.all_elements_dict["constant"]
                elif lexeme1.code==LAB_CODE:
                    i = self.all_elements_dict["lab"]
                elif lexeme1.code==15:
                    i = self.all_elements_dict["¶"]
                else:
                    i = self.all_elements_dict[lexeme1.name]
            # except AttributeError:
            else:
                i = self.all_elements_dict[lexeme1]

            if isinstance(lexeme2, Lexeme):

                if lexeme2.code==IDN_CODE:
                    j = self.all_elements_dict["idn"]
                elif lexeme2.code==CON_CODE:
                    j = self.all_elements_dict["constant"]
                elif lexeme2.code==LAB_CODE:
                    j = self.all_elements_dict["lab"]
                elif lexeme2.code==15:
                    j = self.all_elements_dict["¶"]
                else:
                    j = self.all_elements_dict[lexeme2.name]
            else:
                j = self.all_elements_dict[lexeme2]

            return self.relationMatrix[i][j]

if __name__ == "__main__":
        
    # tableMaker = RelationTableMaker(grammar.grammar)
    
    from tkinter.ttk import *

    class App(Frame):

        def __init__(self, parent):
            Frame.__init__(self, parent)
            self.CreateUI()
            self.LoadTable()
            self.grid(sticky = (N,S,W,E))
            parent.grid_rowconfigure(0, weight = 1)
            parent.grid_columnconfigure(0, weight = 1)

        def CreateUI(self):
            tv = Treeview(self)


            tableMaker = RelationTableMaker(grammar.grammar)
            self.relationTable = tableMaker.getRelationTable()
            self.elementsNames = tableMaker.getElements()
            self.array=['','=','<','>']
            text = ""
            for index,element in enumerate(elementsNames):
                # text+="{:15}{}\n".format(element," ".join([str(i) if i!=0 else '.' for i  in relationTable[index] ]))
                text+="{:15}{}\n".format(element," ".join([array[i] if i!=0 else '.' for i  in relationTable[index] ]))
                # element+"\t"+" ".join([str(i) for i in relationTable[index]])+"\n"


            # print(elementsNames)
            tv['columns'] = elementsNames#('starttime', 'endtime', 'status')
            tv.heading("#0", text='Sources')
            tv.column("#0", anchor="w",width=40,)
            for index,element in enumerate(elementsNames):
                # text+="{:15}{}\n".format(element," ".join([str(i) if i!=0 else '.' for i  in relationTable[index] ]))
                # text+="{:15}{}\n".format(element," ".join([array[i] if i!=0 else '.' for i  in relationTable[index] ]))
                element.split()
                tv.heading(index, text="\n".join(element))
                tv.column(index, anchor='center',width=22)
                
            # tv.column("#0", anchor="w",width=60)
            # tv.heading("#0", text='Sources')
            # tv.column("#0", anchor="w",width=60)
            '''
            tv.heading('starttime', text='Start Time')
            tv.column('starttime', anchor='center', width=100)
            tv.heading('endtime', text='End Time')
            tv.column('endtime', anchor='center', width=100)
            tv.heading('status', text='Status')
            tv.column('status', anchor='center', width=100)
            '''
            tv.grid(sticky = (N,S,W,E))
            self.treeview = tv
            self.grid_rowconfigure(0, weight = 10)
            self.grid_columnconfigure(0, weight = 1)

        def LoadTable(self):
            for index,element in enumerate(self.elementsNames):
                self.treeview.insert('', 'end', text=element, values=(list([array[i] if i!=0 else '.' for i  in relationTable[index] ])))
                if index==5:
                    break



    tableMaker = RelationTableMaker(grammar.grammar)
    relationTable = tableMaker.getRelationTable()
    elementsNames = tableMaker.getElements()
    array=['','=','<','>']

    text = ""
    for index,element in enumerate(elementsNames):
        # text+="{:15}{}\n".format(element," ".join([str(i) if i!=0 else '.' for i  in relationTable[index] ]))
        text+="{:15}{}\n".format(element," ".join([array[i] if i!=0 else '.' for i  in relationTable[index] ]))
        # element+"\t"+" ".join([str(i) for i in relationTable[index]])+"\n"



    #

    max_element_len = max([len(i) for i in elementsNames])
    # print (max_element_len)

    # inverted_labels = np.zeros((max_element_len,len(elementsNames)))
    inverted_labels =[ [0 for i in range(max_element_len)] for i in range(len(elementsNames))]

    for index,row in enumerate(inverted_labels):
        inverted_label = elementsNames[index][::-1]
        # print(inverted_label)
        for index2,char in enumerate(inverted_label):
            row[index2] = char


    # print(inverted_labels)
    def rotated(array_2d):
        list_of_tuples = zip(*array_2d[::-1])
        return [list(elem) for elem in list_of_tuples]
        # return map(list, list_of_tuples)
    inverted_labels2 = rotated(inverted_labels)
    inverted_labels2 = rotated(inverted_labels2)
    inverted_labels2 = rotated(inverted_labels2)
    # inverted_labels2=[
    #     [ inverted_labels[len(inverted_labels[0])-i][len(inverted_labels)-j] 
    #         for j,_ in enumerate(inverted_labels)
    #         ] 
    #             for i,_ in enumerate(inverted_labels)
    #     ]
    # print(inverted_labels2)
    text_labels = ""
    for index,element in enumerate(inverted_labels2):
        text_labels+=" "*15# text+="{:15}{}\n".format(element," ".join([str(i) if i!=0 else '.' for i  in relationTable[index] ]))
        for index2,element2 in enumerate(element):
        # text_labels+="{}{}\n".format(element," ".join())
            if element2 == 0:
                text_labels+="  "
            else:
                text_labels+=str(element2)+" "

        text_labels+="\n"
    # print(text_labels)

    root = Tk()

    from time import sleep 
    from PIL import Image, ImageTk
    from tkinter.ttk import *
    new_window = Toplevel()
    new_window.title("new window")
    frame = Frame(new_window,height = 50) 
    frame.pack(fill=BOTH)

    text_area = Text(frame,font='Consolas 12',height = 50,wrap=NONE)
    text_area.insert(1.0,text_labels+text)
    # np.savetxt(text_area,relationTable,fmt='%.d')
    text_area.pack(fill=BOTH)#fill=X,side=LEFT)
    new_window.state('zoomed')

    # App(root)
    root.mainloop()

    