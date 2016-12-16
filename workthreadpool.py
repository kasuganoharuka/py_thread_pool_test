#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Queue import Queue
from threading import Thread
from msgtask import MsgTask
import heapq


class Work:
    def __init__(self, exec_func, args):
        self.exec_func = exec_func
        self.args = args

    def __eq__(self, other):
        return self.args[0] == other.args[0]

    def __hash__(self):
        return hash(self.args[0])

    def run(self):
        self.exec_func(*self.args)


class WorkThread(Thread):
    def __init__(self, msg_queue):
        super(WorkThread, self).__init__()
        self.msg_queue = msg_queue
        self.work_queue = Queue()
        self.start()

    def add_work(self, work):
        self.work_queue.put(work)

    def work_counts(self):
        return self.work_queue.qsize()

    def run(self):
        while True:
            try:
                work = self.work_queue.get()
            except Exception:
                import traceback
                traceback.print_exc()
            else:
                result = work.run()
                if result:
                    msg_task = MsgTask(**result)
                    self.msg_queue.put(msg_task)


class WorkThreadManager:
    def __init__(self, max_size, msg_queue):
        self.thread_pool = []
        self.max_size = max_size
        self.current_thread = 0
        for _ in xrange(0, self.max_size):
            self.thread_pool.append(WorkThread(msg_queue))

    def get_work_thread(self):
        return min(filter(lambda x: x.isAlive(), self.thread_pool), key=lambda x: x.work_counts)

    def add_work(self, work):
        thread = self.get_work_thread()
        thread.add_work(work)

    def wait_all_complete(self):
        for thread in self.thread_pool:
            if thread.isAlive():
                thread.join()

