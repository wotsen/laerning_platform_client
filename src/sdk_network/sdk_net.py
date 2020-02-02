#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if __name__ == "__main__":
    sys.path.append("../")
else:
    pass

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory

from sdk_protocol_do import sdk_decode
from base_config import *

_sdk_connect = None


def sdk_data_send(data):
    """
    发送sdk数据
    @param data:byte流数据
    """
    if _sdk_connect:
        _sdk_connect.sdk_tcp.data_send(data)


class SdkTcpProtocol(Protocol):
    """SdkTcpProtocol"""

    def __init__(self):
        pass

    def connectionMade(self):
        print("connect sdk server")

    def dataReceived(self, data):
        """
        数据接收
        @param data:byte流数据
        """
        self.factory.data_decode(data)

    def data_send(self, data):
        """
        数据发送
        @param data:byte流数据
        """
        print("send len : ", len(data))
        self.transport.write(data)

    def connectionLost(self, reason=None):
        print("disconnect sdk server")


class SdkTcpFactory(ClientFactory):
    """SdkTcpFactory"""

    protocol = SdkTcpProtocol

    def __init__(self, data_decode):
        self.sdk_tcp = None
        self.data_decode = data_decode

    def startedConnecting(self, connector):
        print('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)

    def buildProtocol(self, addr):
        p = self.protocol()
        self.sdk_tcp = p  # 便于外部能方便使用send方法
        p.factory = self
        return p


# TODO:1.手动断开连接
# TODO:2.手动重连
# TODO:3.控制连接时机


def sdk_tcp_connect():
    """
    创建sdk tcp连接
    """
    global _sdk_connect
    _sdk_connect = SdkTcpFactory(sdk_decode)
    reactor.connectTCP(get_sdk_srv_ip(),
                       get_sdk_srv_tcp_port(),
                       _sdk_connect,
                       bindAddress=(get_local_ip(), get_local_tcp_port()))


if __name__ == "__main__":
    sdk_tcp_connect()
    reactor.run()
