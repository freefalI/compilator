# !/usr/bin/python3
# -- coding: utf-8 --

from PyQt5.QtWidgets import QWidget,QVBoxLayout
from PyQt5.QtGui import QPainter,QColor
from PyQt5.QtCore import Qt, QRect


lineBarColor = QColor("#c6ffb3")  



class NumberBar(QWidget):
    def __init__(self, parent = None):
        super(NumberBar, self).__init__(parent)
        self.editor = parent
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_on_scroll)
        self.update_width('1')

    def update_on_scroll(self, rect, scroll):
        if self.isVisible():
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update()

    def update_width(self, string):
        width = self.fontMetrics().width(str(string)) + 10
        if self.width() != width:
            self.setFixedWidth(width)

    def paintEvent(self, event):
        if self.isVisible():
            block = self.editor.firstVisibleBlock()
            height = self.fontMetrics().height()
            number = block.blockNumber()
            painter = QPainter(self)
            painter.fillRect(event.rect(), lineBarColor)
            painter.drawRect(0, 0, event.rect().width() - 1, event.rect().height() - 1)
            font = painter.font()

            current_block = self.editor.textCursor().block().blockNumber() + 1

            condition = True
            while block.isValid() and condition:
                block_geometry = self.editor.blockBoundingGeometry(block)
                offset = self.editor.contentOffset()
                block_top = block_geometry.translated(offset).top()
                number += 1

                rect = QRect(0, block_top, self.width() - 5, height)

                if number == current_block:
                    font.setBold(True)
                else:
                    font.setBold(False)

                painter.setFont(font)
                painter.drawText(rect, Qt.AlignRight, '%i'%number)

                if block_top > event.rect().bottom():
                    condition = False

                block = block.next()

            painter.end()