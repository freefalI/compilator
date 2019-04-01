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


def tablesToString(t_lexemes,t_idns,t_constants): 
    lexeme_table = ""
    for lexeme in t_lexemes:
        lexeme_table +=str(lexeme)+"\n"
    idn_table = ""
    for idn in t_idns:
        idn_table +=str(idn)+"\n"
    constant_table = ""
    for constant in t_constants:
        constant_table +=str(constant)+"\n"
    return(lexeme_table,idn_table,constant_table)

def makeTables(t_lexemes,t_idns,t_constants,t_transitions=None):
    if t_transitions:

        lexeme_pattern =  "{:^5}|{:^5}|{:<20}|{:<10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^20}|\n"
        lexeme_table =""+ lexeme_pattern.format("id","line","lexeme","code","idn code","con code","label code","state","stack")+"═"*107+"\n"
        for index,lexeme in enumerate(t_lexemes):
            name = lexeme.name if lexeme.name!='\n' else '¶'
            f1=f2=f3=""
            if lexeme.code==LexicalAnalyzer.IDN_CODE:
                f1 = lexeme.fid
            if lexeme.code==LexicalAnalyzer.CON_CODE:
                f2 = lexeme.fid
            if lexeme.code==LexicalAnalyzer.LAB_CODE:
                f3 = lexeme.fid
            stack = "["+",".join([str(i) for i in t_transitions[index][1]])+"]"
            
            lexeme_table += lexeme_pattern.format(lexeme.id,lexeme.line,name,lexeme.code,f1,f2,f3,t_transitions[index][0],stack)

    else:
        lexeme_pattern =  "{:^5}|{:^5}|{:<20}|{:<10}|{:^10}|{:^10}|{:^10}|\n"
        lexeme_table =""+ lexeme_pattern.format("id","line","lexeme","code","idn code","con code","label code")+"═"*77+"\n"
        for lexeme in t_lexemes:
            name = lexeme.name if lexeme.name!='\n' else '¶'
            f1=f2=f3=""
            if lexeme.code==LexicalAnalyzer.IDN_CODE:
                f1 = lexeme.fid
            if lexeme.code==LexicalAnalyzer.CON_CODE:
                f2 = lexeme.fid
            if lexeme.code==LexicalAnalyzer.LAB_CODE:
                f3 = lexeme.fid
            lexeme_table += lexeme_pattern.format(lexeme.id,lexeme.line,name,lexeme.code,f1,f2,f3)


    idn_pattern = "{:^5}|{:<20}|{:<10}|{:^5}|\n"
    idn_table = "" +idn_pattern.format("id","name","type","line")+"═"*44+"\n"
    for idn in t_idns:
        line = idn.line if idn.line else ''
        # print(idn)
        idn_table +=idn_pattern.format(idn.id,idn.name,idn.type,line)

    constant_pattern = "{:^5}|{:<10}|{:<10}|\n"
    constant_table = ""+ constant_pattern.format("id","name","type")+"═"*28+"\n"
    for constant in t_constants:
        constant_table += constant_pattern.format(constant.id,constant.name,constant.type)

    return(lexeme_table,idn_table,constant_table)



