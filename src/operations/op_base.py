#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/2 18:07
# @Author  : ywl
# @Email   : astralrovers@outlook.com
# @File    : op_base.py.py

import in_sdk_body_pb2 as SdkBody
from sdk_tree_map import SdkTreeMap, sdk_append_node_to_root


class OpBase:
    # 当前相对路径
    _URL = "/"
    # 绝对路径
    _ABS_URL = _URL
    # 方法
    _METHOD = SdkBody.OperationType.GET | SdkBody.OperationType.PUT | SdkBody.OperationType.POST | SdkBody.OperationType.DELETE
    # 当前树节点
    _SDK_TREE = SdkTreeMap(_URL, _METHOD, None, None, [])
    # 添加到根节点
    sdk_append_node_to_root(_SDK_TREE)

    def __init__(self):
        pass

    @classmethod
    def append_tree(cls, url, method, encode, decode, next_tree):
        cls._SDK_TREE.next.append(SdkTreeMap(url, method, encode, decode, next_tree))
