# !/usr/bin/python3
# -- coding: utf-8 --

from PyQt5.QtWidgets import (
    QPlainTextEdit,
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
    QHeaderView,
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
    QStandardItemModel,
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
import sys, os

from gui.number_bar import NumberBar


lineHighlightColor = QColor("#c6ffb3")


class CodeEditor(QMainWindow):
    clickedd = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(CodeEditor, self).__init__(parent)

        self.MaxRecentFiles = 5
        self.windowList = []
        self.recentFileActs = []
        self.setAttribute(Qt.WA_DeleteOnClose)
        # Editor Widget ...
        QIcon.setThemeName("Faenza-Dark")
        self.editor = QPlainTextEdit()
        self.editor.setStyleSheet(stylesheet2(self))
        self.editor.setFrameStyle(QFrame.NoFrame)
        self.editor.setStyleSheet("font-size: 12pt; font-family: Consolas;")

        self.editor.setTabStopWidth(14)
        self.extra_selections = []
        self.fname = ""
        self.filename = ""
        # Line Numbers ...
        self.numbers = NumberBar(self.editor)

        self.createActions()
        # Laying out...
        layoutH = QHBoxLayout()
        layoutH.setSpacing(1.5)
        layoutH.addWidget(self.numbers)
        layoutH.addWidget(self.editor)

        ### begin toolbar
        tb = QToolBar(self)
        tb.setWindowTitle("File Toolbar")

        self.newAct = QAction(
            "&New",
            self,
            shortcut=QKeySequence.New,
            statusTip="Create a new file",
            triggered=self.newFile,
        )
        self.newAct.setIcon(QIcon.fromTheme("document-new"))

        self.openAct = QAction(
            "&Open",
            self,
            shortcut=QKeySequence.Open,
            statusTip="open file",
            triggered=self.openFile,
        )
        self.openAct.setIcon(QIcon.fromTheme("document-open"))

        self.saveAct = QAction(
            "&Save",
            self,
            shortcut=QKeySequence.Save,
            statusTip="save file",
            triggered=self.fileSave,
        )
        self.saveAct.setIcon(QIcon.fromTheme("document-save"))

        self.saveAsAct = QAction(
            "&Save as ...",
            self,
            shortcut=QKeySequence.SaveAs,
            statusTip="save file as ...",
            triggered=self.fileSaveAs,
        )
        self.saveAsAct.setIcon(QIcon.fromTheme("document-save-as"))

        self.exitAct = QAction(
            "Exit",
            self,
            shortcut=QKeySequence.Quit,
            toolTip="Exit",
            triggered=self.handleQuit,
        )
        self.exitAct.setIcon(QIcon.fromTheme("application-exit"))

        ### tabs
        self.tabWidget = QTabWidget()
        self.tabWidget.setGeometry(QRect(10, 30, 821, 481))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        # self.tab_2 = QWidget()
        # self.tab_2.setObjectName("tab_2")
        # self.tabWidget.addTab(self.tab_2, "")

        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tableWidget_2 = QTableWidget(self.tab_2)
        self.tableWidget_2.setGeometry(QRect(0, 0, 1300, 600))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(7)
        self.tableWidget_2.setRowCount(500)
        self.tabWidget.addTab(self.tab_2, "")
        self.tableWidget_2.setHorizontalHeaderLabels(
            ["Номер", "Рядок", "Лексема", "Код", "Код idn", "Код const", "Код label"]
        )
        # id  |line |lexeme              |code      | idn code | con code |label code|

        # self.tableWidget_2.setFlags(self.tableWidget_2.flags() | Qt.ItemIsEditable)

        # self.textEditBar2 = QTextEdit(self.tab_2)
        # self.textEditBar2.setGeometry(QRect(0, 50, 801, 900))
        # self.textEditBar2.setObjectName("textEdit")
        # self.textEditBar2.setMaximumSize(QSize(1500, 500))
        # self.textEditBar2.setReadOnly(1)
        # self.textEditBar2.setStyleSheet('font-size: 12pt; font-family: Consolas;')

        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tableWidget_3 = QTableWidget(self.tab_3)
        self.tableWidget_3.setGeometry(QRect(0, 0, 1300, 600))
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(4)
        self.tableWidget_3.setRowCount(100)
        self.tabWidget.addTab(self.tab_3, "")
        self.tableWidget_3.setHorizontalHeaderLabels(
            ["Номер", "Значення", "Тип", "Рядок"]
        )

        # self.textEditBar3 = QTextEdit(self.tab_3)
        # self.textEditBar3.setGeometry(QRect(0, 50, 801, 900))
        # self.textEditBar3.setObjectName("textEdit")
        # self.textEditBar3.setMaximumSize(QSize(1500, 500))
        # self.textEditBar3.setReadOnly(1)
        # self.textEditBar3.setStyleSheet('font-size: 12pt; font-family: Consolas;')

        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tableWidget_4 = QTableWidget(self.tab_4)
        self.tableWidget_4.setGeometry(QRect(0, 0, 1300, 600))
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(3)
        self.tableWidget_4.setRowCount(100)
        self.tabWidget.addTab(self.tab_4, "")
        self.tableWidget_4.setHorizontalHeaderLabels(["Номер", "Значення", "Тип"])

        # self.textEditBar4 = QTextEdit(self.tab_4)
        # self.textEditBar4.setGeometry(QRect(0, 50, 801, 900))
        # self.textEditBar4.setObjectName("textEdit")
        # self.textEditBar4.setMaximumSize(QSize(1500, 500))
        # self.textEditBar4.setReadOnly(1)
        # self.textEditBar4.setStyleSheet('font-size: 12pt; font-family: Consolas;')

        self.tab_5 = QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tableWidget_5 = QTableWidget(self.tab_5)
        self.tableWidget_5.setGeometry(QRect(0, 0, 1300, 1200))
        self.tableWidget_5.setObjectName("tableWidget_5")
        self.tableWidget_5.setColumnCount(3)
        self.tableWidget_5.setRowCount(3)
        self.tabWidget.addTab(self.tab_5, "")

        self.textEditBar5 = QTextEdit(self.tab_5)
        self.textEditBar5.setGeometry(QRect(0, 0, 1340, 1200))
        self.textEditBar5.setObjectName("textEdit")
        self.textEditBar5.setMaximumSize(QSize(1500, 650))
        self.textEditBar5.setReadOnly(1)
        self.textEditBar5.setStyleSheet("font-size: 12pt; font-family: Consolas;")

        self.tab_6 = QWidget()
        self.tab_6.setObjectName("tab_6")
        self.tableWidget_6 = QTableWidget(self.tab_6)
        self.tableWidget_6.setGeometry(QRect(0, 0, 1300, 600))
        self.tableWidget_6.setObjectName("tableWidget_6")
        self.tableWidget_6.setColumnCount(3)
        self.tableWidget_6.setRowCount(3)
        self.tabWidget.addTab(self.tab_6, "")

        self.textEditBar6 = QTextEdit(self.tab_6)
        self.textEditBar6.setGeometry(QRect(0, 50, 801, 900))
        self.textEditBar6.setObjectName("textEdit")
        self.textEditBar6.setMaximumSize(QSize(1500, 500))
        self.textEditBar6.setReadOnly(1)
        self.textEditBar6.setStyleSheet("font-size: 12pt; font-family: Consolas;")

        self.tab_7 = QWidget()
        self.tab_7.setObjectName("tab_7")
        self.tableWidget_7 = QTableWidget(self.tab_7)
        self.tableWidget_7.setGeometry(QRect(0, 0, 1300, 600))
        self.tableWidget_7.setObjectName("tableWidget_7")
        self.tableWidget_7.setColumnCount(4)
        self.tableWidget_7.setRowCount(1000)
        self.tabWidget.addTab(self.tab_7, "")

        # self.textEditBar7 = QTextEdit(self.tab_7)
        # self.textEditBar7.setGeometry(QRect(0, 50, 801, 900))
        # self.textEditBar7.setObjectName("textEdit")
        # self.textEditBar7.setMaximumSize(QSize(1500, 500))
        # self.textEditBar7.setReadOnly(1)
        # self.textEditBar7.setStyleSheet('font-size: 12pt; font-family: Consolas;')

        self.header_7 = self.tableWidget_7.horizontalHeader()
        self.header_7.setSectionResizeMode(0, QHeaderView.Stretch)
        self.header_7.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.header_7.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.header_7.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        # self.table.setHorizontalHeaderLabels(['1', '2', '3', '4', '5'])
        self.tableWidget_7.setHorizontalHeaderLabels(
            ["Полиз", "Стек", "Вход", "Действие"]
        )

        self.tab_8 = QWidget()
        self.tab_8.setObjectName("tab_8")
        self.tableWidget_8 = QTableWidget(self.tab_8)
        self.tableWidget_8.setGeometry(QRect(0, 0, 1300, 600))
        self.tableWidget_8.setObjectName("tableWidget_8")
        self.tableWidget_8.setColumnCount(4)
        self.tableWidget_8.setRowCount(100)
        self.tabWidget.addTab(self.tab_8, "")

        self.header_8 = self.tableWidget_8.horizontalHeader()
        self.header_8.setSectionResizeMode(0, QHeaderView.Stretch)
        self.header_8.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.header_8.setSectionResizeMode(2, QHeaderView.Stretch)
        self.header_8.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        # self.table.setHorizontalHeaderLabels(['1', '2', '3', '4', '5'])
        self.tableWidget_8.setHorizontalHeaderLabels(
            ["Стек", "Текущий эллемент", "Полиз", "Действие"]
        )

        # self.model_8 = QStandardItemModel()
        # self.model_8.setHorizontalHeaderLabels(['Name', 'Age', 'Sex', 'Add'])
        # self.tableWidget_8.setModel(self.model_8)

        # self.textEditBar8 = QTextEdit(self.tab_8)
        # self.textEditBar8.setGeometry(QRect(0, 50, 801, 900))
        # self.textEditBar8.setObjectName("textEdit")
        # self.textEditBar8.setMaximumSize(QSize(1500, 500))
        # self.textEditBar8.setReadOnly(1)
        # self.textEditBar8.setStyleSheet('font-size: 12pt; font-family: Consolas;')

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "Програмний код")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Таблиця лексем")
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_3), "Таблиця iдентификаторiв"
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_4), "Таблиця констант"
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_5), "Таблиця вiдношень"
        )
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), "Граматика")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), "Полiз")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), "Полiз 2")

        ### find / replace toolbar
        self.tbf = QToolBar(self)
        self.tbf.setWindowTitle("Find Toolbar")
        self.findfield = QLineEdit()
        self.findfield.addAction(
            QIcon.fromTheme("edit-find"), QLineEdit.LeadingPosition
        )
        self.findfield.setClearButtonEnabled(True)
        self.findfield.setFixedWidth(150)
        self.findfield.setPlaceholderText("find")
        self.findfield.setToolTip("press RETURN to find")
        self.findfield.setText("")
        ft = self.findfield.text()
        self.findfield.returnPressed.connect(self.findText)
        self.tbf.addWidget(self.findfield)
        self.replacefield = QLineEdit()
        self.replacefield.addAction(
            QIcon.fromTheme("edit-find-and-replace"), QLineEdit.LeadingPosition
        )
        self.replacefield.setClearButtonEnabled(True)
        self.replacefield.setFixedWidth(150)
        self.replacefield.setPlaceholderText("replace with")
        self.replacefield.setToolTip("press RETURN to replace the first")
        self.replacefield.returnPressed.connect(self.replaceOne)
        self.tbf.addSeparator()
        self.tbf.addWidget(self.replacefield)
        self.tbf.addSeparator()

        self.tbf.addAction("replace all", self.replaceAll)
        self.tbf.addSeparator()

        # compile button

        self.compileButton = QPushButton(self.tbf)
        self.compileButton.setGeometry(QRect(0, 10, 87, 29))
        self.compileButton.setObjectName("pushButton")
        self.compileButton.setText("Compile")
        self.compileButton.setGeometry(QRect(0, 0, 300, 300))
        self.compileButton.setMaximumSize(QSize(100, 200))

        # satus bar
        self.textEditStatusBar = QTextEdit(self.tbf)
        self.textEditStatusBar.setGeometry(QRect(0, 50, 801, 101))
        self.textEditStatusBar.setObjectName("textEdit")
        self.textEditStatusBar.setMaximumSize(QSize(1500, 100))
        self.textEditStatusBar.setReadOnly(1)

        self.textEditStatusBar.setStyleSheet("font-size: 12pt; font-family: Courier;")

        layoutV = QVBoxLayout()

        bar = self.menuBar()
        bar.setMaximumSize(QSize(100, 100))
        self.filemenu = bar.addMenu("File")
        self.separatorAct = self.filemenu.addSeparator()
        self.filemenu.addAction(self.newAct)
        self.filemenu.addAction(self.openAct)
        self.filemenu.addAction(self.saveAct)
        self.filemenu.addAction(self.saveAsAct)
        self.filemenu.addSeparator()
        for i in range(self.MaxRecentFiles):
            self.filemenu.addAction(self.recentFileActs[i])
        self.updateRecentFileActions()
        self.filemenu.addSeparator()
        self.filemenu.addAction(self.exitAct)
        bar.setStyleSheet(stylesheet2(self))
        editmenu = bar.addMenu("Edit")
        editmenu.addAction(
            QAction(
                QIcon.fromTheme("edit-copy"),
                "Copy",
                self,
                triggered=self.editor.copy,
                shortcut=QKeySequence.Copy,
            )
        )
        editmenu.addAction(
            QAction(
                QIcon.fromTheme("edit-cut"),
                "Cut",
                self,
                triggered=self.editor.cut,
                shortcut=QKeySequence.Cut,
            )
        )
        editmenu.addAction(
            QAction(
                QIcon.fromTheme("edit-paste"),
                "Paste",
                self,
                triggered=self.editor.paste,
                shortcut=QKeySequence.Paste,
            )
        )
        editmenu.addAction(
            QAction(
                QIcon.fromTheme("edit-delete"),
                "Delete",
                self,
                triggered=self.editor.cut,
                shortcut=QKeySequence.Delete,
            )
        )
        editmenu.addSeparator()
        editmenu.addAction(
            QAction(
                QIcon.fromTheme("edit-select-all"),
                "Select All",
                self,
                triggered=self.editor.selectAll,
                shortcut=QKeySequence.SelectAll,
            )
        )

        layoutV.addWidget(self.tabWidget)
        # layoutV.addWidget(bar)
        # layoutV.addWidget(self.tbf)
        # layoutV.addLayout(layoutH)

        layoutH2 = QHBoxLayout()
        layoutH2.setSpacing(1.5)
        layoutH2.addWidget(bar)
        layoutH2.addWidget(self.tbf)
        layoutH2.addWidget(self.compileButton)

        layoutV2 = QVBoxLayout()
        # layoutV2.addWidget(bar)
        # layoutV2.addWidget(self.tbf)
        # layoutV2.addWidget(self.compileButton)
        layoutV2.addLayout(layoutH2)

        layoutV2.addLayout(layoutH)
        layoutV2.addWidget(self.textEditStatusBar)

        self.tab.setLayout(layoutV2)

        # layoutV3 = QVBoxLayout()
        # layoutV3.addWidget(self.tbf)
        # layoutV3.addWidget(bar)
        # layoutV3.addLayout(layoutH)

        # self.tab_2.setLayout(layoutV3)
        ### main window
        mq = QWidget(self)
        mq.setLayout(layoutV)

        self.setCentralWidget(mq)

        # Event Filter ...
        self.installEventFilter(self)
        self.editor.setFocus()
        self.cursor = QTextCursor()
        self.editor.setPlainText("hello")
        self.editor.moveCursor(self.cursor.End)
        self.editor.document().modificationChanged.connect(self.setWindowModified)

        # Brackets ExtraSelection ...
        self.left_selected_bracket = QTextEdit.ExtraSelection()
        self.right_selected_bracket = QTextEdit.ExtraSelection()

        # self.compileButton.clicked.connect(gui_logic.GUILogic.compile_handler)
        # self.compileButton.clicked.connect(self.on_changed_value)

        # self.changedValue.emit(value)

        # self.compileButton.clicked.connect(logic.compile_handler)

        # logic.main()

    # @pyqtSlot(bool)
    def on_changed_value(self, value):
        print("asdfasdfsadfasdfasdf", value)
        self.compileButton.clicked.emit(value)

    def aa(self):
        print("aasdfsadf")

    def createActions(self):
        for i in range(self.MaxRecentFiles):
            self.recentFileActs.append(
                QAction(self, visible=False, triggered=self.openRecentFile)
            )

    def openRecentFile(self):
        action = self.sender()
        if action:
            if self.maybeSave():
                self.openFileOnStart(action.data())

        ### New File

    def newFile(self):
        if self.maybeSave():
            self.editor.clear()
            self.editor.setPlainText("")
            self.filename = ""
            self.setModified(False)
            self.editor.moveCursor(self.cursor.End)

    ### open File
    def openFileOnStart(self, path=None):
        if path:
            inFile = QFile(path)
            if inFile.open(QFile.ReadWrite | QFile.Text):
                text = inFile.readAll()

                try:
                    # Python v3.
                    text = str(text, encoding="utf8")
                except TypeError:
                    # Python v2.
                    text = str(text)
                self.editor.setPlainText(text)
                self.filename = path
                self.setModified(False)
                self.fname = QFileInfo(path).fileName()
                self.setWindowTitle(self.fname + "[*]")
                self.document = self.editor.document()
                self.setCurrentFile(self.filename)

        ### open File

    def openFile(self, path=None):
        if self.maybeSave():
            if not path:
                path, _ = QFileDialog.getOpenFileName(
                    self,
                    "Open File",
                    QDir.homePath() + "/Documents/",
                    "Text Files (*.txt *.csv *.py);;All Files (*.*)",
                )

            if path:
                inFile = QFile(path)
                if inFile.open(QFile.ReadWrite | QFile.Text):
                    text = inFile.readAll()

                    try:
                        # Python v3.
                        text = str(text, encoding="utf8")
                    except TypeError:
                        # Python v2.
                        text = str(text)
                    self.editor.setPlainText(text)
                    self.filename = path
                    self.setModified(False)
                    self.fname = QFileInfo(path).fileName()
                    self.setWindowTitle(self.fname + "[*]")
                    self.document = self.editor.document()
                    self.setCurrentFile(self.filename)

    def fileSave(self):
        if self.filename != "":
            file = QFile(self.filename)
            print(self.filename)
            if not file.open(QFile.WriteOnly | QFile.Text):
                QMessageBox.warning(
                    self,
                    "Error",
                    "Cannot write file %s:\n%s." % (self.filename, file.errorString()),
                )
                return

            outstr = QTextStream(file)
            QApplication.setOverrideCursor(Qt.WaitCursor)
            outstr << self.editor.toPlainText()
            QApplication.restoreOverrideCursor()
            self.setModified(False)
            self.fname = QFileInfo(self.filename).fileName()
            self.setWindowTitle(self.fname + "[*]")
            self.setCurrentFile(self.filename)

        else:
            self.fileSaveAs()

            ### save File

    def fileSaveAs(self):
        fn, _ = QFileDialog.getSaveFileName(
            self, "Save as...", self.filename, "Python files (*.py)"
        )

        if not fn:
            print("Error saving")
            return False

        lfn = fn.lower()
        if not lfn.endswith(".py"):
            fn += ".py"

        self.filename = fn
        self.fname = os.path.splitext(str(fn))[0].split("/")[-1]
        return self.fileSave()

    def closeEvent(self, e):
        if self.maybeSave():
            e.accept()
        else:
            e.ignore()

        ### ask to save

    def maybeSave(self):
        if not self.isModified():
            return True

        if self.filename.startswith(":/"):
            return True

        ret = QMessageBox.question(
            self,
            "Message",
            "<h4><p>The document was modified.</p>\n"
            "<p>Do you want to save changes?</p></h4>",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
        )

        if ret == QMessageBox.Yes:
            if self.filename == "":
                self.fileSaveAs()
                return False
            else:
                self.fileSave()
                return True

        if ret == QMessageBox.Cancel:
            return False

        return True

    def findText(self):
        ft = self.findfield.text()
        if self.editor.find(ft):
            return
        else:
            self.editor.moveCursor(1)
            if self.editor.find(ft):
                self.editor.moveCursor(QTextCursor.Start, QTextCursor.MoveAnchor)

    def handleQuit(self):
        print("Goodbye ...")
        app.quit()

    def set_numbers_visible(self, value=True):
        self.numbers.setVisible(False)

    def match_left(self, block, character, start, found):
        map = {"{": "}", "(": ")", "[": "]"}

        while block.isValid():
            data = block.userData()
            if data is not None:
                braces = data.braces
                N = len(braces)

                for k in range(start, N):
                    if braces[k].character == character:
                        found += 1

                    if braces[k].character == map[character]:
                        if not found:
                            return braces[k].position + block.position()
                        else:
                            found -= 1

                block = block.next()
                start = 0

    def match_right(self, block, character, start, found):
        map = {"}": "{", ")": "(", "]": "["}

        while block.isValid():
            data = block.userData()

            if data is not None:
                braces = data.braces

                if start is None:
                    start = len(braces)
                for k in range(start - 1, -1, -1):
                    if braces[k].character == character:
                        found += 1
                    if braces[k].character == map[character]:
                        if found == 0:
                            return braces[k].position + block.position()
                        else:
                            found -= 1
            block = block.previous()
            start = None
        #    '''

        cursor = self.editor.textCursor()
        block = cursor.block()
        data = block.userData()
        previous, next = None, None

        if data is not None:
            position = cursor.position()
            block_position = cursor.block().position()
            braces = data.braces
            N = len(braces)

            for k in range(0, N):
                if (
                    braces[k].position == position - block_position
                    or braces[k].position == position - block_position - 1
                ):
                    previous = braces[k].position + block_position
                    if braces[k].character in ["{", "(", "["]:
                        next = self.match_left(block, braces[k].character, k + 1, 0)
                    elif braces[k].character in ["}", ")", "]"]:
                        next = self.match_right(block, braces[k].character, k, 0)
                    if next is None:
                        next = -1

        if next is not None and next > 0:
            if next == 0 and next >= 0:
                format = QTextCharFormat()

            cursor.setPosition(previous)
            cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)

            format.setBackground(QColor("white"))
            self.left_selected_bracket.format = format
            self.left_selected_bracket.cursor = cursor

            cursor.setPosition(next)
            cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)

            format.setBackground(QColor("white"))
            self.right_selected_bracket.format = format
            self.right_selected_bracket.cursor = cursor

    #            '''
    def paintEvent(self, event):
        highlighted_line = QTextEdit.ExtraSelection()
        highlighted_line.format.setBackground(lineHighlightColor)
        highlighted_line.format.setProperty(
            QTextFormat.FullWidthSelection, QVariant(True)
        )
        highlighted_line.cursor = self.editor.textCursor()
        highlighted_line.cursor.clearSelection()
        self.editor.setExtraSelections(
            [highlighted_line, self.left_selected_bracket, self.right_selected_bracket]
        )

    def document(self):
        return self.editor.document

    def isModified(self):
        return self.editor.document().isModified()

    def setModified(self, modified):
        self.editor.document().setModified(modified)

    def setLineWrapMode(self, mode):
        self.editor.setLineWrapMode(mode)

    def clear(self):
        self.editor.clear()

    def setPlainText(self, *args, **kwargs):
        self.editor.setPlainText(*args, **kwargs)

    def setDocumentTitle(self, *args, **kwargs):
        self.editor.setDocumentTitle(*args, **kwargs)

    def set_number_bar_visible(self, value):
        self.numbers.setVisible(value)

    def replaceAll(self):
        print("replacing all")
        oldtext = self.editor.document().toPlainText()
        newtext = oldtext.replace(self.findfield.text(), self.replacefield.text())
        self.editor.setPlainText(newtext)
        self.setModified(True)

    def replaceOne(self):
        print("replacing all")
        oldtext = self.editor.document().toPlainText()
        newtext = oldtext.replace(self.findfield.text(), self.replacefield.text(), 1)
        self.editor.setPlainText(newtext)
        self.setModified(True)

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        if self.curFile:
            self.setWindowTitle("%s - Recent Files" % self.strippedName(self.curFile))
        else:
            self.setWindowTitle("Recent Files")

        settings = QSettings("Andrew Shmatko", "codeeditor")
        # files = settings.value('recentFileList')

        # try:
        #     files.remove(fileName)
        # except ValueError:
        #     pass

        # files.insert(0, fileName)
        # del files[self.MaxRecentFiles]

        # settings.setValue('recentFileList', files)

        # for widget in QApplication.topLevelWidgets():
        #     if isinstance(widget, myEditor):
        #         widget.updateRecentFileActions()

    def updateRecentFileActions(self):
        mytext = ""
        settings = QSettings("Andrew Shmatko", "codeeditor")
        files = settings.value("recentFileList")
        print(files)
        try:
            numRecentFiles = min(len(files), self.MaxRecentFiles)
        except TypeError:
            numRecentFiles = 0  # self.MaxRecentFiles
            pass
        print("numRecentFiles", numRecentFiles)
        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, self.strippedName(files[i]))
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(files[i])
            self.recentFileActs[i].setVisible(True)

        for j in range(numRecentFiles, self.MaxRecentFiles):
            self.recentFileActs[j].setVisible(False)

        self.separatorAct.setVisible((numRecentFiles > 0))

    def clearRecentFileList(self, fileName):
        self.rmenu.clear()

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()


def stylesheet2(self):
    return """
QPlainTextEdit
{
background: #ECECEC;
color: #202020;
border: 1px solid #1EAE3D;
selection-background-color: #505050;
selection-color: #ACDED5;
}
QMenu
{
background: #F2F2F2;
color: #0E185F;
border: 1px solid #1EAE3D;
selection-background-color: #ACDED5;
} 
    """


# if __name__ == '__main__':
