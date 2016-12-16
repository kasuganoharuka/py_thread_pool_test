#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Queue import Queue
from workthreadpool import WorkThreadManager
from msgtask import MessageMap


class MainLoop:
    def __init__(self):
        self.msg_map = MessageMap()
        self.msg_queue = Queue()
        self.work_thread_mgr = WorkThreadManager(500, self.msg_queue)

    def run(self, exec_func, *args, **kwargs):
        exec_func(*args, **kwargs)
        # while True:
        #     try:
        #         msg_task = self.msg_queue.get()
        #     except Exception:
        #         pass
        #     else:
        #         if msg_task:
        #             self.msg_map.handler_msg(**msg_task)
