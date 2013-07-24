# -*- coding: utf-8 -*-


class Reporter(object):

    def __init__(self, *formatters):
        self.listeners = formatters
        self.spec_count = 0
        self.failed_count = 0
        self.pending_count = 0

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
        self.notify('summary', self.spec_count, self.failed_count, self.pending_count)

    def notify(self, event, *args):
        for listener in self.listeners:
            getattr(listener, event)(*args)
