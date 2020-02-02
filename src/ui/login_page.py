#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/2 10:30
# @Author  : ywl
# @Email   : astralrovers@outlook.com
# @File    : login_page.py

from PyQt5.Qt import QWidget, QLineEdit, QPushButton
from op_login import OpUserLogin


class UserName(QLineEdit):
    pass


class UserPassword(QLineEdit):
    pass


class UserLogin(QPushButton):
    pass


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        self.user_name = None
        self.password = None
        self.login = None

        self.setup_ui()
        self.setup_slot()

    def setup_ui(self):
        self.setWindowTitle("登录")
        self.resize(640, 480)
        self.setFixedSize(640, 480)

        self.user_name = UserName(self)
        self.user_name.move(270, 20)
        self.password = UserPassword(self)
        self.password.move(270, 50)
        self.login = UserLogin(self)
        self.login.setText("安全登录")
        self.login.move(270, 80)

    def setup_slot(self):
        self.op_login = OpUserLogin(self.login_result())
        self.login.clicked.connect(self.login_slot())

    def login_result(self):
        def _login_ret(token):
            print(token)

        return _login_ret

    def login_slot(self):
        def _login_slot():
            OpUserLogin.user_login_trigger(self.user_name.text(), self.password.text())

        return _login_slot


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    test = LoginPage()
    test.show()
    sys.exit(app.exec_())
