# -*- coding: utf-8 -*-

import datetime


class Reporter(object):

    def __init__(self, *formatters):
        self.listeners = formatters

    @property
    def failed_count(self):
        return len(self.failed_examples)

    def start(self):
        self.begin = datetime.datetime.utcnow()
        self.duration = datetime.timedelta(0)
        self.example_count = 0
        self.pending_count = 0
        self.failed_examples = []

    def example_started(self, example):
        self.example_count += 1
        self.notify('example_started', example)

    def example_passed(self, example):
        self.notify('example_passed', example)

    def example_failed(self, example):
        self.failed_examples.append(example)
        self.notify('example_failed', example)

    def example_pending(self, example):
        self.pending_count += 1
        self.notify('example_pending', example)

    def example_group_started(self, example_group):
        self.notify('example_group_started', example_group)

    def example_group_finished(self, example_group):
        self.notify('example_group_finished', example_group)

    def example_group_pending(self, example_group):
        self.notify('example_group_pending', example_group)

    def finish(self):
        self.stop()
        self.notify('summary', self.duration, self.example_count, self.failed_count, self.pending_count)
        self.notify('failures', self.failed_examples)

    def stop(self):
        self.duration = datetime.datetime.utcnow() - self.begin

    def notify(self, event, *args):
        for listener in self.listeners:
            getattr(listener, event)(*args)
