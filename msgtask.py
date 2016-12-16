#!/usr/bin/env python
# -*- coding: utf-8 -*-


class MsgTask:
    def __init__(self, msg, args):
        self.msg = msg
        self.args = args

class MessageType(object):
    ConnectionError = 'ConnectionError'
    ConnectionSuccess = 'ConnectionSuccess'
    NotFound = 'NotFound'


class MessageMap:
    def __init__(self):
        self.mapping = {}

    def register_msg_handler(self, msg):
        def decorator(fn):
            self.mapping[msg] = fn
            return fn
        return decorator

    def handler_msg(self, msg, args):
        handler = self.mapping.get(msg)
        if handler is not None:
            handler(*args)