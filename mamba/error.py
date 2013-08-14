# -*- coding: utf-8 -*-


class Error(object):

    def __init__(self, exception, traceback):
        self.exception = exception
        self.traceback = traceback
