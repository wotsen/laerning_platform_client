#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/30 19:12
# @Author  : ywl
# @Email   : astralrovers@outlook.com
# @File    : sdk_protocol_do.py

import sys

sys.path.append("sdk_protocol")
sys.path.append("../")

import time

import in_sdk_pb2 as Sdk
import in_sdk_header_pb2 as SdkHeader
import in_sdk_body_pb2 as SdkBody
from sdk_tree_map import sdk_find_encode_fn, sdk_find_decode_fn

from base_config import *

_SDK_PACK_ID = 0


def sdk_header_encode(header):
    # header
    header.msg_magic = SdkHeader.SdkMagic.SDK_MAGIC
    header.version = SdkHeader.SdkVersion.SDK_CUR_VERSION

    # 包序号
    global _SDK_PACK_ID
    _SDK_PACK_ID += 1
    header.pack_id = _SDK_PACK_ID

    # 发送时间
    header.time.in_time = int(time.time())
    # 数据方向
    header.data_dir = SdkHeader.DataFlow.DATA_IN

    # 地址
    host = header.host
    host.ip_version = get_ip_version()
    host.port = get_local_port()
    host.ip = get_local_ip()

    dest = header.dest
    dest.ip_version = get_ip_version()
    dest.port = get_sdk_srv_port()
    dest.ip = get_sdk_srv_ip()

    # 传输协议
    header.trans_proto = get_sdk_trans_proto()


def sdk_header_decode_check(header):
    if header.msg_magic != SdkHeader.SdkMagic.SDK_MAGIC \
            or header.version != SdkHeader.SdkVersion.SDK_CUR_VERSION \
            or header.pack_id != _SDK_PACK_ID \
            or header.time.out_time > int(time.time()) \
            or header.data_dir != SdkHeader.DataFlow.DATA_OUT \
            or header.trans_proto != get_sdk_trans_proto() \
            or header.host.ip_version != get_ip_version() \
            or header.host.port != get_sdk_srv_port() \
            or header.host.ip != get_sdk_srv_ip() \
            or header.dest.ip_version != get_ip_version() \
            or header.dest.port != get_local_port() \
            or header.dest.ip != get_local_ip():
        return False

    return True


def sdk_encode(url, method, *args, **kwargs):
    msg = Sdk.Sdk()

    # 打包包头
    sdk_header_encode(msg.header)

    # 查找编码接口
    pack_content = sdk_find_encode_fn(url, method)

    # 使用回调接口打包主体部分
    if not pack_content:
        return None

    # 填写路劲与方法
    msg.body.url = url
    msg.body.method = method

    # 业务数据内容封装
    pack_content(msg.body, *args, *kwargs)

    return msg.SerializeToString()


def sdk_decode(data):
    try:
        msg = Sdk.Sdk()
        msg.ParseFromString(data)
    except Exception as e:
        print(e)
        return

    if not sdk_header_decode_check(msg.header):
        print("header check fail")
        return

    # 查找解码接口
    unpack_content = sdk_find_decode_fn(msg.body.url, msg.body.method)
    if not unpack_content:
        print("not find decode function")
        return

    # 业务内容返回处理
    unpack_content(msg)


# #############################以下仅测试#####################################


def _test_encode():
    return sdk_encode("/index", SdkBody.OperationType.GET)


def _test_decode(data):
    try:
        msg = Sdk.Sdk()
        msg.ParseFromString(data)
    except Exception as e:
        print(e)
        return

    # 查找解码接口
    unpack_content = sdk_find_decode_fn(msg.body.url, msg.body.method)
    if not unpack_content:
        print("not find decode function")
        return

    # 业务内容返回处理
    unpack_content(msg)


if __name__ == "__main__":
    _test_decode(_test_encode())
