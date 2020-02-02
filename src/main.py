#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
# import platform

# if platform.system() == "Windows":
#     # 解决windows任务栏的图标问题
#     import ctypes
#
#     ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("my-app-id")

import src_packages_path

from PyQt5.QtWidgets import QApplication
import qt5reactor

example_app = QApplication(sys.argv)

qt5reactor.install()

from twisted.python import log
from twisted.internet import reactor
from twisted.internet import defer

# sys.path.append("ui")
# from mainpage import UiInit

from ui.login_page import LoginPage
from sdk_net import sdk_tcp_connect


def mainTaskLoop():
    def loop(ret):
        d = defer.Deferred()
        d.addCallback(loop)
        reactor.callLater(1, d.callback, "mianloop")

    d = defer.Deferred()
    d.addCallback(loop)
    reactor.callLater(1, d.callback, "mianloop")


if "__main__" == __name__:
    # 开启日志
    log.startLogging(sys.stdout)
    print("platform start.........................")

    # 初始化UI
    # ui = UiInit()
    login = LoginPage()
    login.show()

    sdk_tcp_connect()

    # 主任务(空转)
    reactor.callWhenRunning(mainTaskLoop)

    # loop循环
    reactor.run()
    exit(1)
