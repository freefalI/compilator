# !/usr/bin/python3
# -- coding: utf-8 --
from PyQt5.QtWidgets import (
    QPlainTextEdit,
    QDialog,
    QWidget,
    QVBoxLayout,
    QApplication,
    QFileDialog,
    QMessageBox,
    QHBoxLayout,
    QFrame,
    QTextEdit,
    QToolBar,
    QComboBox,
    QLabel,
    QAction,
    QLineEdit,
    QToolButton,
    QMenu,
    QMainWindow,
    QTabWidget,
    QTableWidget,
    QPushButton,
    QTableWidgetItem,
    QInputDialog
)
from PyQt5.QtGui import (
    QIcon,
    QPainter,
    QTextFormat,
    QColor,
    QTextCursor,
    QKeySequence,
    QClipboard,
    QTextCharFormat,
    QPalette,
)
from PyQt5.QtCore import (
    Qt,
    QVariant,
    QRect,
    QDir,
    QFile,
    QFileInfo,
    QTextStream,
    QRegExp,
    QSettings,
    QSize,
    QObject,
    pyqtSlot,
    pyqtSignal,
)

# from compiler.LexicalAnalyzer import *
from compiler.LexicalAnalyzerOld import *

# from SyntaxAnalyzer import *
# from SyntaxAnalyzer2 import *
import compiler.transition_table
import easygui
import traceback

# from compiler.AscendingAnalysis import RelationTableMaker
import compiler.grammar as grammar
from compiler.SyntaxAnalyzer3 import SyntaxAnalyzer3
from compiler.SyntaxAnalyzer2 import SyntaxAnalyzer2
from compiler.transition_table import transition_table


