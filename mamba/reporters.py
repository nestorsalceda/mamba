# -*- coding: utf-8 -*-

import datetime


class Reporter(object):

    def __init__(self, *formatters):
        self.listeners = formatters
        self.spec_count = 0
        self.failed_count = 0
        self.pending_count = 0
        self.begin = None
        self.duration = datetime.timedelta(0)

    def start(self):
        self.begin = datetime.datetime.utcnow()

    def spec_started(self, spec):
        self.spec_count += 1
        self.notify('spec_started', spec)

    def spec_passed(self, spec):
        self.notify('spec_passed', spec)

    def spec_failed(self, spec):
        self.failed_count += 1
        self.notify('spec_failed', spec)

    def spec_pending(self, spec):
        self.pending_count += 1
        self.notify('spec_pending', spec)

    def spec_group_started(self, spec_group):
        self.notify('spec_group_started', spec_group)

    def spec_group_finished(self, spec_group):
        self.notify('spec_group_finished', spec_group)

    def finish(self):
        self.stop()
        self.notify('summary', self.duration, self.spec_count, self.failed_count, self.pending_count)

    def stop(self):
        self.duration = datetime.datetime.utcnow() - self.begin

    def notify(self, event, *args):
        for listener in self.listeners:
            getattr(listener, event)(*args)