class GUILogic(QDialog):
    def __init__(self):
        # super().__init__()
        super(GUILogic ,self).__init__()
        # self.app = app
        # app.clickedd.connect(self.on_clickedd)
        pass
        # self.main()
        # self.show()

    def make_connection(self,app):
        self.app = app
        print("main called")
        
        

        self.tableMaker = RelationTableMaker(grammar.grammar)
        
        
        relationTable = self.tableMaker.getRelationTable()
        elementsNames = self.tableMaker.getElements()
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

        app.textEditBar5.setText(text_labels+text)
        # (1.0,text_labels+text)  
               
        # app.compileButton.clicked.connect(self.compile_handler)
        # app.clickedd.connect(self.on_clickedd)
        # app.compileButton.clicked.connect(self.compile_handler)
        app.compileButton.clicked.connect(self.compile_handler)



    #     @pyqtSlot(int)
    # def get_slider_value(self, val):
    #     self.progressBar.setValue(val)
        # self.progressBar.setValue(val)

    # def edit_bottom_textarea(method_to_decorate):
    #     def wrapper(*args, **kwargs):
    #         args[0].text_area_bottom.config(state=NORMAL)
    #         # try:
    #         method_to_decorate(*args, **kwargs)
    #         # except Exception as ex:
    #             # print(ex)
    #         args[0].text_area_bottom.config(state=DISABLED)
    #     return wrapper
    
    # @edit_bottom_textarea
    # def open_file_handler(self,event):
    #     filename = askopenfilename(filetypes = (("txt files","*.txt"),("all files","*.*"))) 
    #     try:
    #         file = open(filename,'r')
    #         text = file.readlines()
    #         # num_lines = sum(1 for line in text)
    #         file.close()

    #         # line_numbers = "\n".join(str(i) for i in range(1,num_lines+1))
            
    #         # self.text_area_line_numbers.config(state=NORMAL)
    #         # self.text_area_line_numbers.delete('1.0', END)             
    #         # self.text_area_line_numbers.insert(1.0,line_numbers)
    #         # self.text_area_line_numbers.config(state=DISABLED)

    #         self.text_area_top.delete('1.0', END) 
    #         self.text_area_top.insert(1.0,"".join(text))
    #     except UnicodeDecodeError as ex:
    #         self.text_area_bottom.delete('1.0', END) 
    #         self.text_area_bottom.insert(1.0,"Wrong file format!")

    # @edit_bottom_textarea
    # @pyqtSlot(bool)
    def compile_handler(self):


        # self.text_area_bottom.delete('1.0', END) 
        # text = self.text_area_top.get('1.0', END)  

        # text = 'asdfsadf'
        # text = "a* (b+4)/-2 * (1 + 1)\n"
        text= self.app.editor.toPlainText() #getText()
        print(text)
        lexer = LexicalAnalyzer(text)
        try:
            
                    
            #------------------------------------------------------------------------


           
            # App(root)
            # root.mainloop()


            #------------------------------------------------------------------------



            (t_lexemes,t_idns,t_constants) = lexer.run()

            for key,lexeme in enumerate(t_constants):
                print(lexeme)
                self.app.tableWidget_4.setItem(key,0, QTableWidgetItem(str(lexeme.id)))
                self.app.tableWidget_4.setItem(key,1, QTableWidgetItem(lexeme.name))
                self.app.tableWidget_4.setItem(key,2, QTableWidgetItem(lexeme.type))
                # self.app.tableWidget_4.setItem(lexeme.id,3, QTableWidgetItem(lexeme.line))

            for key,lexeme in enumerate(t_idns):
                print(lexeme)
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
                print(lexeme)
                self.app.tableWidget_2.setItem(key,0, QTableWidgetItem(str(lexeme.id)))
                self.app.tableWidget_2.setItem(key,1, QTableWidgetItem(str(lexeme.line)))
                self.app.tableWidget_2.setItem(key,2, QTableWidgetItem(name))
                self.app.tableWidget_2.setItem(key,3, QTableWidgetItem(str(lexeme.code)))
                self.app.tableWidget_2.setItem(key,4, QTableWidgetItem(f1))
                self.app.tableWidget_2.setItem(key,5, QTableWidgetItem(f2))
                self.app.tableWidget_2.setItem(key,6, QTableWidgetItem(f3))

            # print("0000",t_lexemes)
            # print("11111",t_idns)
            # print("2222",t_constants)
            # return
            
                      # tableMaker = RelationTableMaker(grammar.grammar)
            # relation_table = tableMaker.getRelationTable()
            sAn = SyntaxAnalyzer3(t_lexemes,t_idns,t_constants,self.tableMaker)
            # sAn = SyntaxAnalyzer2(t_lexemes,t_idns,t_constants,transition_table.transition_table)
            # state_table = sAn.run()
            parse_table = sAn.run()
            # if  state_table == True:
                # state_table=None
            
            # self.e = Entry(self.top_frame)
            # self.e.pack()
            self.variables={}
            for idn in t_idns:
                myvar = easygui.enterbox("Enter "+idn.name)
                #myvar = 5
                self.variables.update({idn.name:myvar})
                print(myvar)

            
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

            # text2="".join(tablesToString(t_lexemes,t_idns,t_constants))
            ttt = makeTables(t_lexemes,t_idns,t_constants)
            # text2="".join(makeTables(t_lexemes,t_idns,t_constants))
            # self.app.textEditBar2.setText(ttt[0])
            # self.app.textEditBar3.setText(ttt[1])
            # self.app.textEditBar4.setText(ttt[2])





            # text2=""+str(parse_table)
            # text2="successful compilation" if parse_table else False 
            # self.text_area_bottom.insert(1.0,text2)
          


            priority_table=[
                ['('],
                [')','+','-'],
                ['*','/']
            ]
            
            def findPriority(lexeme):
                for key,i in enumerate(priority_table):
                    if lexeme.name in i:
                        return key
                print("_________________________l0000000000000000000000",lexeme)
                return None

            #input = list(map(lambda lexeme: lexeme.name,t_lexemes))
            input = t_lexemes
            stack=[]
            output=[]
            IDN_CODE = 100
            CON_CODE = 101
            LAB_CODE = 102
            it=-1
            while len(input):
                #lexeme = input.pop(0)
                lexeme = input[0]
                # if lexeme.name=="(":

                if lexeme.code==IDN_CODE or lexeme.code==CON_CODE:
                    it+=1

                    output.append(lexeme)
                    input.pop(0)
                    print(lexeme.name,"на виход")
                    # self.app.textEditBar7.append(lexeme.name+"на виход")

                    output_str=", ".join([i.name for i in output])
                    input_str=", ".join([i.name for i in input])
                    stack_str=", ".join([i.name for i in stack])
                    print(input_str)
                    print(stack_str)
                    print(output_str)
                    self.app.tableWidget_7.setItem(it,2, QTableWidgetItem(input_str))
                    self.app.tableWidget_7.setItem(it,1, QTableWidgetItem(stack_str))
                    self.app.tableWidget_7.setItem(it,0, QTableWidgetItem(output_str))
                    self.app.tableWidget_7.setItem(it,3, QTableWidgetItem(lexeme.name+" на виход"))
                
                elif lexeme.name=="(":
                    l = input.pop(0)   
                    stack.append(l)
                else:
                    #if len(stack):
                    while len(stack) and findPriority(stack[-1]) >= findPriority(lexeme):
                            print("!!!!!!!!!!!!!",findPriority(stack[-1]),findPriority(lexeme))
                            it+=1

                            el = stack.pop()
                            print(el.name,"на виход со стека ")
                            # self.app.textEditBar7.append(el.name+"на виход со стека ")

                            if el.name!="(":
                                output.append(el) 

                            output_str=", ".join([i.name for i in output])
                            input_str=", ".join([i.name for i in input])
                            stack_str=", ".join([i.name for i in stack])
                            print(input_str)
                            print(stack_str)
                            print(output_str)  

                            self.app.tableWidget_7.setItem(it,2, QTableWidgetItem(input_str))
                            self.app.tableWidget_7.setItem(it,1, QTableWidgetItem(stack_str))
                            self.app.tableWidget_7.setItem(it,0, QTableWidgetItem(output_str))
                            self.app.tableWidget_7.setItem(it,3, QTableWidgetItem(el.name+" на виход со стека "))
                            # self.tableWidget_8.setItem(X,Y, QTableWidgetItem("TEXT"))
                            # continue
                    else:
                        it+=1

                        l = input.pop(0)       
                        print(l.name,"в стек ")  
                        # self.app.textEditBar7.append(lexeme.name+"в стек ")

                        if l.name!=")":
                            stack.append(l)
                        else:
                            stack.pop()
                        output_str=", ".join([i.name for i in output])
                        input_str=", ".join([i.name for i in input])
                        stack_str=", ".join([i.name for i in stack])
                        print(input_str)
                        print(stack_str)
                        print(output_str)
                        self.app.tableWidget_7.setItem(it,2, QTableWidgetItem(input_str))
                        self.app.tableWidget_7.setItem(it,1, QTableWidgetItem(stack_str))
                        self.app.tableWidget_7.setItem(it,0, QTableWidgetItem(output_str))
                        self.app.tableWidget_7.setItem(it,3, QTableWidgetItem(l.name+" в стек "))
            
            while(len(stack)):
                it+=1

                el = stack.pop()
                print(el.name,"на виход со стека ")
                # self.app.textEditBar7.append(el.name+"на виход со стека ")

                if el.name!="(":
                    output.append(el) 

                output_str=", ".join([i.name for i in output])
                input_str=", ".join([i.name for i in input])
                stack_str=", ".join([i.name for i in stack])
                print(input_str)
                print(stack_str)
                print(output_str)  

                self.app.tableWidget_7.setItem(it,2, QTableWidgetItem(input_str))
                self.app.tableWidget_7.setItem(it,1, QTableWidgetItem(stack_str))
                self.app.tableWidget_7.setItem(it,0, QTableWidgetItem(output_str))
                self.app.tableWidget_7.setItem(it,3, QTableWidgetItem(el.name+" на виход со стека "))
                # for i in output:
                    # output_str+=""
                # print(stack,output,input)     
            
            # output_str=", ".join([i.name for i in output])
            # input_str=", ".join([i.name for i in input])
            # stack_str=", ".join([i.name for i in stack])
            # print(input_str)
            # print(stack_str)
            # print(output_str)
            # self.app.tableWidget_7.setItem(it,0, QTableWidgetItem(input_str))
            # self.app.tableWidget_7.setItem(it,1, QTableWidgetItem(stack_str))
            # self.app.tableWidget_7.setItem(it,2, QTableWidgetItem(output_str))
            # self.tableWidget.setRowCount(4)
            
            # set column count
            # self.tableWidget.setColumnCount(2)


            while len(stack):
                el=stack.pop()
                print(el.name,"на виход со стека ")
                if el.name!="(":
                    output.append(el)


            output2 = list(map(lambda lexeme: lexeme.name,output))

            print(output2)
            # compute poliz 
            var_stack=[]

            output_str=", ".join([i.name for i in output])
            print(output_str)  

            self.app.tableWidget_8.setItem(0,2, QTableWidgetItem(output_str))
            self.app.tableWidget_8.setItem(0,1, QTableWidgetItem(output[0].name))

            it2=0
            while len(output):
                self.app.tableWidget_8.setItem(it2,0, QTableWidgetItem(input_str))
                self.app.tableWidget_8.setItem(it2,1, QTableWidgetItem(output[0].name))

                # self.app.tableWidget_7.setItem(it,1, QTableWidgetItem(stack_str))
                self.app.tableWidget_8.setItem(it2,2, QTableWidgetItem(output_str))
                it2+=1

                a = output[0]
                if a.code==IDN_CODE:
                    val =  self.variables.get(a.name)
                    var_stack.append(val )
                    self.app.tableWidget_8.setItem(it2-1,1, QTableWidgetItem(output[0].name+" = "+str(val)))
                    output.pop(0)

                elif a.code==CON_CODE:
                    #val =  self.variables.get(a.name)
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
                    # it2+=1
                    try:
                        self.app.tableWidget_8.setItem(it2,1, QTableWidgetItem(output[0].name))
                        self.app.tableWidget_8.setItem(it2,0, QTableWidgetItem(input_str))

                        self.app.tableWidget_8.setItem(it2,2, QTableWidgetItem(output_str))
                    except IndexError:
                        pass
                # it2+=1

                output_str=", ".join([i.name for i in output])
                input_str=", ".join([str(i) for i in var_stack])
                # stack_str=", ".join([i.name for i in stack])
                print(input_str)
                # print(stack_str)
                print(output_str)  
                self.app.tableWidget_8.setItem(it2,0, QTableWidgetItem(str(var_stack[0])))
                # self.app.tableWidget_8.setItem(it2,1, QTableWidgetItem(output[it2].name))
                # self.app.tableWidget_8.setItem(it2,2, QTableWidgetItem(output_str))


                # self.app.tableWidget_7.setItem(it,1, QTableWidgetItem(stack_str))
                # self.app.tableWidget_7.setItem(it,3, QTableWidgetItem(el.name+" на виход со стека "))
            print(var_stack)
                # elif a.code==IDN_CODE or a.code==CON_CODE:
                #     pas

            self.app.textEditStatusBar.setText("success\n"+str(var_stack[0]))
        except TranslatorException as ex:
            print(ex)
            self.app.textEditStatusBar.setText(ex.__class__.__name__+"\n"+str(ex))

            



    # @edit_bottom_textarea
    # def save_handler(self,event):
    #     filename = asksaveasfilename(filetypes = (("txt files","*.txt"),("all files","*.*")))
    #     file = open(filename,'w')
    #     file.write(self.text_area_top.get(1.0,END))
    #     file.close()
    #     # self.text_area_top.delete('1.0', END) 
    #     # self.text_area_top.insert(1.0,text)

