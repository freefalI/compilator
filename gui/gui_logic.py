# !/usr/bin/python3
# -- coding: utf-8 --



from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout, QApplication, QFileDialog, QMessageBox, QHBoxLayout, \
                         QFrame, QTextEdit, QToolBar, QComboBox, QLabel, QAction, QLineEdit, QToolButton, QMenu, QMainWindow,QTabWidget,QTableWidget,QPushButton
from PyQt5.QtGui import QIcon, QPainter, QTextFormat, QColor, QTextCursor, QKeySequence, QClipboard, QTextCharFormat, QPalette
from PyQt5.QtCore import Qt, QVariant, QRect, QDir, QFile, QFileInfo, QTextStream, QRegExp, QSettings,QSize


class GUILogic:
    def __init__(self,app):
        self.app = app
        self.main()

    def main(self):
        app = self.app

        #app.compileButton.clicked.connect(app.textEditStatusBar.clear)
        




