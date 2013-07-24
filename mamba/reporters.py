# -*- coding: utf-8 -*-


class Reporter(object):

    def spec_started(self, spec):
        pass

    def spec_passed(self, spec):
        pass

    def spec_failed(self, spec):
        pass

    def spec_pending(self, spec):
        pass

    def spec_group_started(self, spec_group):
        pass

    def spec_group_finished(self, spec_group):
        pass
