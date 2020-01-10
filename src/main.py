#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
import qt5reactor

example_app = QApplication(sys.argv)

qt5reactor.install()

from twisted.python import log
from twisted.internet import reactor
from twisted.internet import defer

from ui.mainpage import UiInit


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
    UiInit()

    # 主任务(空转)
    reactor.callWhenRunning(mainTaskLoop)

    # loop循环
    reactor.run()
    exit(1)
