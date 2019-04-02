# !/usr/bin/python3
# -- coding: utf-8 --
from PyQt5.QtWidgets import QPlainTextEdit,QDialog, QWidget, QVBoxLayout, QApplication, QFileDialog, QMessageBox, QHBoxLayout, \
                         QFrame, QTextEdit, QToolBar, QComboBox, QLabel, QAction, QLineEdit, QToolButton, QMenu, \
                             QMainWindow,QTabWidget,QTableWidget,QPushButton,QTableWidgetItem
from PyQt5.QtGui import QIcon, QPainter, QTextFormat, QColor, QTextCursor, QKeySequence, QClipboard, QTextCharFormat, QPalette
from PyQt5.QtCore import Qt, QVariant, QRect, QDir, QFile, QFileInfo, QTextStream, QRegExp, QSettings,QSize, QObject,pyqtSlot,pyqtSignal

from compiler.LexicalAnalyzer import *
#from SyntaxAnalyzer import *
#from SyntaxAnalyzer2 import *
import compiler.transition_table
import easygui
from compiler.AscendingAnalysis import RelationTableMaker
import compiler.grammar_poliz as grammar
from compiler.SyntaxAnalyzer3 import SyntaxAnalyzer3

class GUILogic(QDialog):
    def __init__(self):
        # super().__init__()
        super(GUILogic ,self).__init__()
        self.tableMaker = RelationTableMaker(grammar.grammar)
        self.priority_table=[
            ['('],
            [')','+','-'],
            ['*','/']
        ]



    def make_connection(self,app):
        self.app = app
        self.dump_relation_table()
        # app.compileButton.clicked.connect(self.compile_handler)
        # app.clickedd.connect(self.on_clickedd)
        # app.compileButton.clicked.connect(self.compile_handler)
        app.compileButton.clicked.connect(self.compile_handler)

    def compile_handler(self):
        # text = "a* (b+4)/-2 * (1 + 1)\n"
        text= self.app.editor.toPlainText()+"\n" #getText()
        print(text)
        lexer = LexicalAnalyzer(text)
        try:
            (t_lexemes,t_idns,t_constants) = lexer.run()
            self.dump_tables(t_lexemes,t_idns,t_constants)
            sAn = SyntaxAnalyzer3(t_lexemes,t_idns,t_constants,self.tableMaker)
            parse_table = sAn.run()

            self.request_variables(t_idns)

            self.analyze(parse_table,t_lexemes)

        except TranslatorException as ex:
            print(ex)
            self.app.textEditStatusBar.setText(ex.__class__.__name__+"\n"+str(ex))      

    def analyze(self,parse_table,t_lexemes):
        self.dump_analysis_table(parse_table)
        poliz = self.build_poliz(t_lexemes)
        output=poliz
        result = self.compute_poliz(output)
        self.app.textEditStatusBar.setText("success\n"+result)

    def dump_tables(self,t_lexemes,t_idns,t_constants):
        for key,lexeme in enumerate(t_constants):
            self.app.tableWidget_4.setItem(key,0, QTableWidgetItem(str(lexeme.id)))
            self.app.tableWidget_4.setItem(key,1, QTableWidgetItem(lexeme.name))
            self.app.tableWidget_4.setItem(key,2, QTableWidgetItem(lexeme.type))

        for key,lexeme in enumerate(t_idns):
            self.app.tableWidget_3.setItem(key,0, QTableWidgetItem(str(lexeme.id)))
            self.app.tableWidget_3.setItem(key,1, QTableWidgetItem(lexeme.name))
            self.app.tableWidget_3.setItem(key,2, QTableWidgetItem(lexeme.type))
            self.app.tableWidget_3.setItem(key,3, QTableWidgetItem(str(lexeme.line)))

        for key,lexeme in enumerate(t_lexemes):
            f1=f2=f3=""
            if lexeme.code==LexicalAnalyzer.IDN_CODE:
                f1 = lexeme.fid
            if lexeme.code==LexicalAnalyzer.CON_CODE:
                f2 = lexeme.fid
            if lexeme.code==LexicalAnalyzer.LAB_CODE:
                f3 = lexeme.fid
            # lexeme_table += lexeme_pattern.format(lexeme.id,lexeme.line,name,lexeme.code,f1,f2,f3
            name = lexeme.name if lexeme.name!='\n' else '¶'
            self.app.tableWidget_2.setItem(key,0, QTableWidgetItem(str(lexeme.id)))
            self.app.tableWidget_2.setItem(key,1, QTableWidgetItem(str(lexeme.line)))
            self.app.tableWidget_2.setItem(key,2, QTableWidgetItem(name))
            self.app.tableWidget_2.setItem(key,3, QTableWidgetItem(str(lexeme.code)))
            self.app.tableWidget_2.setItem(key,4, QTableWidgetItem(f1))
            self.app.tableWidget_2.setItem(key,5, QTableWidgetItem(f2))
            self.app.tableWidget_2.setItem(key,6, QTableWidgetItem(f3))

    def dump_relation_table(self):
        relationTable = self.tableMaker.getRelationTable()
        elementsNames = self.tableMaker.getElements()
        array=['','=','<','>']

        text = ""
        for index,element in enumerate(elementsNames):
            # text+="{:15}{}\n".format(element," ".join([str(i) if i!=0 else '.' for i  in relationTable[index] ]))
            text+="{:15}{}\n".format(element," ".join([array[i] if i!=0 else '.' for i  in relationTable[index] ]))
            # element+"\t"+" ".join([str(i) for i in relationTable[index]])+"\n"

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

        self.app.textEditBar5.setText(text_labels+text)
        # (1.0,text_labels+text)  
               
    def request_variables(self,t_idns):
        self.variables={}
        for idn in t_idns:
            myvar = easygui.enterbox("Enter "+idn.name)
            #myvar = 5
            self.variables.update({idn.name:myvar})

    def dump_analysis_table(self,parse_table):
        relation_map=['','=','<','>']
        # print(parse_table)
        for count,i in enumerate(parse_table):
            print("\n",'='*150,end="")
            print("\n i = ",count,"\nstack      ",end="")
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

    def dump_poliz_building_step(self,widget,iteration,input,output,stack,message=""):
        it=iteration
        output_str=", ".join([i.name for i in output])
        input_str=", ".join([i.name for i in input])
        stack_str=", ".join([i.name for i in stack])
        widget.setItem(it,2, QTableWidgetItem(input_str))
        widget.setItem(it,1, QTableWidgetItem(stack_str))
        widget.setItem(it,0, QTableWidgetItem(output_str))
        widget.setItem(it,3, QTableWidgetItem(message))

    def build_poliz(self,t_lexemes):
        def findPriority(lexeme):
            for key,i in enumerate(self.priority_table):
                if lexeme.name in i:
                    return key
            return None

        input = t_lexemes
        stack=[]
        output=[]
        it=-1
        while len(input):
            lexeme = input[0]

            if lexeme.code==LexicalAnalyzer.IDN_CODE or lexeme.code==LexicalAnalyzer.CON_CODE:
                it+=1
                output.append(lexeme)
                input.pop(0)
                message=lexeme.name+" на виход"
                self.dump_poliz_building_step(self.app.tableWidget_7,it,input,output,stack,message)
        
            elif lexeme.name=="(":
                el = input.pop(0)   
                stack.append(el)
            else:
                #if len(stack):
                while len(stack) and findPriority(stack[-1]) >= findPriority(lexeme):
                    # print("!!!!!!!!!!!!!",findPriority(stack[-1]),findPriority(lexeme))
                    it+=1
                    el = stack.pop()
                    if el.name!="(":
                        output.append(el) 
                    message=el.name+" на виход со стека "
                    self.dump_poliz_building_step(self.app.tableWidget_7,it,input,output,stack,message)
                else:
                    it+=1
                    l = input.pop(0)       
                    if l.name!=")":
                        stack.append(l)
                    else:
                        stack.pop()
                    message=l.name+" в стек "
                    self.dump_poliz_building_step(self.app.tableWidget_7,it,input,output,stack,message)
        
        while(len(stack)):
            it+=1
            el = stack.pop()
            if el.name!="(":
                output.append(el) 
            message=el.name+" на виход со стека "
            self.dump_poliz_building_step(self.app.tableWidget_7,it,input,output,stack,message)

        output2 = list(map(lambda lexeme: lexeme.name,output))
        print(output2)

        return output

    def compute_poliz(self,output):
        var_stack=[]

        output_str=", ".join([i.name for i in output])
        self.app.tableWidget_8.setItem(0,2, QTableWidgetItem(output_str))
        self.app.tableWidget_8.setItem(0,1, QTableWidgetItem(output[0].name))

        it2=0
        while len(output):
            self.app.tableWidget_8.setItem(it2,1, QTableWidgetItem(output[0].name))
            self.app.tableWidget_8.setItem(it2,2, QTableWidgetItem(output_str))
            it2+=1

            a = output[0]
            if a.code==LexicalAnalyzer.IDN_CODE:
                val =  self.variables.get(a.name)
                var_stack.append(val )
                self.app.tableWidget_8.setItem(it2-1,1, QTableWidgetItem(output[0].name+" = "+str(val)))
                output.pop(0)
            elif a.code==LexicalAnalyzer.CON_CODE:
                var_stack.append(a.name)
                output.pop(0)
            else:
                action = output.pop(0).name
                if action=="+":
                    res = float(var_stack[-2])+ float(var_stack[-1])
                elif action=="-":
                    res = float(var_stack[-2])- float(var_stack[-1])
                elif action=="*":
                    res = float(var_stack[-2])* float(var_stack[-1])
                elif action=="/":
                    res = float(var_stack[-2])/ float(var_stack[-1])
                var_stack.pop()
                var_stack.pop()
                var_stack.append(res)
                try:
                    self.app.tableWidget_8.setItem(it2,1, QTableWidgetItem(output[0].name))
                    self.app.tableWidget_8.setItem(it2,2, QTableWidgetItem(output_str))
                except IndexError:
                    pass
            output_str=", ".join([i.name for i in output])
            input_str=", ".join([str(i) for i in var_stack])
            self.app.tableWidget_8.setItem(it2,0, QTableWidgetItem(input_str))
        return str(var_stack[0])