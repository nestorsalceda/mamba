# -*- coding: utf-8 -*-


class Runner(object):

    def __init__(self, example_collector, reporter):
        self.example_collector = example_collector
        self.reporter = reporter
        self.has_failed_examples = False

    def run(self):
        self.reporter.start()

        for module in self.example_collector.modules():
            self._run_examples_in(module)

        self.reporter.finish()

    def _run_examples_in(self, module):
        for example in module.examples:
            example.run(self.reporter)

            if example.failed:
                self.has_failed_examples = True
