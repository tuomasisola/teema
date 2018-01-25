#!/usr/bin/env python3

import sys, os
from PyQt5 import QtWidgets, QtGui, QtCore

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

STYLESHEET = ('QPlainTextEdit, QMessageBox {background: #f7f7f7; color: #212121;'
            'selection-color: #f7f7f7; selection-background-color: #212121 }')
PATH_TO_DESKTOP = os.path.expanduser("~/Desktop/teema.txt")

FONTSIZE = 26   #points
LINEWIDTH = 7   #inches

class TextWindow(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super(TextWindow, self).__init__()
        self.setWindowTitle('Teema')
        self.fontsize = FONTSIZE
        self.initFont()
        self.initGeometry()
        self.initMargins()
        self.show()
        self.file = Load(self)

    def initGeometry(self):
        self.showFullScreen()
        self.setCenterOnScroll(True)
        self.setPlaceholderText('CMD + S to save. ESC to exit. Just Write')
        self.setCursorWidth(3)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def initMargins(self):
        screen = app.primaryScreen()
        dpi = screen.physicalDotsPerInchX()
        width = screen.size().width()
        line = dpi * LINEWIDTH
        sidemargin = (width - line) / 2
        self.setViewportMargins(sidemargin, 30, sidemargin, 30)

    def initFont(self):
        self.setFont(QtGui.QFont("Roboto Mono", FONTSIZE))

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.matches(QtGui.QKeySequence.Cancel):    # Esc
            ExitDialog(self)
        elif event.matches(QtGui.QKeySequence.Save):    # Ctrl-S
            self.file.save()


class ExitDialog(QtWidgets.QMessageBox):
    def __init__(self, window):
        super(ExitDialog, self).__init__()
        self.window = window
        self.setText("Press E to exit without saving.")
        self.setInformativeText('Press Esc to Cancel')
        self.setFont(QtGui.QFont('Sans Serif', 18))
        self.exec_()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == 0x45: # 'e'-key
            self.window.close()
            self.close()


class Load:
    def __init__(self, TextEdit):
        self.TextEdit = TextEdit
        self.path = PATH_TO_DESKTOP
        self.load()

    def save(self):
        teksti = self.TextEdit.toPlainText()
        with open(self.path, mode='w') as f:
            f.write(teksti)

    def load(self):
        try:
            with open(self.path) as input_file:
                lines = input_file.readlines()
                text = ''.join(lines)
                self.TextEdit.setPlainText(text)
        except OSError:
            print("Could not open {}".format(self.path), file=sys.stderr)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    text = TextWindow()
    sys.exit(app.exec_())
