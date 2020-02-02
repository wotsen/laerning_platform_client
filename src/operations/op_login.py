#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/2 13:19
# @Author  : ywl
# @Email   : astralrovers@outlook.com
# @File    : op_login.py.py

from sdk_net import sdk_data_send
from sdk_protocol_do import sdk_encode
import in_sdk_body_pb2 as SdkBody
import in_sdk_body_user_pb2 as SdkUser
from sdk_tree_map import (SdkTreeMap, add_url_pre,
                          append_node_to_father_next, sdk_create_node_to_next,
                          add_url_pre)
from op_base import OpBase


class OpUserLogin(OpBase):
    _URL = "user_manage/"
    _ABS_URL = add_url_pre(OpBase._ABS_URL, _URL)
    _METHOD = SdkBody.OperationType.GET | SdkBody.OperationType.PUT \
              | SdkBody.OperationType.POST | SdkBody.OperationType.DELETE
    _SDK_TREE = SdkTreeMap(_URL, _METHOD, None, None, [])
    # 添加到基类的下级节点列表
    append_node_to_father_next(OpBase._SDK_TREE, _SDK_TREE)

    def __init__(self, login_result, register_result=None):
        super().__init__()
        self.login_result = login_result

        # 创建登录节点
        OpUserLogin.create_login_node("index", SdkBody.OperationType.GET,
                                      OpUserLogin.login_encode, lambda msg: self.login_decode(msg))

        OpUserLogin.create_register_node("logout", SdkBody.OperationType.PUT,
                                         OpUserLogin.logout_encode, lambda msg: self.logout_decode(msg))

        OpUserLogin.create_logout_node("register", SdkBody.OperationType.POST,
                                       OpUserLogin.register_encode, lambda msg: self.register_decode(msg))

        OpUserLogin.create_verify_node("verify", SdkBody.OperationType.GET,
                                       OpUserLogin.verify_encode, lambda msg: self.verify_decode(msg))

    @classmethod
    def create_login_node(cls, url, method, encode=None, decode=None, next_tree=None):
        def user_login_trigger(username, password):
            # [NOTE]:必须传入绝对路径
            sdk_data_send(sdk_encode(add_url_pre(OpUserLogin._ABS_URL, url), method, username, password))

        # ui触发
        cls.user_login_trigger = user_login_trigger
        # 添加到当前类节点的下级节点列表
        # 添加方式相对灵活，可以添加到当前类的下级列表中，也可以添加到其他类的下级列表中，甚至可以直接添加到一级节点列表中
        # 只要保证路径、编码、解码接口能找到
        sdk_create_node_to_next(cls._SDK_TREE, url, method, encode, decode, next_tree)

    @classmethod
    def create_register_node(cls, url, method, encode=None, decode=None, next_tree=None):
        def user_register_trigger(username, password, email, phone, permission):
            sdk_data_send(sdk_encode(add_url_pre(OpUserLogin._ABS_URL, url), method,
                                     username, password, email, phone, permission))

        cls.user_register_trigger = user_register_trigger
        sdk_create_node_to_next(cls._SDK_TREE, url, method, encode, decode, next_tree)

    @classmethod
    def create_logout_node(cls, url, method, encode=None, decode=None, next_tree=None):
        def user_logout_trigger(username):
            sdk_data_send(sdk_encode(add_url_pre(OpUserLogin._ABS_URL, url), method, username))

        cls.user_logout_trigger = user_logout_trigger
        sdk_create_node_to_next(cls._SDK_TREE, url, method, encode, decode, next_tree)

    @classmethod
    def create_verify_node(cls, url, method, encode=None, decode=None, next_tree=None):
        def user_verify_trigger(username):
            sdk_data_send(sdk_encode(add_url_pre(OpUserLogin._ABS_URL, url), method, username))

        cls.user_verify_trigger = user_verify_trigger
        sdk_create_node_to_next(cls._SDK_TREE, url, method, encode, decode, next_tree)

    @classmethod
    def login_encode(cls, body, username, password):
        user_session = body.user_session
        user_session.user_type = SdkUser.UserSessionMsg.U_LOGIN
        user_session.user.user_name = username
        user_session.user.user_pass = password
        user_session.alive_time = 80

    def login_decode(self, msg):
        # 消息返回回调处理
        self.login_result(msg.body.user_session.token)

    @classmethod
    def register_encode(cls, body, username, password, email, phone, permission):
        user_session = body.user_session
        user_session.user_type = SdkUser.UserSessionMsg.U_REGISTER
        user_session.user.user_name = username
        user_session.user.user_pass = password
        user_session.user.permission = permission  # TODO:转换到协议权限
        user_session.user.email = email
        user_session.user.phone = phone
        user_session.alive_time = 80

    def register_decode(self, msg):
        pass

    @classmethod
    def logout_encode(cls, body, username):
        pass

    def logout_decode(self, msg):
        pass

    @classmethod
    def verify_encode(cls, body, username):
        pass

    def verify_decode(self, msg):
        pass
