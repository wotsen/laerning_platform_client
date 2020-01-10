#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QIcon, QFont
from . login import Ui_MainWindow


class MainPage(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainPage, self).__init__()
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.setWindowTitle('platform')
        self.setWindowIcon(QIcon('resource/icon.jpg'))


_Ui = None


def UiInit():
    global _Ui
    if not _Ui:
        _Ui = MainPage()
        _Ui.show()


if "__main__" == __name__:
    app = QApplication(sys.argv)
    UiInit()
    # _Ui = MainPage()
    # _Ui.show()
    sys.exit(app.exec_())
