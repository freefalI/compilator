import gui.codeeditor as codeeditor
import gui.gui_logic as gui_logic
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
    QPushButton,
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
)
import sys, os


class Compiler:
    def __init__(self):
        # self.__config = None
        self.app = QApplication(sys.argv)
        self.win = codeeditor.CodeEditor()
        self.win.setWindowIcon(QIcon.fromTheme("application-text"))
        self.win.setWindowTitle("Plain Text Edit" + "[*]")
        self.win.setMinimumSize(640, 250)
        self.win.showMaximized()

        self.logic = gui_logic.GUILogic()
        self.logic.make_connection(self.win)

    def run(self):
        self.win.openFileOnStart("compiler/source.txt")
        if len(sys.argv) > 1:
            print(sys.argv[1])
            self.win.openFileOnStart(sys.argv[1])
        self.app.exec_()


compiler = Compiler()
compiler.run()

