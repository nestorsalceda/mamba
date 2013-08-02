# -*- coding: utf-8 -*-

class Runner(object):

    def __init__(self, reporter):
        self.reporter = reporter
        self.has_failed_examples = False

    def run(self, examples):
        for example in examples:
            example.run(self.reporter)

            if example.failed:
                self.has_failed_examples = True
