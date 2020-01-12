#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory, Factory


class SdkTcpProtocol(Protocol):
    """SdkTcpProtocol"""
    def __init__(self):
        pass

    def connectionMade(self):
        print("client connect")

    def dataReceived(self, data):
        self.transport.write(data)

    def connectionLost(self, reason=None):
        pass


class SdkTcpFactory(Factory):
    """SdkTcpFactory"""

    protocol = SdkTcpProtocol

    def __init__(self):
        pass


def sdk_tcp_connet(port, host="0.0.0.0"):
    sdk_connect = SdkTcpFactory()
    reactor.listenTCP(port, sdk_connect)


if __name__ == "__main__":
    sdk_tcp_connet(8000)
    reactor.run()