class GUILogic(QDialog):
    def __init__(self):
        # super().__init__()
        super(GUILogic, self).__init__()
        # self.tableMaker = RelationTableMaker(grammar.grammar)
        self.priority_table = [["("], [")", "+", "-"], ["*", "/"]]
        self.line=-1
    def make_connection(self, app):
        self.app = app
        # self.dump_relation_table()
        # app.compileButton.clicked.connect(self.compile_handler)
        # app.clickedd.connect(self.on_clickedd)
        # app.compileButton.clicked.connect(self.compile_handler)
        app.compileButton.clicked.connect(self.compile_handler)

    def compile_handler(self):
        # text = "a* (b+4)/-2 * (1 + 1)\n"
        text = self.app.editor.toPlainText() + "\n"  # getText()
        print(text)
        lexer = LexicalAnalyzer(text)
        try:
            (t_lexemes, t_idns, t_constants) = lexer.run()
            self.t_lexemes = t_lexemes
            self.t_idns = t_idns
            self.t_constants = t_constants
            self.app.tableWidget_2.clearContents()
            self.app.tableWidget_3.clearContents()
            self.app.tableWidget_4.clearContents()

            self.dump_tables()
            # sAn = SyntaxAnalyzer3(t_lexemes,t_idns,t_constants,self.tableMaker)

         

            sAn = SyntaxAnalyzer2(
                t_lexemes, t_idns, t_constants, transition_table
            )
            parse_table = sAn.run()

            #self.request_variables(t_idns)

            self.analyze()
           
            print("END OF COMPILING")
            
          

        except TranslatorException as ex:
            print(ex)
            self.app.textEditStatusBar.setText(ex.__class__.__name__ + "\n" + str(ex))
        except Exception as ex:
            print(ex)
            self.app.textEditStatusBar.setText( traceback.format_exc())

    def analyze(self):
        #self.dump_analysis_table(parse_table)
        self.line=-1

        self.app.tableWidget_7.clearContents()
        self.app.tableWidget_8.clearContents()

        self.variables_values={}
        self.full_poliz=[]
        self.labels={}
        self.label_count=1
        self.app.textEditStatusBar.setText("syntax analysis successful" )
        self.label_index=100
        poliz = self.build_poliz(self.t_lexemes)
        poliz2=[]
        for i in poliz:
            if isinstance(i,Lexeme):
                # output2.append(i.name)
                poliz2.append(i)
            else:
                # output2.append(i)
                poliz2.append(Lexeme(None,None,name=i))

        poliz=poliz2
        self.poliz=poliz[:]
        #output = poliz

        #result = 
        #self.app.textEditStatusBar.setText("success\n" + result)
        #self.app.textEditStatusBar.append("poliz= "+poliz)
        print(poliz)
        output=''
        for i in poliz:
            if isinstance(i,Lexeme):
                output+=i.name+'  '
            else:
                output+=i+'  '
        # stack_str = ", ".join([i.name for i in stack])
        self.app.tableWidget_7.setItem(self.line+1, 0, QTableWidgetItem(output))
        self.find_labels(poliz)
        self.compute_poliz(poliz)

    def find_labels(self,poliz):
        self.lexemes_adresses=[]
        for key,i in enumerate(poliz):
            if isinstance(i, Lexeme):
                if i.name[-1]==":":
                    self.lexemes_adresses.append((i,key))
            else:
                if i[-1]==":":
                    self.lexemes_adresses.append((i,key))
            
        print(888)


    def dump_tables(self):
        for key, lexeme in enumerate(self.t_constants):
            self.app.tableWidget_4.setItem(key, 0, QTableWidgetItem(str(lexeme.id)))
            self.app.tableWidget_4.setItem(key, 1, QTableWidgetItem(lexeme.name))
            self.app.tableWidget_4.setItem(key, 2, QTableWidgetItem(lexeme.type))

        for key, lexeme in enumerate(self.t_idns):
            self.app.tableWidget_3.setItem(key, 0, QTableWidgetItem(str(lexeme.id)))
            self.app.tableWidget_3.setItem(key, 1, QTableWidgetItem(lexeme.name))
            self.app.tableWidget_3.setItem(key, 2, QTableWidgetItem(lexeme.type))
            self.app.tableWidget_3.setItem(key, 3, QTableWidgetItem(str(lexeme.line)))

        for key, lexeme in enumerate(self.t_lexemes):
            f1 = f2 = f3 = ""
            if lexeme.code == LexicalAnalyzer.IDN_CODE:
                f1 = lexeme.fid
            if lexeme.code == LexicalAnalyzer.CON_CODE:
                f2 = lexeme.fid
            if lexeme.code == LexicalAnalyzer.LAB_CODE:
                f3 = lexeme.fid
            # lexeme_table += lexeme_pattern.format(lexeme.id,lexeme.line,name,lexeme.code,f1,f2,f3
            name = lexeme.name if lexeme.name != "\n" else "¶"
            self.app.tableWidget_2.setItem(key, 0, QTableWidgetItem(str(lexeme.id)))
            self.app.tableWidget_2.setItem(key, 1, QTableWidgetItem(str(lexeme.line)))
            self.app.tableWidget_2.setItem(key, 2, QTableWidgetItem(name))
            self.app.tableWidget_2.setItem(key, 3, QTableWidgetItem(str(lexeme.code)))
            self.app.tableWidget_2.setItem(key, 4, QTableWidgetItem(f1))
            self.app.tableWidget_2.setItem(key, 5, QTableWidgetItem(f2))
            self.app.tableWidget_2.setItem(key, 6, QTableWidgetItem(f3))

    def dump_relation_table(self):
        relationTable = self.tableMaker.getRelationTable()
        elementsNames = self.tableMaker.getElements()
        array = ["", "=", "<", ">"]

        text = ""
        for index, element in enumerate(elementsNames):
            # text+="{:15}{}\n".format(element," ".join([str(i) if i!=0 else '.' for i  in relationTable[index] ]))
            text += "{:15}{}\n".format(
                element,
                " ".join([array[i] if i != 0 else "." for i in relationTable[index]]),
            )
            # element+"\t"+" ".join([str(i) for i in relationTable[index]])+"\n"

        max_element_len = max([len(i) for i in elementsNames])
        # print (max_element_len)
        # inverted_labels = np.zeros((max_element_len,len(elementsNames)))
        inverted_labels = [
            [0 for i in range(max_element_len)] for i in range(len(elementsNames))
        ]

        for index, row in enumerate(inverted_labels):
            inverted_label = elementsNames[index][::-1]
            # print(inverted_label)
            for index2, char in enumerate(inverted_label):
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
        for index, element in enumerate(inverted_labels2):
            text_labels += (
                " " * 15
            )  # text+="{:15}{}\n".format(element," ".join([str(i) if i!=0 else '.' for i  in relationTable[index] ]))
            for index2, element2 in enumerate(element):
                # text_labels+="{}{}\n".format(element," ".join())
                if element2 == 0:
                    text_labels += "  "
                else:
                    text_labels += str(element2) + " "

            text_labels += "\n"
        # print(text_labels)

        self.app.textEditBar5.setText(text_labels + text)
        # (1.0,text_labels+text)

    def request_variables(self, t_idns):
        self.variables = {}
        for idn in t_idns:
            myvar = easygui.enterbox("Enter " + idn.name)
            # myvar = 5
            self.variables.update({idn.name: myvar})

    def dump_analysis_table(self, parse_table):
        relation_map = ["", "=", "<", ">"]
        # print(parse_table)
        for count, i in enumerate(parse_table):
            print("\n", "=" * 150, end="")
            print("\n i = ", count, "\nstack      ", end="")
            if not len(i["stack"]):
                print("!!!empty!!!", end="")
            else:
                for st_el in i["stack"]:
                    if isinstance(st_el, Lexeme):
                        if st_el.code == 15:
                            print("¶", end=", ")
                        else:
                            print(st_el.name, end=", ")
                    else:
                        print(st_el, end=", ")

            print("\ninput_row      ", end="")
            if not len(i["input_row"]):
                print("!!!empty!!!", end="")
            else:
                for row_el in i["input_row"]:
                    if isinstance(row_el, Lexeme):
                        if row_el.code == 15:
                            print("¶", end=", ")
                        else:
                            print(row_el.name, end=", ")
                    else:
                        print(row_el, end=", ")
            print("\nrelation      ", end="")

            print(relation_map[i["relation"]], end="")
            try:
                if not len(i["base"]):
                    pass
                    # print("!!!empty!!!",end="")
                else:
                    print("\nBASE      ", end="")
                    for base_el in i["base"]:
                        if isinstance(base_el, Lexeme):
                            if base_el.code == 15:
                                print("¶", end=", ")
                            else:
                                print(base_el.name, end=", ")
                        else:
                            print(base_el, end=", ")
            except KeyError:
                pass

    def dump_poliz_building_step(
        self, widget, iteration, input, output, stack, message=""
    ):
        it = iteration
        if len(message):
            output_str = ", ".join([i.name for i in output])
            input_str = ", ".join([i.name for i in input])
            stack_str = ", ".join([i.name for i in stack])
            widget.setItem(it, 2, QTableWidgetItem(input_str))
            widget.setItem(it, 1, QTableWidgetItem(stack_str))
            widget.setItem(it, 0, QTableWidgetItem(output_str))
            widget.setItem(it, 3, QTableWidgetItem(message))
        else:
            widget.setItem(it, 0, QTableWidgetItem(output))

    def build_poliz(self,lexemes,skip=True):
        i=0
        
        if skip:
            while lexemes[i].name !="{":
                i+=1
                continue
            i+=2  

        full_poliz=[]

        while True:
            try:
                l = lexemes[i]
            except IndexError:
                break  
            #print(l)
            cases={
                'cout': self.build_cout_poliz,
                'cin': self.build_cin_poliz,
                'if': self.build_if_poliz,
                'for': self.build_for_poliz,
                'goto': self.build_goto_poliz
            }
            if cases.get(l.name):
                lexemes2=[lexemes[i]]
                print(cases.get(l.name))
                if skip:
                    while lexemes[i].code!=15:
                        i+=1
                        lexemes2.append(lexemes[i])
                        continue
                    lexemes2.pop()  
                else:
                    lexemes2.pop()
                    lexemes2.extend(lexemes)
                    # lexemes2.pop()    
                poliz = cases.get(l.name)(lexemes2)
                print(123)
                print(poliz)
                print(123)
                if skip:
                    full_poliz.extend(poliz)
                else:
                    return poliz
                #self.full_poliz.extend(poliz)


            elif l.code == LexicalAnalyzer.IDN_CODE:
                lexemes2=[lexemes[i]]
                if skip:
                    while lexemes[i].code!=15:
                        i+=1
                        lexemes2.append(lexemes[i])
                        continue
                    lexemes2.pop()   
                else:
                    lexemes2.pop()

                    lexemes2.extend(lexemes)
                    # lexemes2.pop()    
                ternar=False
                for x in lexemes2:
                    if x.name=="?":
                        ternar=True
                if ternar:
                    poliz=self.build_assignment_poliz_ternar(lexemes2)
                else:
                    poliz=self.build_assignment_poliz(lexemes2)
                print(123)
                print(poliz)
                print(123)
                if skip:
                    full_poliz.extend(poliz)
                else:
                    return poliz
                


            elif l.code == LexicalAnalyzer.LAB_CODE:
                lexemes2=[lexemes[i]]
                if skip:
                    while self.t_lexemes[i].code!=15:
                        i+=1
                        lexemes2.append(lexemes[i])
                        continue
                    lexemes2.pop()   
                else:
                    lexemes2.pop()

                    lexemes2.extend(lexemes)
                    # lexemes2.pop()     
                poliz = self.build_label_point_poliz(lexemes2)
                print(123)
                print(poliz)
                print(123)
                if skip:
                    full_poliz.extend(poliz)
                else:
                    return poliz



            elif l.name=="}":  
                break
            else:
                if skip:
                    raise BuildException

            # if l.name in ["int","float","label"]:
                # print('definition')

            # else:
                # raise BuildException
            i+=1
        # self.build_arifmetic_expression_poliz()
        # def findPriority(lexeme):
        #     for key, i in enumerate(self.priority_table):
        #         if lexeme.name in i:
        #             return key
        #     return None

        # input = self.t_lexemes
        # stack = []
        # output = []
        # it = -1
        # while len(input):
        #     lexeme = input[0]

        #     if (
        #         lexeme.code == LexicalAnalyzer.IDN_CODE
        #         or lexeme.code == LexicalAnalyzer.CON_CODE
        #     ):
        #         it += 1
        #         output.append(lexeme)
        #         input.pop(0)
        #         message = lexeme.name + " на виход"
        #         self.dump_poliz_building_step(
        #             self.app.tableWidget_7, it, input, output, stack, message
        #         )

        #     elif lexeme.name == "(":
        #         el = input.pop(0)
        #         stack.append(el)
        #     else:
        #         # if len(stack):
        #         while len(stack) and findPriority(stack[-1]) >= findPriority(lexeme):
        #             # print("!!!!!!!!!!!!!",findPriority(stack[-1]),findPriority(lexeme))
        #             it += 1
        #             el = stack.pop()
        #             if el.name != "(":
        #                 output.append(el)
        #             message = el.name + " на виход со стека "
        #             self.dump_poliz_building_step(
        #                 self.app.tableWidget_7, it, input, output, stack, message
        #             )
        #         else:
        #             it += 1
        #             l = input.pop(0)
        #             if l.name != ")":
        #                 stack.append(l)
        #             else:
        #                 stack.pop()
        #             message = l.name + " в стек "
        #             self.dump_poliz_building_step(
        #                 self.app.tableWidget_7, it, input, output, stack, message
        #             )

        # while len(stack):
        #     it += 1
        #     el = stack.pop()
        #     if el.name != "(":
        #         output.append(el)
        #     message = el.name + " на виход со стека "
        #     self.dump_poliz_building_step(
        #         self.app.tableWidget_7, it, input, output, stack, message
        #     )

        # output2 = list(map(lambda lexeme: lexeme.name, output))
        # print(output2)

        # return output
        return full_poliz
    def print(self,lexemes):
        for i in lexemes:
            print("{0:10} {0:10} ".format(i.name,i.code))
    def build_cout_poliz(self,lexemess):
        self.print(lexemess)
        lexemes=lexemess[:]
        result=[]
        cout=lexemes.pop(0)
        for key,i in enumerate(lexemes):
            if key%2==1:
                result.append(i)
                result.append("PRINT")
        output=''
        for i in result:
            if isinstance(i,Lexeme):
                output+=i.name+','
            else:
                output+=i+','
        self.line += 1
        self.dump_poliz_building_step(
                        self.app.tableWidget_7, self.line, '', output, '', ''
                    )
        return result
        # lexemes=lexemess[:]
        # result=[]
        # label = lexemes.pop()
        # result.append(label.name + "БП")

    def build_cin_poliz(self,lexemess):
        self.print(lexemess)
        lexemes=lexemess[:]
        result=[]
        cout=lexemes.pop(0)
        for key,i in enumerate(lexemes):
            if key%2==1:
                result.append(i)
                result.append("READ")

        self.line += 1
        output=''
        for i in result:
            if isinstance(i,Lexeme):
                output+=i.name+','
            else:
                output+=i+','

        self.dump_poliz_building_step(
                        self.app.tableWidget_7, self.line, '', output, '', ''
                    )
        return result
    def build_condition_poliz(self,lexemess):
        self.print(lexemess)
        lexemes=lexemess[:]
        result=[]
        expr1=[]
        expr2=[]
        flag=False
        for key,i in enumerate(lexemes):
            if i.code >=20 and i.code <=25:
                flag=True
                cond_op_index=key
                continue
            if not flag:
                expr1.append(i)
            else:
                expr2.append(i)

        poliz1 = self.build_arifmetic_expression_poliz(expr1)
        poliz2 = self.build_arifmetic_expression_poliz(expr2)

        print(poliz1)
        print(poliz2)
        result.extend(poliz1)
        result.extend(poliz2)
        result.append(lexemes[cond_op_index])
        # print(result)
        output=''
        for i in result:
            if isinstance(i,Lexeme):
                output+=i.name+','
            else:
                output+=i+','
        self.line += 1
        self.dump_poliz_building_step(
                        self.app.tableWidget_7, self.line, '', output, '', ''
                    )


        return result

    def build_if_poliz(self,lexemess):
        self.print(lexemess)
        lexemes=lexemess[:]
        result=[]
        lexemes.pop(0)
        cond=[]
        for i in lexemes[:]:
            if i.name=="then":
                break
            cond.append(i)
            # lexemes.pop(0)
        cond_poliz = self.build_condition_poliz(cond)

        
        label = lexemes.pop()
        result.extend(cond_poliz)
        # self.labels.update({"m"+str(self.label_count+1):true})
        result.append("m УПХ")
        # result.append(label)
        result.append(label.name + " БП")
        result.append("m:")
        self.line += 1
        output=''
        for i in result:
            if isinstance(i,Lexeme):
                output+=i.name+','
            else:
                output+=i+','
        self.dump_poliz_building_step(
                        self.app.tableWidget_7, self.line, '', output, '', ''
                    )

        return result
    def build_for_poliz(self,lexemess):
        
        lexemes=lexemess[:]
        lexemes.pop(0)
        # a = a>5 ? 4-4 : 25
        index1=0# index of by
        index2=0# index of while
        index3=0# index of do

        for key,i in enumerate(lexemes):
            if i.name=="by" and index1==0:
                index1=key
            if i.name=="while" and index2==0:
                index2=key
            if i.name=="do" and index3==0:
                index3=key

        expr1=lexemes[0:index1]
        expr2=lexemes[index1+1:index2]
        cond=lexemes[index2+1:index3]
        op=lexemes[index3+1:]

        poliz_cond=self.build_condition_poliz(cond)
        poliz_expr1=self.build_arifmetic_expression_poliz(expr1)
        poliz_expr2=self.build_arifmetic_expression_poliz(expr2)
        poliz_op = self.build_poliz(op,False)
        # poliz_op = "123"

        var=lexemes[0]
        result=[]
        #result.append(var)
        # result.append("for")
        result.extend(poliz_expr1)
        result.append("rj")
        result.append('number@1')
        result.append("=")
        result.append("m"+str(self.label_index)+":")
        result.append("rj+1")
        result.extend(poliz_expr2)
        result.append("=")
        result.append("rj")
        result.append("number@0")
        result.append("==")
        result.append("m"+str(self.label_index+1)+" УПХ")
        result.append(var)
        result.append(var)
        result.append("rj+1")
        result.append("+")
        result.append("=")
        result.append("m"+str(self.label_index+1)+":")
        result.append("rj")
        result.append("number@0")
        result.append("=")
        result.extend(poliz_cond)
        result.append("m"+str(self.label_index+2)+" УПХ")
        result.extend(poliz_op)
        result.append("m"+str(self.label_index)+" БП")
        result.append("m"+str(self.label_index+2)+":")
        self.label_index+=3
        self.line += 1
        output=''
        for i in result:
            if isinstance(i,Lexeme):
                output+=i.name+','
            else:
                output+=i+','
        self.dump_poliz_building_step(
                        self.app.tableWidget_7, self.line, '', output, '', ''
                    )
        return result

    def build_goto_poliz(self,lexemess):
        self.print(lexemess)
        lexemes=lexemess[:]
        result=[]
        label = lexemes.pop()
        result.append(label.name + " БП")
        return result
    def build_assignment_poliz_ternar(self,lexemess):
        self.print(lexemess)
       
        lexemes=lexemess[:]
        result=[lexemes.pop(0)]
        assign = lexemes.pop(0)
        # a = a>5 ? 4-4 : 25
        index1=0# index of ?
        index2=0# index of :

        for key,i in enumerate(lexemes):
            if i.name=="?":
                index1=key
            if i.name==":":
                index2=key
        cond=lexemes[0:index1]
        expr1=lexemes[index1+1:index2]
        expr2=lexemes[index2+1:]

        poliz_cond=self.build_condition_poliz(cond)
        poliz_expr1=self.build_arifmetic_expression_poliz(expr1)
        poliz_expr2=self.build_arifmetic_expression_poliz(expr2)

        result.extend(poliz_cond)
        result.append("m1 УПХ")
        result.extend(poliz_expr1)
        result.append("m2 БП")
        result.append("m1:")
        result.extend(poliz_expr2)
        result.append("m2:")
        result.append(assign)
        
        return result
        

    def build_assignment_poliz(self,lexemess):
        self.print(lexemess)
        lexemes=lexemess[:]
        result=[lexemes.pop(0)]
        assign = lexemes.pop(0)

        poliz = self.build_arifmetic_expression_poliz(lexemes)
        result.extend(poliz)
        result.append(assign)
       
        self.line += 1
        output=''
        for i in result:
            if isinstance(i,Lexeme):
                output+=i.name+','
            else:
                output+=i+','
        self.dump_poliz_building_step(
                        self.app.tableWidget_7, self.line, '', output, '', ''
                    )

        return result


    def build_label_point_poliz(self,lexemess):
        self.print(lexemess)
        lexemes=lexemess[:]
        result=[]
        label = lexemes.pop(0)
        result.append(label.name + ":")

        self.line += 1
        output=''
        for i in result:
            if isinstance(i,Lexeme):
                output+=i.name+','
            else:
                output+=i+','
        self.dump_poliz_building_step(
                        self.app.tableWidget_7, self.line, '', output, '', ''
                    )
        return result

    def build_arifmetic_expression_poliz(self,lexemess):
        def findPriority(lexeme):
            for key, i in enumerate(self.priority_table):
                if lexeme.name in i:
                    return key
            return None

        input = lexemess[:]
        stack = []
        output = []
        # it = -1
        self.line+=1
        while len(input):
            lexeme = input[0]

            if (
                lexeme.code == LexicalAnalyzer.IDN_CODE
                or lexeme.code == LexicalAnalyzer.CON_CODE
            ):
                self.line += 1
                output.append(lexeme)
                input.pop(0)
                message = lexeme.name + " на виход"
                self.dump_poliz_building_step(
                    self.app.tableWidget_7, self.line, input, output, stack, message
                )

            elif lexeme.name == "(":
                el = input.pop(0)
                stack.append(el)
            else:
                # if len(stack):
                while len(stack) and findPriority(stack[-1]) >= findPriority(lexeme):
                    # print("!!!!!!!!!!!!!",findPriority(stack[-1]),findPriority(lexeme))
                    self.line += 1
                    el = stack.pop()
                    if el.name != "(":
                        output.append(el)
                    message = el.name + " на виход со стека "
                    self.dump_poliz_building_step(
                        self.app.tableWidget_7, self.line, input, output, stack, message
                    )
                else:
                    self.line += 1
                    l = input.pop(0)
                    if l.name != ")":
                        stack.append(l)
                    else:
                        stack.pop()
                    message = l.name + " в стек "
                    self.dump_poliz_building_step(
                        self.app.tableWidget_7, self.line, input, output, stack, message
                    )

        while len(stack):
            self.line += 1
            el = stack.pop()
            if el.name != "(":
                output.append(el)
            message = el.name + " на виход со стека "
            self.dump_poliz_building_step(
                self.app.tableWidget_7, self.line, input, output, stack, message
            )

        output2 = list(map(lambda lexeme: lexeme.name, output))
        print(output2)
        print(output)
        return output



    def compute_poliz(self, poliz):

        self.cout=''
        self.variables_values={}
        self.labels_list={}
        var_stack = []
        for i in poliz:
            print(i)
        #return
        output2 =[]
      
        poliz_str= ", ".join([i.name for i in poliz])

        self.app.tableWidget_8.setItem(0, 2, QTableWidgetItem(poliz_str))
        self.app.tableWidget_8.setItem(0, 1, QTableWidgetItem(poliz[0].name))

        it2 = 0
        while len(poliz):
            self.app.tableWidget_8.setItem(it2, 1, QTableWidgetItem(poliz[0].name))
            self.app.tableWidget_8.setItem(it2, 2, QTableWidgetItem(poliz_str))
            it2 += 1

            a = poliz[0]
            if a.code == LexicalAnalyzer.IDN_CODE:
                #val = self.variables.get(a.name)
                # val = 25
                var_stack.append(a)

                val = self.variables_values.get(a.name,"undefined")

                
                self.app.tableWidget_8.setItem(
                    it2 - 1, 1, QTableWidgetItem(poliz[0].name + " = " + str(val))
                )
                poliz.pop(0)
            elif a.code == LexicalAnalyzer.CON_CODE:
                var_stack.append(a.name)
                poliz.pop(0)
            elif 'number@' in a.name:
                print('qqqqqqqqq')
                var_stack.append(a.name.split('@')[1])
                poliz.pop(0)
            elif "УПХ" in a.name:
                cond_res = var_stack.pop()
                if cond_res not  in [True,False]:
                    raise RuntimeException("no bool in stack")
                poliz.pop(0)
                if cond_res==False:
                    label = a.name.split()[0]
                    found=False
                    while len(poliz):
                        l = poliz.pop(0)
                        if l.name==label+":":
                            found=True
                            print("label "+label+" found")
                            break
                        
                    if not found:
                        raise NotFoundLabelRuntimeException("1label "+label+" not found")

            elif "БП" in a.name:
                label = a.name.split()[0]
                poliz.pop(0)
                found=False
                while len(poliz):
                    l = poliz.pop(0)
                    if l.name==label+":":
                        found=True
                        print("label "+label+" found")
                        break
                    
                if not  found:
                    # print([i[0] for i in self.lexemes_adresses])
                    index=None
                    for i in self.lexemes_adresses:
                        if label+":" ==i[0].name:
                            index=i[1]
                            print('label '+label+' before found')

                    if index==None:
                        raise NotFoundLabelRuntimeException("2label "+label+" not found")
                    else:
                        poliz = self.poliz[index:]
                        print(poliz)

            elif a.name=="for":
                print('zzz')
                #return
                poliz.pop(0)
                zpc = poliz[0]
            
            elif a.name[0]=="r":# and  a.name[1:].isdigit():
                var_stack.append(a)
                print(a)          
                poliz.pop(0)
                

            else:
                action = poliz.pop(0).name
                if action in ["+","-","*","/"]:
                    operand2 = var_stack.pop()
                    operand1 = var_stack.pop()

                    if isinstance(operand1,Lexeme):
                        #operand1=operand1.name
                        operand1 = float(self.variables_values.get(operand1.name,"undefined"))
                    else:
                        operand1=float(operand1)

                    if isinstance(operand2,Lexeme):
                        #operand2=operand2.name
                        operand2 = float(self.variables_values.get(operand2.name,"undefined"))

                    else:
                        operand2=float(operand2)

                    if action=="+":
                        res = operand1 + operand2
                    elif  action=="-":
                        res = operand1 - operand2
                    elif  action=="*":
                        res = operand1 * operand2
                    elif  action=="/":
                        res = operand1 / operand2
                  
                    var_stack.append(res)


                elif action in [">","<",">=","<=","==","!="]:
                    operand2 = var_stack.pop()
                    operand1 = var_stack.pop()
                    if isinstance(operand1,Lexeme):
                        #operand1=operand1.name
                        operand1 = float(self.variables_values.get(operand1.name,"undefined"))
                    else:
                        operand1=float(operand1)

                    if isinstance(operand2,Lexeme):
                        #operand2=operand2.name
                        operand2 = float(self.variables_values.get(operand2.name,"undefined"))

                    else:
                        operand2=float(operand2)

                    if action=="<":
                        res = operand1 < operand2
                    elif  action==">":
                        res = operand1 > operand2
                    elif  action=="<=":
                        res = operand1 <= operand2
                    elif  action==">=":
                        res = operand1 >= operand2
                    elif action=="==":
                        res = operand1 == operand2
                    elif action=="!=":
                        res = operand1 != operand2

                    var_stack.append(res)


                elif action == "PRINT":
                    var = var_stack.pop()
                    value = self.variables_values.get(var.name,"undefined")
                    self.cout+=value+"\n"

                elif action == "READ":
                    var = var_stack.pop()
                    var_fid = int(var.fid)
                    idn = self.t_idns[var_fid-1]
                    idn_type=idn.type

                    if idn_type=="int":
                        v, okPressed = QInputDialog.getInt(self, "Get integer",idn.name+":")
                        # v, okPressed = QInputDialog.getInt(self, "Get integer",idn.name+":", 0, 0, 100, 1)
                        if okPressed:
                            print(v)
                    elif idn_type=="float":
                        # v, okPressed = QInputDialog.getDouble(self, "Get double",idn.name+":", 10.05, 0, 100, 10)
                        v, okPressed = QInputDialog.getDouble(self, "Get double",idn.name+":",0.0,decimals=10)
                        if okPressed:
                            print(v)

                    if not okPressed:
                        raise RuntimeException("value of "+idn.name+" haven`t inputed correctly",var.line)
                    self.variables_values.update({idn.name:str(v)})

                elif action == "=":
                    value = str(var_stack.pop())
                    variable = var_stack.pop()
                    value_type = ''

                    if '.'  in value:
                        value_type='float'
                    else:
                        value_type='int' 
                    if variable.fid ==None:
                        self.variables_values.update({variable.name:value})
                    else:
                        var_fid = int(variable.fid)
                        idn = self.t_idns[var_fid-1]
                        idn_type=idn.type

                        if idn_type=="int":
                            v = value.split('.')[0]
                            self.variables_values.update({idn.name:v})
                        else:
                            self.variables_values.update({idn.name:value})
                 
                else:
                    print("STRANGE LEXEME:",a)     

                try:
                    self.app.tableWidget_8.setItem(
                        it2, 1, QTableWidgetItem(poliz[0].name)
                    )
                    self.app.tableWidget_8.setItem(it2, 2, QTableWidgetItem(poliz_str))
                except IndexError:
                    pass

            # output2 =[]
            # for i in poliz:
            #     if isinstance(i,Lexeme):
            #         output2.append(i.name)
            #     else:
            #         output2.append(i)
            
            poliz_str= ", ".join([i.name for i in poliz])

            #poliz_str = ", ".join([i.name for i in output])
            input_str = ", ".join([str(i) for i in var_stack])
            self.app.tableWidget_8.setItem(it2, 0, QTableWidgetItem(input_str))
        print(self.cout)
        self.app.textEditStatusBar.setText(self.cout )

        #return str(var_stack[0])
