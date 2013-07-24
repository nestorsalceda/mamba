# -*- coding: utf-8 -*-


class Reporter(object):

    def __init__(self, *formatters):
        self.listeners = formatters

    def spec_started(self, spec):
        self.notify('spec_started', spec)

    def spec_passed(self, spec):
        self.notify('spec_passed', spec)

    def spec_failed(self, spec):
        self.notify('spec_failed', spec)

    def spec_pending(self, spec):
        self.notify('spec_pending', spec)

    def spec_group_started(self, spec_group):
        self.notify('spec_group_started', spec_group)

    def spec_group_finished(self, spec_group):
        self.notify('spec_group_finished', spec_group)

    def notify(self, event, *args):
        for listener in self.listeners:
            getattr(listener, event)(*args)
