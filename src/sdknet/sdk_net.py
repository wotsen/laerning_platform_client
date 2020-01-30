#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory


class SdkTcpProtocol(Protocol):
    """SdkTcpProtocol"""
    def __init__(self):
        pass

    def connectionMade(self):
        print("connect");
        self.transport.write(b'hello server')

    def dataReceived(self, data):
        #  self.factory.data_proc(data)
        print(data)
        self.transport.write(b'hello server')

    def data_send(self, data):
        """data_send

        :param data:
        """
        # FIXME:byte类型检查
        self.transport.write(data)

    def connectionLost(self, reason=None):
        pass


class SdkTcpFactory(ClientFactory):
    """SdkTcpFactory"""

    protocol = SdkTcpProtocol

    def __init__(self, data_proc):
        self.data_proc = data_proc

    def startedConnecting(self, connector):
        print('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)


def sdk_data_proc(data):
    """sdk_data_proc

    :param data:
    """
    print(data)


def sdk_tcp_connet(port, host="0.0.0.0"):
    sdk_connect = SdkTcpFactory(sdk_data_proc)
    reactor.connectTCP(host, port, sdk_connect)


if __name__ == "__main__":
    sdk_tcp_connet(9001)
    reactor.run()
