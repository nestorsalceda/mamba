# -*- coding: utf-8 -*-

from functools import partial


class _Hook(object):
    def __init__(self, where):
        self.where = where

    def __getattr__(self, key):
        return partial(self._add_hook_info, key)

    def _add_hook_info(self, when, fn):
        fn.hook = {'where': self.where, 'when': when}
        return fn


before = _Hook('before')
after = _Hook('after')
