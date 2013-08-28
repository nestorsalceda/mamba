# -*- coding: utf-8 -*-

import functools

from mamba import settings, formatters, reporter, runner


def _memoize_instance(fn):
    @functools.wraps(fn)
    def wrapped(self):
        target = fn.__name__.split('create_')[-1]
        if target not in self._instances:
            self._instances[target] = fn(self)

        return self._instances[target]

    return wrapped


class ApplicationFactory(object):

    def __init__(self, arguments):
        self._instances = {}
        self.arguments = arguments

    @_memoize_instance
    def create_settings(self):
        settings_ = settings.Settings()
        settings_.slow_test_threshold = self.arguments.slow

        return settings_

    @_memoize_instance
    def create_formatter(self):
        return formatters.DocumentationFormatter(self.create_settings())

    @_memoize_instance
    def create_reporter(self):
        return reporter.Reporter(self.create_formatter())

    @_memoize_instance
    def create_runner(self):
        return runner.Runner(self.create_reporter())

