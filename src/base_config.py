#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/31 16:07
# @Author  : ywl
# @Email   : astralrovers@outlook.com
# @File    : base_config.py

import json
import sys

sys.path.append("sdk_network/sdk_protocol")

import in_sdk_header_pb2 as SdkHeader

_base_config = None
# 正式使用路径为: runtime/config/config.json
with open("runtime/config/config.json", "r+", encoding="utf8") as f:
    try:
        _base_config = json.load(f)
    except Exception as e:
        print(e)


def get_ip_version():
    """
    获取ip版本
    @return:
    """
    if _base_config["network"]["sdk-net"]["ip-version"] == "ipv4":
        return SdkHeader.IpVersion.IPV4
    else:
        return SdkHeader.IpVersion.IPV6


def get_local_ip():
    """
    获取本地ip
    @return:
    """
    return _base_config["network"]["sdk-net"]["ip"]


def get_local_tcp_port():
    """
    获取本地tcp判断口
    @return:
    """
    return _base_config["network"]["sdk-net"]["tcp-port"]


def get_local_udp_port():
    """
    获取本地udp端口
    @return:
    """
    return _base_config["network"]["sdk-net"]["udp-port"]


def get_sdk_srv_ip():
    """
    获取sdk服务器ip
    @return:
    """
    return _base_config["network"]["sdk-net"]["srv-ip"]


def get_sdk_srv_tcp_port():
    """
    获取sdk服务器tcp端口
    @return:
    """
    return _base_config["network"]["sdk-net"]["srv-tcp-port"]


def get_sdk_srv_udp_port():
    """
    获取sdk服务器udp端口
    @return:
    """
    return _base_config["network"]["sdk-net"]["srv-udp-port"]


def get_sdk_trans_proto():
    """
    获取sdk传输协议
    @return:
    """
    if _base_config["network"]["sdk-net"]["cur-trans-proto"] == "tcp":
        return SdkHeader.TransProto.TCP
    else:
        return SdkHeader.TransProto.UDP


def get_local_port():
    """
    获取本地端口
    @return:
    """
    if get_sdk_trans_proto() == SdkHeader.TransProto.TCP:
        return get_local_tcp_port()
    else:
        return get_local_udp_port()


def get_sdk_srv_port():
    """
    获取sdk服务器端口
    @return:
    """
    if get_sdk_trans_proto() == SdkHeader.TransProto.TCP:
        return get_sdk_srv_tcp_port()
    else:
        return get_sdk_srv_udp_port()
