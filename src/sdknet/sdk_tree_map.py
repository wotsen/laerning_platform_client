#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/31 12:26
# @Author  : ywl
# @Email   : astralrovers@outlook.com
# @File    : sdk_tree_map.py

import sys

sys.path.append("sdk_protocol")

import in_sdk_body_pb2 as SdkBody
import in_sdk_body_user_pb2 as SdkUser
from collections import namedtuple
import re

# 格式说明：
# url：路径必须为字符串
# method:方法，参考SdkBody.OperationType
# encode:编码接口，参考_index_encode
# decode:解码接口，参考_index_decode
# next:下级节点，类型为数组，数组内是SdkTreeMap类型
SdkTreeMap = namedtuple("SdkTreeMap", ["url", "method", "encode", "decode", "next"])


def _index_encode(body, *args, **kwargs):
    """
    编码模板接口，第一个参数至少是body，也是输出参数
    @param body:
    """
    print("........encode : ", body)


def _index_decode(msg):
    """
    解码模板接口
    @param msg:完整的sdk协议数据
    """
    print("........decode : ", msg)

# #####################################测试代码##################################################


def _sdk_test_pack_body(body):
    user_session = body.user_session
    user_session.user_type = SdkUser.UserSessionMsg.U_LOGIN
    user_session.user.user_name = "admin"
    user_session.user.user_pass = "admin"
    user_session.user.permission = SdkUser.U_PERMISSION_ADMIN
    user_session.user.email = "astralrovers@outlook.com"
    user_session.user.phone = "12345678901"
    user_session.token = "accc"
    user_session.alive_time = 80


def _sdk_test_unpack(msg):
    header = msg.header
    body = msg.body
    footer = msg.footer
    print("#####################header######################")
    print("header.msg_magic : ", header.msg_magic)
    print("header.version : ", header.version)
    print("header.pack_id : ", header.pack_id)

    _time = header.time
    print("_time.in_time : ", _time.in_time)
    print("_time.out_time : ", _time.out_time)

    print("header.data_dir : ", header.data_dir)

    host = header.host
    print("host.ip_version : ", host.ip_version)
    print("host.port : ", host.port)
    print("host.ip : ", host.ip)

    dest = header.dest
    print("dest.ip_version : ", dest.ip_version)
    print("dest.port : ", dest.port)
    print("dest.ip : ", dest.ip)
    print("header.trans_proto : ", header.trans_proto)

    print("#####################body######################")

    user_session = body.user_session
    print("user_session.token : ", user_session.token)

    print("#####################footer######################")

    print("footer.res : ", footer.res)
    print("footer.result.sdk_result.status_code : ", footer.result.sdk_result.status_code)
    print("footer.result.sdk_result.code : ", footer.result.sdk_result.code)
    print("footer.result.content_result.status_code : ", footer.result.content_result.status_code)
    print("footer.result.content_result.code : ", footer.result.content_result.code)

    print("#####################over######################")

# #####################################测试代码over##################################################


_sdk_tree_map = [
    SdkTreeMap("/index", SdkBody.OperationType.GET, _sdk_test_pack_body, _sdk_test_unpack, []),
    SdkTreeMap("/test", SdkBody.OperationType.GET, _index_encode, _index_decode, []),
]


def sdk_node_insert_into(father, url, method, encode=None, decode=None, next_tree=None):
    """
    添加一个节点到已有的树的下级树列表中
    @param father:父节点
    @param url:
    @param method:
    @param encode:
    @param decode:
    @param next_tree:下一树
    @return:
    """
    if not father \
            or not url \
            or not isinstance(str, url) \
            or re.match(r'[^/a-zA-Z_\-0-9]', url) \
            or not method:
        return

    # 接口检查，只是简单检查
    if encode:
        if not callable(encode):
            return

    if decode:
        if not callable(decode):
            return

    if not father.next:
        father.next = list()

    father.next.append(SdkTreeMap(url, method, encode, decode, next_tree if next_tree else []))


def sdk_node_append(tree):
    """
    追加树到根
    @param tree:
    @return:
    """
    if not isinstance(SdkTreeMap, tree):
        print("tree type error : ", type(tree))
        return

    _sdk_tree_map.append(tree)


def is_method_valid(method):
    """
    校验方法有合法性
    @param method:
    @return:
    """
    if method == SdkBody.OperationType.GET \
            or method == SdkBody.OperationType.POST \
            or method == SdkBody.OperationType.PUT \
            or method == SdkBody.OperationType.DELETE:
        return True
    return False


def is_method_support(operation, method):
    """
    校验方法是否支持
    @param operation:
    @param method:
    @return:
    """
    return operation | method


def _sdk_find_codec_fn(fn_name, tree, url, method):
    """
    查找编解码方法
    @param fn_name:编解码名称,encode,decode
    @param tree:树
    @param url:
    @param method:
    @return:编解码方法
    """
    if not tree or not len(tree) or not url:
        return None

    for item in tree:
        if not item.url \
                or not is_method_support(method, item.method):
            return None

        if re.match(r'[^/a-zA-Z_\-0-9]', url):
            return None

        url_pat = "%s(.*)" % item.url
        ret = re.match(url_pat, url)

        # 未匹配
        if not ret:
            continue

        # 完全匹配
        if not ret.group(1):
            return getattr(item, fn_name)

        # 向下级查找
        if item.next:
            fun = _sdk_find_codec_fn(fn_name, item.next, ret.group(1), method)

            # 找到了直接返回
            if fun:
                return fun
            continue

    return None


def sdk_find_encode_fn(url, method):
    """
    查找编码方法
    @param url:
    @param method:
    @return:
    """
    return _sdk_find_codec_fn("encode", _sdk_tree_map, url, method)


def sdk_find_decode_fn(url, method):
    """
    查找解码方法
    @param url:
    @param method:
    @return:
    """
    return _sdk_find_codec_fn("decode", _sdk_tree_map, url, method)


if __name__ == "__main__":
    fn = sdk_find_encode_fn("/test", SdkBody.OperationType.GET)
    if fn:
        fn("..")
    fn = sdk_find_decode_fn("/test", SdkBody.OperationType.GET)
    if fn:
        fn("..")

