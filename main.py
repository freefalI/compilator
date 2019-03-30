import gui.codeeditor as  codeeditor

from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout, QApplication, QFileDialog, QMessageBox, QHBoxLayout, \
                         QFrame, QTextEdit, QToolBar, QComboBox, QLabel, QAction, QLineEdit, QToolButton, QMenu, QMainWindow,QTabWidget,QTableWidget,QPushButton
from PyQt5.QtGui import QIcon, QPainter, QTextFormat, QColor, QTextCursor, QKeySequence, QClipboard, QTextCharFormat, QPalette
from PyQt5.QtCore import Qt, QVariant, QRect, QDir, QFile, QFileInfo, QTextStream, QRegExp, QSettings,QSize
import sys, os

    
app = QApplication(sys.argv)
win = codeeditor.CodeEditor()
win.setWindowIcon(QIcon.fromTheme("application-text"))
win.setWindowTitle("Plain Text Edit" + "[*]")
win.setMinimumSize(640,250)
win.showMaximized()
if len(sys.argv) > 1:
    print(sys.argv[1])
    win.openFileOnStart(sys.argv[1])
app.exec_()
